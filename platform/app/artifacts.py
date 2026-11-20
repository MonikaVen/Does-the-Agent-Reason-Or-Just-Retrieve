"""Read-only views of suite pack files and lab SQLite trajectories."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .store import ROOT

REPORTS = ROOT / "reports"
PAYLOAD_LIMIT = 6000


class ArtifactError(ValueError):
    pass


def resolve_suite(name: str, reports_root: Path | None = None) -> Path:
    root = (reports_root or REPORTS).resolve()
    if not name or name.strip() != name or "/" in name or "\\" in name or name in {".", ".."}:
        raise ArtifactError("suite must be a single directory name under reports/")
    suite = (root / name).resolve()
    if suite.parent != root or not suite.is_dir():
        raise ArtifactError(f"unknown suite {name}")
    return suite


def list_suites(reports_root: Path | None = None) -> list[dict[str, Any]]:
    root = (reports_root or REPORTS).resolve()
    if not root.is_dir():
        return []
    suites = []
    candidates = [path for path in root.iterdir() if path.is_dir()]
    candidates.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    for path in candidates:
        if not path.is_dir():
            continue
        packs = path / "packs"
        databases = sorted(path.glob("lab-w*.sqlite3"))
        pack_files = list(packs.glob("*.json")) if packs.is_dir() else []
        if not pack_files and not databases and not (path / "c0c7-table.md").exists():
            continue
        suites.append(
            {
                "name": path.name,
                "pack_files": len([item for item in pack_files if not item.name.endswith(".error.json")]),
                "error_files": len([item for item in pack_files if item.name.endswith(".error.json")]),
                "databases": [item.name for item in databases],
            }
        )
    return suites


def list_packs(suite_name: str, reports_root: Path | None = None) -> dict[str, Any]:
    suite = resolve_suite(suite_name, reports_root)
    by_incident: dict[str, dict[str, Any]] = {}
    packs_dir = suite / "packs"
    if packs_dir.is_dir():
        for path in sorted(packs_dir.glob("*.json")):
            summary = _summarize_pack_file(path)
            by_incident[summary["incident_id"]] = summary
    live = _sqlite_incidents(suite)
    for incident_id, rows in live.items():
        existing = by_incident.get(incident_id)
        if existing is None:
            by_incident[incident_id] = _summary_from_sqlite(incident_id, rows)
            continue
        known = {run["condition"] for run in existing["runs"]}
        for row in rows:
            if row["condition"] not in known or row["status"] == "running":
                existing["runs"] = [run for run in existing["runs"] if run["condition"] != row["condition"]]
                existing["runs"].append(_run_brief(row))
        existing["runs"].sort(key=lambda run: run.get("condition") or "")
        _recount(existing)
    packs = [by_incident[key] for key in sorted(by_incident)]
    running = next((item for item in packs if any(run.get("status") == "running" for run in item["runs"])), None)
    return {
        "suite": suite.name,
        "pack_count": len(packs),
        "running_incident": running["incident_id"] if running else None,
        "packs": packs,
    }


def pack_detail(suite_name: str, incident_id: str, reports_root: Path | None = None) -> dict[str, Any]:
    catalog = list_packs(suite_name, reports_root)
    for pack in catalog["packs"]:
        if pack["incident_id"] == incident_id:
            return pack
    raise ArtifactError(f"unknown incident {incident_id}")


def run_detail(suite_name: str, run_id: str, reports_root: Path | None = None) -> dict[str, Any]:
    suite = resolve_suite(suite_name, reports_root)
    if not run_id or "/" in run_id or "\\" in run_id:
        raise ArtifactError("invalid run id")
    for database in sorted(suite.glob("lab-w*.sqlite3")):
        found = _read_run(database, run_id)
        if found is not None:
            return found
    raise ArtifactError(f"unknown run {run_id}")


def _summarize_pack_file(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    incident_id = data.get("incident_id") or _incident_from_filename(path.name)
    if path.name.endswith(".error.json"):
        return {
            "incident_id": incident_id,
            "dataset": None,
            "scenario": None,
            "provider": None,
            "model": None,
            "generated_at": data.get("at"),
            "completed": 0,
            "failed": 1,
            "skipped": 0,
            "pack_error": data.get("error"),
            "on_disk": True,
            "runs": [],
        }
    runs = [_file_run(item) for item in data.get("runs") or []]
    summary = {
        "incident_id": incident_id,
        "dataset": data.get("dataset"),
        "scenario": data.get("scenario"),
        "provider": data.get("provider"),
        "model": data.get("model"),
        "generated_at": data.get("generated_at"),
        "completed": data.get("completed"),
        "failed": data.get("failed"),
        "skipped": data.get("skipped"),
        "pack_error": None,
        "on_disk": True,
        "runs": runs,
    }
    _recount(summary)
    return summary


def _file_run(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "condition": item.get("condition"),
        "status": item.get("status"),
        "verdict": item.get("verdict"),
        "confidence": item.get("confidence"),
        "tool_observations": item.get("tool_observations"),
        "knowledge_retrievals": item.get("knowledge_retrievals"),
        "run_id": item.get("run_id"),
        "started_at": item.get("started_at"),
        "completed_at": item.get("completed_at"),
        "error": item.get("error"),
        "database": None,
    }


def _summary_from_sqlite(incident_id: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    model = None
    for row in rows:
        manifest = row.get("manifest") or {}
        if manifest.get("model_profile"):
            model = manifest["model_profile"]
            break
    summary = {
        "incident_id": incident_id,
        "dataset": None,
        "scenario": None,
        "provider": None,
        "model": model,
        "generated_at": None,
        "completed": None,
        "failed": None,
        "skipped": None,
        "pack_error": None,
        "on_disk": False,
        "runs": [_run_brief(row) for row in rows],
    }
    _recount(summary)
    return summary


def _recount(summary: dict[str, Any]) -> None:
    runs = summary["runs"]
    summary["runs"] = sorted(runs, key=lambda run: run.get("condition") or "")
    summary["completed"] = sum(1 for run in runs if run.get("status") == "completed")
    summary["failed"] = sum(1 for run in runs if run.get("status") == "failed") + (1 if summary.get("pack_error") and not runs else 0)
    summary["skipped"] = sum(1 for run in runs if run.get("status") == "skipped")


def _sqlite_incidents(suite: Path) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for database in sorted(suite.glob("lab-w*.sqlite3")):
        try:
            rows = _read_run_index(database)
        except sqlite3.Error:
            continue
        for row in rows:
            grouped.setdefault(row["incident_id"], []).append(row)
    return grouped


def _read_run_index(database: Path) -> list[dict[str, Any]]:
    with _connect(database) as conn:
        fetched = conn.execute(
            """
            SELECT id, condition, status, started_at, completed_at, manifest_json, report_json, error
            FROM runs ORDER BY rowid
            """
        ).fetchall()
    rows = []
    for item in fetched:
        manifest = json.loads(item["manifest_json"]) if item["manifest_json"] else {}
        report = json.loads(item["report_json"]) if item["report_json"] else {}
        if not isinstance(report, dict):
            report = {}
        rows.append(
            {
                "id": item["id"],
                "condition": item["condition"],
                "status": item["status"],
                "started_at": item["started_at"],
                "completed_at": item["completed_at"],
                "error": item["error"],
                "verdict": report.get("verdict"),
                "confidence": report.get("confidence"),
                "incident_id": manifest.get("incident_id") or item["id"],
                "manifest": manifest,
                "database": database.name,
            }
        )
    return rows


def _incident_from_filename(name: str) -> str:
    if name.endswith(".error.json"):
        return name[: -len(".error.json")]
    if name.endswith(".json"):
        return name[: -len(".json")]
    return name


def _run_brief(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "condition": row.get("condition"),
        "status": row.get("status"),
        "verdict": row.get("verdict"),
        "confidence": row.get("confidence"),
        "tool_observations": None,
        "knowledge_retrievals": None,
        "run_id": row.get("id"),
        "started_at": row.get("started_at"),
        "completed_at": row.get("completed_at"),
        "error": row.get("error"),
        "database": row.get("database"),
    }


def _read_run(database: Path, run_id: str) -> dict[str, Any] | None:
    with _connect(database) as conn:
        row = conn.execute(
            """
            SELECT id, condition, status, started_at, completed_at, manifest_json, state_json, report_json, error
            FROM runs WHERE id = ?
            """,
            (run_id,),
        ).fetchone()
        if row is None:
            return None
        events = conn.execute(
            """
            SELECT sequence, timestamp, kind, service, stage, payload_json
            FROM events WHERE run_id = ? ORDER BY sequence ASC
            """,
            (run_id,),
        ).fetchall()
    report = json.loads(row["report_json"]) if row["report_json"] else None
    manifest = json.loads(row["manifest_json"]) if row["manifest_json"] else None
    state = json.loads(row["state_json"]) if row["state_json"] else None
    return {
        "database": database.name,
        "id": row["id"],
        "condition": row["condition"],
        "status": row["status"],
        "started_at": row["started_at"],
        "completed_at": row["completed_at"],
        "error": row["error"],
        "incident_id": (manifest or {}).get("incident_id"),
        "model_profile": (manifest or {}).get("model_profile"),
        "report": report,
        "state": _truncate_value(state),
        "events": [_event_row(item) for item in events],
    }


def _event_row(row: sqlite3.Row) -> dict[str, Any]:
    payload = json.loads(row["payload_json"]) if row["payload_json"] else {}
    text = json.dumps(payload, ensure_ascii=False)
    truncated = len(text) > PAYLOAD_LIMIT
    if truncated:
        payload = {"truncated": True, "preview": text[:PAYLOAD_LIMIT]}
    return {
        "sequence": row["sequence"],
        "timestamp": row["timestamp"],
        "kind": row["kind"],
        "service": row["service"],
        "stage": row["stage"],
        "payload": payload,
        "truncated": truncated,
    }


def _truncate_value(value: Any) -> Any:
    if value is None:
        return None
    text = json.dumps(value, ensure_ascii=False)
    if len(text) <= PAYLOAD_LIMIT:
        return value
    return {"truncated": True, "preview": text[:PAYLOAD_LIMIT]}


def _connect(database: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn
