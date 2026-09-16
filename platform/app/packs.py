from __future__ import annotations

from typing import Any

DATA_KINDS = [
    {
        "id": "alert",
        "label": "Alert",
        "used_by": ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7"],
        "hint": "JSON object with timestamp, host, user, alert_type, summary.",
    },
    {
        "id": "telemetry",
        "label": "Telemetry",
        "used_by": ["C0", "C1", "C2", "C3", "C4", "C5"],
        "hint": "Map of source → records, each with event_id. Sources: process_events, network, file, registry, identity, cloud.",
    },
    {
        "id": "knowledge",
        "label": "Knowledge corpus",
        "used_by": ["C1", "C3", "C4", "C5", "C6", "C7"],
        "hint": "{index_version, passages:[{passage_id, source_id, source_version, category, corpus_tags, text}]}",
    },
    {
        "id": "query_pack",
        "label": "C4 query pack",
        "used_by": ["C4"],
        "hint": "{version, queries:[{tool, arguments}]}",
    },
    {
        "id": "oracle_evidence",
        "label": "C6 oracle evidence",
        "used_by": ["C6"],
        "hint": "Array of decisive records with event_id, source, timestamp, host, fields.",
    },
    {
        "id": "oracle_plan",
        "label": "C7 oracle plan",
        "used_by": ["C7"],
        "hint": "Array of {order, question, tool, arguments}.",
    },
    {
        "id": "ground_truth",
        "label": "Ground truth (sealed)",
        "used_by": [],
        "hint": "Never sent to the model, context builder, knowledge, or telemetry gateway.",
    },
]

KIND_INDEX = {item["id"]: item for item in DATA_KINDS}


def empty_pack() -> dict[str, Any]:
    return {
        "incident_id": "incident-untitled",
        "name": "Untitled incident",
        "alert": {},
        "scope": {},
        "telemetry": {},
        "oracle_evidence": [],
        "oracle_plan": [],
        "fixed_query_pack": None,
        "knowledge_corpus": None,
        "ground_truth": None,
    }


def merge_part(pack: dict[str, Any], kind: str, payload: Any) -> dict[str, Any]:
    if kind not in KIND_INDEX:
        raise ValueError(f"unknown data kind '{kind}'")
    next_pack = dict(pack)
    if kind == "alert":
        if not isinstance(payload, dict):
            raise ValueError("alert must be a JSON object")
        next_pack["alert"] = payload
        if payload.get("host"):
            scope = dict(next_pack.get("scope") or {})
            hosts = list(scope.get("hosts") or [])
            if payload["host"] not in hosts:
                hosts.append(payload["host"])
            scope["hosts"] = hosts
            next_pack["scope"] = scope
        if payload.get("summary") and next_pack.get("name") in {None, "", "Untitled incident"}:
            next_pack["name"] = payload["summary"]
    elif kind == "telemetry":
        next_pack["telemetry"] = _merge_telemetry(next_pack.get("telemetry") or {}, payload)
    elif kind == "knowledge":
        next_pack["knowledge_corpus"] = _as_corpus(payload)
    elif kind == "query_pack":
        if not isinstance(payload, dict) or "queries" not in payload:
            raise ValueError("query pack must be {version, queries:[...]}")
        next_pack["fixed_query_pack"] = payload
    elif kind == "oracle_evidence":
        records = payload if isinstance(payload, list) else payload.get("records")
        if not isinstance(records, list):
            raise ValueError("oracle evidence must be an array of records")
        next_pack["oracle_evidence"] = records
    elif kind == "oracle_plan":
        steps = payload if isinstance(payload, list) else payload.get("steps") or payload.get("oracle_plan")
        if not isinstance(steps, list):
            raise ValueError("oracle plan must be an array of steps")
        next_pack["oracle_plan"] = steps
    elif kind == "ground_truth":
        if not isinstance(payload, dict):
            raise ValueError("ground truth must be a JSON object")
        next_pack["ground_truth"] = payload
    return next_pack


def _merge_telemetry(existing: dict[str, Any], payload: Any) -> dict[str, Any]:
    merged = {source: list(items or []) for source, items in existing.items()}
    if isinstance(payload, dict) and "source" in payload and "records" in payload:
        source = str(payload["source"])
        records = payload["records"]
        if not isinstance(records, list):
            raise ValueError("telemetry.records must be a list")
        merged.setdefault(source, []).extend(records)
        return merged
    if isinstance(payload, dict):
        for source, records in payload.items():
            if source in {"incident_id", "name", "alert", "scope"}:
                continue
            if not isinstance(records, list):
                raise ValueError(f"telemetry.{source} must be a list")
            merged.setdefault(source, []).extend(records)
        return merged
    raise ValueError("telemetry must be a source map or {source, records}")


def _as_corpus(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict) and isinstance(payload.get("passages"), list):
        return {
            "index_version": payload.get("index_version") or "uploaded",
            "passages": payload["passages"],
        }
    if isinstance(payload, list):
        return {"index_version": "uploaded", "passages": payload}
    raise ValueError("knowledge must be {passages:[...]} or an array of passages")


def part_errors(kind: str, payload: Any) -> list[str]:
    try:
        merge_part(empty_pack(), kind, payload)
    except ValueError as exc:
        return [str(exc)]
    errors = []
    if kind == "telemetry":
        pack = merge_part(empty_pack(), kind, payload)
        for source, items in (pack.get("telemetry") or {}).items():
            for index, item in enumerate(items or []):
                if not isinstance(item, dict) or not item.get("event_id"):
                    errors.append(f"{source}[{index}] needs event_id")
    if kind == "oracle_evidence":
        records = payload if isinstance(payload, list) else (payload or {}).get("records") or []
        for index, item in enumerate(records):
            if not isinstance(item, dict) or not (item.get("event_id") or item.get("evidence_id")):
                errors.append(f"oracle_evidence[{index}] needs event_id")
    return errors


def packs_present(pack: dict[str, Any] | None) -> dict[str, bool]:
    pack = pack or {}
    telemetry = pack.get("telemetry") or {}
    return {
        "alert": bool(pack.get("alert")),
        "telemetry": bool(telemetry),
        "knowledge": bool(pack.get("knowledge_corpus")),
        "query_pack": bool(pack.get("fixed_query_pack")),
        "oracle_evidence": bool(pack.get("oracle_evidence")),
        "oracle_plan": bool(pack.get("oracle_plan")),
        "ground_truth": bool(pack.get("ground_truth")),
    }
