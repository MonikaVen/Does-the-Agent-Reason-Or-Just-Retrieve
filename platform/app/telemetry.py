from __future__ import annotations

from datetime import datetime
from typing import Any


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def flatten_pack(pack: dict[str, Any]) -> list[dict[str, Any]]:
    records = []
    telemetry = pack.get("telemetry") or {}
    for source, items in telemetry.items():
        for item in items or []:
            records.append(normalize_record(source, item))
    return records


def normalize_record(source: str, item: dict[str, Any]) -> dict[str, Any]:
    fields = {
        key: value
        for key, value in item.items()
        if key not in {"event_id", "timestamp", "host", "source"}
    }
    return {
        "evidence_id": item.get("event_id") or item.get("evidence_id"),
        "source": item.get("source") or source,
        "timestamp": item.get("timestamp"),
        "host": item.get("host"),
        "fields": fields if fields else item,
        "raw": item,
    }


class TelemetryStore:
    """Read-only incident telemetry. Ground-truth labels never live here."""

    def __init__(self, pack: dict[str, Any]) -> None:
        self.pack = pack
        self.scope = pack.get("scope") or {}
        self.records = flatten_pack(pack)

    def in_scope(self, record: dict[str, Any]) -> bool:
        allowed = set(self.scope.get("allowed_log_sources") or [])
        if allowed and record["source"] not in allowed:
            return False
        hosts = set(self.scope.get("hosts") or [])
        if hosts and record.get("host") and record["host"] not in hosts:
            return False
        start = _parse_ts(self.scope.get("start"))
        end = _parse_ts(self.scope.get("end"))
        ts = _parse_ts(record.get("timestamp"))
        if start and ts and ts < start:
            return False
        if end and ts and ts > end:
            return False
        return True

    def scoped(self) -> list[dict[str, Any]]:
        return [record for record in self.records if self.in_scope(record)]


class TelemetryGateway:
    def __init__(self, store: TelemetryStore, max_records: int = 100) -> None:
        self.store = store
        self.max_records = max_records

    def _cap(self, records: list[dict[str, Any]], limit: int | None) -> tuple[list[dict[str, Any]], bool]:
        cap = min(self.max_records, limit or self.max_records)
        truncated = len(records) > cap
        return records[:cap], truncated

    def grep_logs(self, arguments: dict[str, Any]) -> dict[str, Any]:
        pattern = str(arguments.get("pattern") or "").lower()
        source = arguments.get("source")
        matched = []
        for record in self.store.scoped():
            if source and record["source"] != source:
                continue
            blob = str(record["raw"]).lower()
            if pattern and pattern not in blob:
                continue
            matched.append(self._public(record))
        return self._observation("grep_logs", matched, arguments.get("limit"))

    def query_events(self, arguments: dict[str, Any]) -> dict[str, Any]:
        source = arguments.get("source")
        filters = arguments.get("filter") or {}
        matched = []
        for record in self.store.scoped():
            if source and record["source"] != source:
                continue
            if self._matches(record, filters):
                matched.append(self._public(record))
        order = arguments.get("order")
        if order == "timestamp_ascending":
            matched.sort(key=lambda rec: rec.get("timestamp") or "")
        elif order == "timestamp_descending":
            matched.sort(key=lambda rec: rec.get("timestamp") or "", reverse=True)
        return self._observation("query_events", matched, arguments.get("limit"))

    def find_process_tree(self, arguments: dict[str, Any]) -> dict[str, Any]:
        host = arguments.get("host")
        needle = str(arguments.get("process_or_event_id") or "")
        processes = [
            record
            for record in self.store.scoped()
            if record["source"] == "process_events" and (not host or record.get("host") == host)
        ]
        seed = None
        for record in processes:
            raw = record["raw"]
            if needle in {record.get("evidence_id"), str(raw.get("pid") or ""), raw.get("process_name")}:
                seed = record
                break
        if seed is None and processes:
            seed = processes[0]
        if seed is None:
            return self._observation("find_process_tree", [], arguments.get("limit"))
        tree = [seed]
        parent_pid = seed["raw"].get("parent_pid")
        for record in processes:
            if parent_pid and record["raw"].get("pid") == parent_pid:
                tree.insert(0, record)
            if record["raw"].get("parent_pid") == seed["raw"].get("pid"):
                tree.append(record)
        return self._observation("find_process_tree", [self._public(r) for r in tree], arguments.get("limit"))

    def build_timeline(self, arguments: dict[str, Any]) -> dict[str, Any]:
        sources = set(arguments.get("sources") or [])
        host = arguments.get("host")
        records = []
        for record in self.store.scoped():
            if sources and record["source"] not in sources:
                continue
            if host and record.get("host") != host:
                continue
            records.append(self._public(record))
        records.sort(key=lambda rec: rec.get("timestamp") or "")
        return self._observation("build_timeline", records, arguments.get("limit"))

    def search_related(self, arguments: dict[str, Any]) -> dict[str, Any]:
        entity = str(arguments.get("entity") or "")
        matched = []
        for record in self.store.scoped():
            blob = str(record["raw"])
            if entity and entity not in blob and entity != record.get("host"):
                continue
            matched.append(self._public(record))
        return self._observation("search_related", matched, arguments.get("limit"))

    def execute(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        dispatch = {
            "grep_logs": self.grep_logs,
            "query_events": self.query_events,
            "find_process_tree": self.find_process_tree,
            "build_timeline": self.build_timeline,
            "search_related": self.search_related,
        }
        if tool not in dispatch:
            raise ValueError(f"unknown tool {tool}")
        return dispatch[tool](arguments)

    def _matches(self, record: dict[str, Any], filters: dict[str, Any]) -> bool:
        for key, expected in filters.items():
            if key == "host" and record.get("host") != expected:
                return False
            raw = record["raw"]
            fields = record.get("fields") or {}
            actual = raw.get(key, fields.get(key))
            if actual is not None and str(actual).lower() != str(expected).lower():
                return False
            if actual is None and key not in {"host"}:
                blob = str(raw).lower()
                if str(expected).lower() not in blob:
                    return False
        return True

    def _public(self, record: dict[str, Any]) -> dict[str, Any]:
        return {
            "evidence_id": record.get("evidence_id"),
            "source": record.get("source"),
            "timestamp": record.get("timestamp"),
            "host": record.get("host"),
            "fields": record.get("fields") or {},
        }

    def _observation(self, tool: str, records: list[dict[str, Any]], limit: Any) -> dict[str, Any]:
        capped, truncated = self._cap(records, int(limit) if limit else None)
        return {
            "tool": tool,
            "status": "success",
            "records": capped,
            "record_count": len(capped),
            "truncated": truncated,
            "schema_version": "1.0",
        }
