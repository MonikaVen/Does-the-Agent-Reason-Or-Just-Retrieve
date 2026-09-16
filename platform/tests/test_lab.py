from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.codegen import generate_experiment
from app.conditions import architecture_view, interface_enabled
from app.llm import extract_json
from app.experiment_report import render_markdown, summarize_run
from app.orchestrator import Orchestrator, validate_pack
from app.packs import merge_part, empty_pack, packs_present
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
    assert "adapter-ollama" in enabled
    assert "adapter-openai" in enabled


def test_typed_upload_and_sealed_ground_truth():
    pack = empty_pack()
    pack = merge_part(pack, "alert", {"host": "workstation-17", "summary": "ps"})
    pack = merge_part(pack, "telemetry", {"process_events": [{"event_id": "e1", "host": "workstation-17"}]})
    pack = merge_part(pack, "knowledge", {"passages": [{"passage_id": "k1", "text": "guidance", "category": "detection", "source_id": "s", "source_version": "1", "corpus_tags": []}]})
    pack = merge_part(pack, "ground_truth", {"verdict": "malicious"})
    present = packs_present(pack)
    assert present["alert"] and present["telemetry"] and present["knowledge"] and present["ground_truth"]


def test_extract_json_from_fence():
    data = extract_json("noise ```json\n{\"verdict\": \"benign\"}\n```")
    assert data["verdict"] == "benign"
    trailing = extract_json('{"verdict": "malicious", "confidence": 0.4} trailing text')
    assert trailing["verdict"] == "malicious"


def test_secrets_are_masked(tmp_path):
    store = Store(tmp_path / "lab.sqlite3")
    store.upsert_secret("openai", "sk-test-secret-key", {})
    public = store.list_secret_public()
    assert public[0]["hint"] == "••••-key"
    assert "sk-test-secret" not in json.dumps(public)


def test_generated_experiment_pins_condition():
    generated = generate_experiment(
        {
            "condition": "C3",
            "dataset_id": "ds-1",
            "provider": "openai",
            "model": "gpt-4.1-mini",
        }
    )
    assert "C3" in generated["python"]
    assert "openai" in generated["python"]
    assert generated["filename"] == "experiment_c3_openai.py"


def test_policy_rejects_disabled_tool():
    policy = PolicyEngine("C1", SAMPLE, 100)
    decision = policy.validate({"tool": "query_events", "arguments": {"source": "process_events"}, "action_id": "a-1"})
    assert decision["decision"] == "reject"
    assert decision["error"]["error_code"] == "SERVICE_DISABLED"


def test_architecture_marks_selected_provider():
    view = architecture_view("C3", provider="groq", configured_providers=["groq"])
    adapters = {svc["id"]: svc for plane in view["planes"] for svc in plane["services"]}
    assert adapters["adapter-groq"]["selected"] is True
    assert adapters["adapter-openai"]["selected"] is False


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
                "manifest": {"model": {"provider": "reference", "model": "reference-investigator-v1"}},
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


def test_experiment_report_markdown():
    suite = {
        "generated_at": "2026-09-16T19:00:00Z",
        "incident_id": "incident-0042",
        "provider": "ollama",
        "model": "llama3.2:1b",
        "dataset_id": "ds-sample-0042",
        "runs": [
            {
                "condition": "C0",
                "status": "completed",
                "verdict": "inconclusive",
                "confidence": 0.4,
                "evidence_ids": [],
                "tool_observations": 0,
                "knowledge_retrievals": 0,
                "summary": "Alert only.",
                "tools": [],
            },
            {
                "condition": "C5",
                "status": "skipped",
                "error": "C5 skipped; no completed C3 run in this suite.",
            },
        ],
    }
    markdown = render_markdown(suite)
    assert "ollama:llama3.2:1b" in markdown
    assert "| C0 |" in markdown
    assert "C5 skipped" in markdown
    summary = summarize_run(
        {
            "id": "run-1",
            "condition": "C3",
            "status": "completed",
            "report": {"verdict": "malicious", "confidence": 0.9, "summary": "ps", "supporting_evidence": [{"event_id": "event-1021"}]},
            "manifest": {"model_profile": "ollama:llama3.2:1b"},
        },
        [{"kind": "tool_observation", "payload": {"tool": "query_events"}}, {"kind": "knowledge_retrieved", "payload": {}}],
    )
    assert summary["tool_observations"] == 1
    assert summary["knowledge_retrievals"] == 1
    assert summary["evidence_ids"] == ["event-1021"]
