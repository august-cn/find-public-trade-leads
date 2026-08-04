#!/usr/bin/env python3
"""Maintain a project-local, git-ignored lead history for cross-batch deduplication."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


STATE_VERSION = 1
LEGAL_SUFFIXES = {
    "ag", "bv", "co", "company", "corp", "corporation", "eirl", "gmbh",
    "inc", "incorporated", "kg", "kgaa", "limited", "llc", "llp", "ltd",
    "oy", "oyj", "plc", "pte", "pty", "sa", "sarl", "sas", "srl", "spa",
    "spol", "zoo",
}
LEGAL_SUFFIX_SEQUENCES = (
    ("sp", "z", "o", "o"),
    ("s", "a"),
    ("s", "l"),
    ("s", "r", "l"),
    ("s", "p", "a"),
)


class DuplicateHistoryError(Exception):
    def __init__(self, payload: dict):
        super().__init__("当前批次包含历史或批内重复企业。")
        self.payload = payload


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def state_path(project_root: Path) -> Path:
    return project_root / ".find-public-trade-leads" / "history.json"


def empty_state() -> dict:
    return {
        "version": STATE_VERSION,
        "updated_at": "",
        "batches": [],
        "companies": [],
    }


def load_state(path: Path) -> dict:
    if not path.exists():
        return empty_state()
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"无法读取项目客户历史：{exc}") from exc
    if state.get("version") != STATE_VERSION:
        raise SystemExit("项目客户历史版本不受支持。")
    if not isinstance(state.get("batches"), list) or not isinstance(state.get("companies"), list):
        raise SystemExit("项目客户历史结构无效。")
    return state


def atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=".history-", suffix=".json", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary_path, 0o600)
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def words(value: str) -> list[str]:
    text = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return [token for token in re.findall(r"\w+", text, flags=re.UNICODE) if token != "_"]


def normalize_name(value: str) -> str:
    tokens = words(value)
    changed = True
    while tokens and changed:
        changed = False
        for suffix in LEGAL_SUFFIX_SEQUENCES:
            if tuple(tokens[-len(suffix):]) == suffix:
                del tokens[-len(suffix):]
                changed = True
                break
        if not changed and tokens[-1] in LEGAL_SUFFIXES:
            tokens.pop()
            changed = True
    return "".join(tokens)


def normalize_market(value: str) -> str:
    return "".join(words(value))


def normalize_domain(value: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    parsed = urlparse(raw if "://" in raw else f"//{raw}")
    host = (parsed.hostname or "").strip(".").casefold()
    if host.startswith("www."):
        host = host[4:]
    try:
        return host.encode("idna").decode("ascii")
    except UnicodeError:
        return host


def identity_keys(company: str, legal_name: str, website: str, market: str) -> list[str]:
    market_key = normalize_market(market)
    keys: list[str] = []
    domain = normalize_domain(website)
    if domain:
        keys.append(f"domain:{market_key}:{domain}")
    for value in (company, legal_name):
        name = normalize_name(value)
        if name:
            keys.append(f"name:{market_key}:{name}")
    return sorted(set(keys))


def suggested_batch_id(state: dict) -> str:
    return f"batch-{len(state['batches']) + 1:04d}"


def public_context(state: dict, path: Path, include_companies: bool = False) -> dict:
    last_batch = state["batches"][-1] if state["batches"] else None
    context = {
        "has_history": bool(state["batches"]),
        "history_file": str(path),
        "batch_count": len(state["batches"]),
        "historical_company_count": len(state["companies"]),
        "suggested_batch_id": suggested_batch_id(state),
        "previous_batch_id": last_batch.get("batch_id", "") if last_batch else "",
        "last_brief": last_batch.get("brief") if last_batch else None,
    }
    if include_companies:
        context["companies"] = [
            {
                "company": item.get("company", ""),
                "legal_name": item.get("legal_name", ""),
                "website": item.get("website", ""),
                "market": item.get("market", ""),
                "identity_keys": item.get("identity_keys", []),
                "first_seen_batch": item.get("first_seen_batch", ""),
                "last_seen_batch": item.get("last_seen_batch", ""),
                "statuses": item.get("statuses", []),
            }
            for item in state["companies"]
        ]
    return context


def find_matches(state: dict, keys: list[str]) -> list[dict]:
    key_set = set(keys)
    return [item for item in state["companies"] if key_set.intersection(item.get("identity_keys", []))]


def candidate_rows(data: dict) -> list[tuple[str, dict]]:
    rows: list[tuple[str, dict]] = []
    rows.extend(("qualified", row) for row in data.get("leads", []) if isinstance(row, dict))
    rows.extend(("near_match", row) for row in data.get("near_matches", []) if isinstance(row, dict))
    rows.extend(("excluded", row) for row in data.get("excluded", []) if isinstance(row, dict))
    return rows


def record(args: argparse.Namespace, path: Path, state: dict) -> dict:
    input_path = args.input.expanduser().resolve()
    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"无法读取工作簿输入JSON：{exc}") from exc

    brief = data.get("brief") if isinstance(data.get("brief"), dict) else {}
    batch_id = str(args.batch_id or brief.get("batch_id") or suggested_batch_id(state)).strip()
    skipped_unidentifiable = 0
    target_market = str(brief.get("target_market", ""))
    recorded_at = now_utc()
    prepared_rows: list[tuple[str, str, str, str, str, list[str]]] = []

    for status, row in candidate_rows(data):
        company = str(row.get("company", "")).strip()
        legal_name = str(row.get("legal_name", "")).strip()
        website = str(row.get("website", "")).strip()
        market = str(row.get("country") or target_market).strip()
        keys = identity_keys(company, legal_name, website, market)
        if not keys:
            skipped_unidentifiable += 1
            continue
        prepared_rows.append((status, company, legal_name, website, market, keys))

    all_identity_keys = sorted({key for prepared in prepared_rows for key in prepared[5]})
    existing_batch = next(
        (batch for batch in state["batches"] if batch.get("batch_id") == batch_id),
        None,
    )
    if existing_batch:
        if existing_batch.get("company_identity_keys", []) == all_identity_keys:
            return {
                "recorded": False,
                "idempotent": True,
                "batch_id": batch_id,
                "historical_company_count": len(state["companies"]),
                "history_file": str(path),
            }
        raise SystemExit(f"批次编号已存在但企业集合不同：{batch_id}")

    historical_duplicates: list[dict] = []
    within_batch_duplicates: list[dict] = []
    seen_keys: set[str] = set()
    for _, company, legal_name, website, market, keys in prepared_rows:
        matches = find_matches(state, keys)
        if matches:
            historical_duplicates.append({
                "company": company,
                "legal_name": legal_name,
                "website": website,
                "market": market,
                "matches": [match.get("company", "") for match in matches],
            })
        if seen_keys.intersection(keys):
            within_batch_duplicates.append({
                "company": company,
                "legal_name": legal_name,
                "website": website,
                "market": market,
            })
        seen_keys.update(keys)

    if historical_duplicates or within_batch_duplicates:
        raise DuplicateHistoryError({
            "recorded": False,
            "error": "duplicates_found",
            "batch_id": batch_id,
            "historical_duplicates": historical_duplicates,
            "within_batch_duplicates": within_batch_duplicates,
            "history_file": str(path),
        })

    for status, company, legal_name, website, market, keys in prepared_rows:
        state["companies"].append({
            "company": company,
            "legal_name": legal_name,
            "website": website,
            "market": market,
            "identity_keys": keys,
            "first_seen_batch": batch_id,
            "last_seen_batch": batch_id,
            "statuses": [status],
        })

    batch = {
        "batch_id": batch_id,
        "previous_batch_id": str(brief.get("previous_batch_id", "")),
        "recorded_at": recorded_at,
        "input_file": str(input_path),
        "output_workbook": str(args.output_workbook.expanduser().resolve()) if args.output_workbook else "",
        "brief": brief,
        "company_identity_keys": all_identity_keys,
        "counts": {
            "qualified": len(data.get("leads", [])),
            "near_matches": len(data.get("near_matches", [])),
            "excluded": len(data.get("excluded", [])),
            "added_to_history": len(prepared_rows),
            "matched_existing": 0,
            "skipped_unidentifiable": skipped_unidentifiable,
        },
    }
    state["batches"].append(batch)
    state["updated_at"] = recorded_at
    atomic_write(path, state)
    return {
        "recorded": True,
        "batch_id": batch_id,
        "added_to_history": len(prepared_rows),
        "matched_existing": 0,
        "skipped_unidentifiable": skipped_unidentifiable,
        "historical_company_count": len(state["companies"]),
        "history_file": str(path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)

    context_parser = subparsers.add_parser("context", help="输出上次Brief和历史统计")
    context_parser.add_argument("--include-companies", action="store_true")

    check_parser = subparsers.add_parser("check", help="检查一个候选公司是否已出现")
    check_parser.add_argument("--company", default="")
    check_parser.add_argument("--legal-name", default="")
    check_parser.add_argument("--website", default="")
    check_parser.add_argument("--market", default="")

    record_parser = subparsers.add_parser("record", help="在Excel成功生成后记录本批次")
    record_parser.add_argument("--input", type=Path, required=True)
    record_parser.add_argument("--output-workbook", type=Path)
    record_parser.add_argument("--batch-id", default="")

    clear_parser = subparsers.add_parser("clear", help="清空当前项目客户历史")
    clear_parser.add_argument("--yes", action="store_true")

    args = parser.parse_args()
    project_root = args.project_root.expanduser().resolve()
    if not project_root.is_dir():
        raise SystemExit(f"Codex项目目录不存在：{project_root}")
    path = state_path(project_root)
    state = load_state(path)

    if args.command == "context":
        print(json.dumps(public_context(state, path, args.include_companies), ensure_ascii=False))
        return 0

    if args.command == "check":
        keys = identity_keys(args.company, args.legal_name, args.website, args.market)
        matches = find_matches(state, keys)
        print(json.dumps({
            "duplicate": bool(matches),
            "identity_keys": keys,
            "matches": matches,
        }, ensure_ascii=False))
        return 0 if not matches else 3

    if args.command == "record":
        try:
            result = record(args, path, state)
        except DuplicateHistoryError as exc:
            print(json.dumps(exc.payload, ensure_ascii=False))
            return 4
        print(json.dumps(result, ensure_ascii=False))
        return 0

    if not args.yes:
        raise SystemExit("清空历史属于破坏性操作；仅在用户明确要求后添加 --yes。")
    existed = path.exists()
    if existed:
        path.unlink()
    print(json.dumps({"cleared": existed, "history_file": str(path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
