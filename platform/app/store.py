from __future__ import annotations

import json
import os
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DB_PATH = Path(os.environ.get("LAB_DB", str(ROOT / "var" / "lab.sqlite3")))


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


class Store:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or DB_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._init()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def _init(self) -> None:
        with self._lock, self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS datasets (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    incident_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    pack_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY,
                    dataset_id TEXT NOT NULL,
                    condition TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    started_at TEXT,
                    completed_at TEXT,
                    seed INTEGER NOT NULL,
                    budgets_json TEXT NOT NULL,
                    matched_run_id TEXT,
                    manifest_json TEXT,
                    state_json TEXT,
                    report_json TEXT,
                    error TEXT,
                    FOREIGN KEY(dataset_id) REFERENCES datasets(id)
                );
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    sequence INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    service TEXT NOT NULL,
                    stage TEXT,
                    payload_json TEXT NOT NULL,
                    FOREIGN KEY(run_id) REFERENCES runs(id)
                );
                """
            )

    def insert_dataset(self, dataset: dict[str, Any]) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                "INSERT INTO datasets (id, name, incident_id, created_at, pack_json) VALUES (?, ?, ?, ?, ?)",
                (
                    dataset["id"],
                    dataset["name"],
                    dataset["incident_id"],
                    dataset["created_at"],
                    json.dumps(dataset["pack"]),
                ),
            )

    def list_datasets(self) -> list[dict[str, Any]]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                "SELECT id, name, incident_id, created_at, pack_json FROM datasets ORDER BY created_at DESC"
            ).fetchall()
        return [self._dataset_row(row) for row in rows]

    def get_dataset(self, dataset_id: str) -> dict[str, Any] | None:
        with self._lock, self._connect() as conn:
            row = conn.execute(
                "SELECT id, name, incident_id, created_at, pack_json FROM datasets WHERE id = ?",
                (dataset_id,),
            ).fetchone()
        return self._dataset_row(row) if row else None

    def _dataset_row(self, row: sqlite3.Row) -> dict[str, Any]:
        pack = json.loads(row["pack_json"])
        telemetry = pack.get("telemetry") or {}
        counts = {source: len(records or []) for source, records in telemetry.items()}
        return {
            "id": row["id"],
            "name": row["name"],
            "incident_id": row["incident_id"],
            "created_at": row["created_at"],
            "alert": pack.get("alert") or {},
            "scope": pack.get("scope") or {},
            "record_counts": counts,
            "record_total": sum(counts.values()),
            "has_oracle_evidence": bool(pack.get("oracle_evidence")),
            "has_oracle_plan": bool(pack.get("oracle_plan")),
            "has_fixed_query_pack": bool(pack.get("fixed_query_pack")),
            "pack": pack,
        }

    def insert_run(self, run: dict[str, Any]) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO runs (
                    id, dataset_id, condition, status, created_at, started_at, completed_at,
                    seed, budgets_json, matched_run_id, manifest_json, state_json, report_json, error
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run["id"],
                    run["dataset_id"],
                    run["condition"],
                    run["status"],
                    run["created_at"],
                    run.get("started_at"),
                    run.get("completed_at"),
                    run["seed"],
                    json.dumps(run["budgets"]),
                    run.get("matched_run_id"),
                    json.dumps(run.get("manifest")),
                    json.dumps(run.get("state")),
                    json.dumps(run.get("report")),
                    run.get("error"),
                ),
            )

    def update_run(self, run_id: str, **fields: Any) -> None:
        if not fields:
            return
        assignments = []
        values: list[Any] = []
        for key, value in fields.items():
            column = key
            if key in {"budgets", "manifest", "state", "report"}:
                column = f"{key}_json"
                value = json.dumps(value)
            assignments.append(f"{column} = ?")
            values.append(value)
        values.append(run_id)
        with self._lock, self._connect() as conn:
            conn.execute(f"UPDATE runs SET {', '.join(assignments)} WHERE id = ?", values)

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
        return self._run_row(row) if row else None

    def list_runs(self) -> list[dict[str, Any]]:
        with self._lock, self._connect() as conn:
            rows = conn.execute("SELECT * FROM runs ORDER BY created_at DESC").fetchall()
        return [self._run_row(row) for row in rows]

    def list_completed_condition(self, condition: str) -> list[dict[str, Any]]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM runs WHERE condition = ? AND status = 'completed' ORDER BY created_at DESC",
                (condition,),
            ).fetchall()
        return [self._run_row(row) for row in rows]

    def _run_row(self, row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": row["id"],
            "dataset_id": row["dataset_id"],
            "condition": row["condition"],
            "status": row["status"],
            "created_at": row["created_at"],
            "started_at": row["started_at"],
            "completed_at": row["completed_at"],
            "seed": row["seed"],
            "budgets": json.loads(row["budgets_json"]),
            "matched_run_id": row["matched_run_id"],
            "manifest": json.loads(row["manifest_json"]) if row["manifest_json"] else None,
            "state": json.loads(row["state_json"]) if row["state_json"] else None,
            "report": json.loads(row["report_json"]) if row["report_json"] else None,
            "error": row["error"],
        }

    def next_sequence(self, run_id: str) -> int:
        with self._lock, self._connect() as conn:
            row = conn.execute(
                "SELECT COALESCE(MAX(sequence), -1) AS seq FROM events WHERE run_id = ?",
                (run_id,),
            ).fetchone()
        return int(row["seq"]) + 1

    def append_event(self, event: dict[str, Any]) -> dict[str, Any]:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO events (run_id, sequence, timestamp, kind, service, stage, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event["run_id"],
                    event["sequence"],
                    event["timestamp"],
                    event["kind"],
                    event["service"],
                    event.get("stage"),
                    json.dumps(event.get("payload") or {}),
                ),
            )
        return event

    def list_events(self, run_id: str, after: int = -1) -> list[dict[str, Any]]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                """
                SELECT run_id, sequence, timestamp, kind, service, stage, payload_json
                FROM events WHERE run_id = ? AND sequence > ? ORDER BY sequence ASC
                """,
                (run_id, after),
            ).fetchall()
        return [
            {
                "run_id": row["run_id"],
                "sequence": row["sequence"],
                "timestamp": row["timestamp"],
                "kind": row["kind"],
                "service": row["service"],
                "stage": row["stage"],
                "payload": json.loads(row["payload_json"]),
            }
            for row in rows
        ]
