#!/usr/bin/env python3
"""Persist the user's Apollo workflow preference without storing credentials."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path


MODES = {
    "public_only": "未注册、未安装、未连接或不可用",
    "connected_free": "已连接，但不使用积分",
    "credit_per_call": "已连接，允许逐次审批积分",
}


def default_state_file() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    root = Path(codex_home).expanduser() if codex_home else Path.home() / ".codex"
    return root / "state" / "find-public-trade-leads" / "apollo-preference.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_state(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"无法读取 Apollo 状态文件：{exc}") from exc
    if state.get("status") not in MODES:
        raise SystemExit("Apollo 状态文件无效；请运行 clear 后重新选择。")
    return state


def write_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(
        prefix=".apollo-preference-", suffix=".json", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(state, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary_path, 0o600)
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def output(payload: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False))
        return
    if not payload.get("configured"):
        print("尚未选择 Apollo 状态。")
        return
    print(f"Apollo 状态：{payload['label_zh']} ({payload['status']})")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-file", type=Path, default=default_state_file())
    subparsers = parser.add_subparsers(dest="command", required=True)

    get_parser = subparsers.add_parser("get", help="读取已保存状态")
    get_parser.add_argument("--json", action="store_true")

    set_parser = subparsers.add_parser("set", help="保存状态")
    set_parser.add_argument("status", choices=sorted(MODES))
    set_parser.add_argument("--json", action="store_true")

    clear_parser = subparsers.add_parser("clear", help="忘记状态并在下次重新选择")
    clear_parser.add_argument("--json", action="store_true")

    args = parser.parse_args()
    state_file = args.state_file.expanduser().resolve()

    if args.command == "get":
        state = read_state(state_file)
        if state is None:
            output({"configured": False, "state_file": str(state_file)}, args.json)
            return 2
        output({"configured": True, "state_file": str(state_file), **state}, args.json)
        return 0

    if args.command == "set":
        existing = read_state(state_file)
        now = utc_now()
        state = {
            "version": 1,
            "status": args.status,
            "label_zh": MODES[args.status],
            "selected_at": existing.get("selected_at", now) if existing else now,
            "updated_at": now,
        }
        write_state(state_file, state)
        output({"configured": True, "state_file": str(state_file), **state}, args.json)
        return 0

    existed = state_file.exists()
    if existed:
        state_file.unlink()
    output(
        {"configured": False, "cleared": existed, "state_file": str(state_file)},
        args.json,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
