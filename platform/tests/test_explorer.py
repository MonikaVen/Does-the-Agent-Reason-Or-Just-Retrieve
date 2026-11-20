from __future__ import annotations

import json
import threading
from urllib.request import urlopen

from app.artifacts import ArtifactError, list_packs, list_suites, run_detail
from app.explorer import serve
from app.store import Store


def _suite(tmp_path):
    reports = tmp_path / "reports"
    suite = reports / "demo"
    (suite / "packs").mkdir(parents=True)
    (suite / "packs" / "inc-saved.json").write_text(
        json.dumps(
            {
                "incident_id": "inc-saved",
                "dataset": "SOC-AgentBench",
                "provider": "ollama",
                "model": "qwen2.5:14b",
                "completed": 1,
                "failed": 0,
                "skipped": 0,
                "runs": [
                    {
                        "condition": "C0",
                        "status": "completed",
                        "verdict": "benign",
                        "confidence": 0.4,
                        "tool_observations": 0,
                        "knowledge_retrievals": 0,
                        "run_id": "run-saved",
                    }
                ],
            }
        )
    )
    (suite / "packs" / "inc-bad.error.json").write_text(
        json.dumps({"incident_id": "inc-bad", "error": "boom"})
    )
    store = Store(suite / "lab-w1.sqlite3")
    store.insert_dataset(
        {
            "id": "ds1",
            "name": "live",
            "incident_id": "inc-live",
            "created_at": "2026-01-01T00:00:00Z",
            "pack": {"incident_id": "inc-live", "alert": {}, "telemetry": {}},
        }
    )
    store.insert_run(
        {
            "id": "run-live",
            "dataset_id": "ds1",
            "condition": "C3",
            "status": "running",
            "created_at": "2026-01-01T00:00:00Z",
            "started_at": "2026-01-01T00:00:01Z",
            "completed_at": None,
            "seed": 1,
            "budgets": {"max_tool_calls": 2},
            "manifest": {"incident_id": "inc-live", "model_profile": "ollama:qwen2.5:14b"},
            "state": {"hypotheses": []},
            "report": None,
            "error": None,
        }
    )
    store.append_event(
        {
            "run_id": "run-live",
            "sequence": 0,
            "timestamp": "2026-01-01T00:00:02Z",
            "kind": "decision",
            "service": "model-gateway",
            "stage": "generate_decision",
            "payload": {"stop": False, "blob": "x" * 7000},
        }
    )
    return reports


def test_suite_catalog_merges_pack_files_and_open_runs(tmp_path):
    reports = _suite(tmp_path)
    (reports / "empty-notes").mkdir()
    suites = list_suites(reports)
    assert [item["name"] for item in suites] == ["demo"]
    catalog = list_packs("demo", reports)
    ids = [pack["incident_id"] for pack in catalog["packs"]]
    assert ids == ["inc-bad", "inc-live", "inc-saved"]
    saved = next(pack for pack in catalog["packs"] if pack["incident_id"] == "inc-saved")
    assert saved["runs"][0]["verdict"] == "benign"
    assert saved["model"] == "qwen2.5:14b"
    assert catalog["running_incident"] == "inc-live"
    bad = next(pack for pack in catalog["packs"] if pack["incident_id"] == "inc-bad")
    assert bad["pack_error"] == "boom"


def test_run_detail_truncates_payload_and_rejects_escape(tmp_path):
    reports = _suite(tmp_path)
    detail = run_detail("demo", "run-live", reports)
    assert detail["condition"] == "C3"
    assert detail["events"][0]["truncated"] is True
    assert detail["events"][0]["payload"]["truncated"] is True
    try:
        list_packs("../secrets", reports)
    except ArtifactError:
        return
    raise AssertionError("path escape was accepted")


def test_http_lists_suites(tmp_path):
    reports = _suite(tmp_path)
    server = serve("127.0.0.1", 0, reports)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        with urlopen(f"http://127.0.0.1:{port}/api/suites") as response:
            body = json.loads(response.read().decode())
        assert body["suites"][0]["name"] == "demo"
        with urlopen(f"http://127.0.0.1:{port}/") as response:
            page = response.read().decode()
        assert "Artifact explorer" in page
    finally:
        server.shutdown()
        server.server_close()
