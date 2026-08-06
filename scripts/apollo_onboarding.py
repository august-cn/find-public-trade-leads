#!/usr/bin/env python3
"""Persist whether the one-time Apollo setup recommendation was shown."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def state_file(project_root: Path) -> Path:
    return project_root / ".find-public-trade-leads" / "apollo-onboarding.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_state(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"无法读取 Apollo 引导状态文件：{exc}") from exc
    if state.get("recommendation_shown") is not True:
        raise SystemExit("Apollo 引导状态文件无效；请运行 clear 后重试。")
    return state


def write_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(
        prefix=".apollo-onboarding-", suffix=".json", dir=path.parent
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


def emit(payload: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False))
    elif payload.get("recommendation_shown"):
        print("Apollo 注册与插件建议已显示。")
    else:
        print("Apollo 注册与插件建议尚未显示。")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        required=True,
        help="当前Codex项目根目录；状态写入其git忽略目录",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command, help_text in (
        ("get", "读取一次性引导状态"),
        ("mark-shown", "记录引导已经显示"),
        ("clear", "清除状态以重新测试首次使用体验"),
    ):
        subparser = subparsers.add_parser(command, help=help_text)
        subparser.add_argument("--json", action="store_true")

    args = parser.parse_args()
    state_path = state_file(args.project_root.expanduser().resolve())

    if args.command == "get":
        state = read_state(state_path)
        if state is None:
            emit(
                {"recommendation_shown": False, "state_file": str(state_path)},
                args.json,
            )
            return 2
        emit({"state_file": str(state_path), **state}, args.json)
        return 0

    if args.command == "mark-shown":
        existing = read_state(state_path)
        shown_at = existing.get("shown_at", utc_now()) if existing else utc_now()
        state = {"version": 1, "recommendation_shown": True, "shown_at": shown_at}
        write_state(state_path, state)
        emit({"state_file": str(state_path), **state}, args.json)
        return 0

    existed = state_path.exists()
    if existed:
        state_path.unlink()
    emit(
        {
            "recommendation_shown": False,
            "cleared": existed,
            "state_file": str(state_path),
        },
        args.json,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
