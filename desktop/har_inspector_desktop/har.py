from __future__ import annotations

import csv
import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


class HarFormatError(ValueError):
    pass


def _ensure_entry_id(entry: dict[str, Any], index: int) -> str:
    entry_id = entry.get("_id")
    if isinstance(entry_id, str) and entry_id:
        return entry_id
    entry_id = f"entry-{index}"
    entry["_id"] = entry_id
    return entry_id


def load_har(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise HarFormatError("Top-level JSON value must be an object")
    log = data.get("log")
    if not isinstance(log, dict):
        raise HarFormatError("Missing 'log' object")
    entries = log.get("entries")
    if not isinstance(entries, list):
        raise HarFormatError("Missing 'log.entries' array")
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise HarFormatError(f"Entry {i} must be an object")
        _ensure_entry_id(entry, i)
    return data


def validate_har_file(path: str | Path) -> tuple[bool, str | None]:
    try:
        load_har(path)
    except Exception as e:  # pragma: no cover (used for CLI)
        return False, str(e)
    return True, None


def _entry_get(entry: dict[str, Any], *keys: str, default: Any = "") -> Any:
    cur: Any = entry
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


@dataclass(frozen=True)
class EntryRow:
    entry_id: str
    method: str
    url: str
    status: int
    size: int
    time_ms: float


def iter_entry_rows(har: dict[str, Any]) -> Iterable[EntryRow]:
    entries = _entry_get(har, "log", "entries", default=[])
    if not isinstance(entries, list):
        return []
    for i, entry_any in enumerate(entries):
        if not isinstance(entry_any, dict):
            continue
        entry_id = _ensure_entry_id(entry_any, i)
        method = str(_entry_get(entry_any, "request", "method", default="")).upper()
        url = str(_entry_get(entry_any, "request", "url", default=""))
        status = int(_entry_get(entry_any, "response", "status", default=0) or 0)
        size = int(_entry_get(entry_any, "response", "content", "size", default=0) or 0)
        time_ms = float(_entry_get(entry_any, "time", default=0) or 0)
        yield EntryRow(entry_id=entry_id, method=method, url=url, status=status, size=size, time_ms=time_ms)


def strip_internal_ids(har: dict[str, Any]) -> dict[str, Any]:
    cleaned = deepcopy(har)
    log = cleaned.get("log")
    if not isinstance(log, dict):
        return cleaned
    entries = log.get("entries")
    if not isinstance(entries, list):
        return cleaned
    for entry in entries:
        if isinstance(entry, dict):
            entry.pop("_id", None)
    return cleaned


def save_har(path: str | Path, har: dict[str, Any]) -> None:
    path = Path(path)
    cleaned = strip_internal_ids(har)
    path.write_text(json.dumps(cleaned, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def export_csv(path: str | Path, rows: Iterable[EntryRow]) -> None:
    path = Path(path)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Method", "URL", "Status", "Size", "Time (ms)"])
        for r in rows:
            writer.writerow([r.method, r.url, r.status, r.size, round(r.time_ms, 3)])

