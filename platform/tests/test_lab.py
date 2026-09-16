from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.conditions import architecture_view, interface_enabled
from app.orchestrator import Orchestrator, validate_pack
from app.policy import PolicyEngine
from app.store import Store
from app.bus import EventBus


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = json.loads((ROOT / "data" / "sample_incident.json").read_text())


def test_pack_requires_stable_ids():
    errors = validate_pack({"incident_id": "x", "alert": {"host": "h"}, "telemetry": {"process_events": [{}]}})
    assert any("event_id" in item for item in errors)


def test_c0_cannot_search():
    assert not interface_enabled("C0", "query_events")
    assert not interface_enabled("C1", "find_process_tree")
    assert interface_enabled("C3", "retrieve_knowledge")
    assert not interface_enabled("C2", "retrieve_knowledge")
    view = architecture_view("C0")
    enabled = {svc["id"]: svc["enabled"] for plane in view["planes"] for svc in plane["services"]}
    assert enabled["knowledge-service"] is False
    assert enabled["telemetry-gateway"] is False
    assert enabled["model-gateway"] is True


def test_policy_rejects_disabled_tool():
    policy = PolicyEngine("C1", SAMPLE, 100)
    decision = policy.validate({"tool": "query_events", "arguments": {"source": "process_events"}, "action_id": "a-1"})
    assert decision["decision"] == "reject"
    assert decision["error"]["error_code"] == "SERVICE_DISABLED"


@pytest.mark.asyncio
async def test_c0_and_c3_runs(tmp_path, monkeypatch):
    monkeypatch.setattr("app.orchestrator.STEP_DELAY", 0)
    store = Store(tmp_path / "lab.sqlite3")
    bus = EventBus(store)
    orch = Orchestrator(store, bus)
    store.insert_dataset(
        {
            "id": "ds-1",
            "name": SAMPLE["name"],
            "incident_id": SAMPLE["incident_id"],
            "created_at": "2026-07-10T14:00:00Z",
            "pack": SAMPLE,
        }
    )
    for condition, run_id in (("C0", "run-c0"), ("C3", "run-c3")):
        store.insert_run(
            {
                "id": run_id,
                "dataset_id": "ds-1",
                "condition": condition,
                "status": "queued",
                "created_at": "2026-07-10T14:00:00Z",
                "seed": 42,
                "budgets": {
                    "max_tool_calls": 8,
                    "max_records_per_call": 50,
                    "max_runtime_seconds": 60,
                    "max_model_tokens": 8000,
                },
                "matched_run_id": None,
                "manifest": {},
            }
        )
        await orch.run(run_id)
        run = store.get_run(run_id)
        assert run["status"] == "completed"
        assert run["report"]["verdict"] in {"malicious", "benign", "inconclusive"}
        kinds = [event["kind"] for event in store.list_events(run_id)]
        assert "report_validated" in kinds
        if condition == "C3":
            assert "tool_observation" in kinds
            assert run["state"]["known_evidence"]
        if condition == "C0":
            assert "tool_observation" not in kinds
