from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from .bus import EventBus
from .conditions import CONDITIONS, architecture_view, condition_ids, get_condition
from .orchestrator import Orchestrator, config_digest, dataset_passport, validate_pack
from .store import DATA_DIR, ROOT, Store, utcnow

FRONTEND = ROOT / "frontend"
SAMPLE = DATA_DIR / "sample_incident.json"

store = Store()
bus = EventBus(store)
orchestrator = Orchestrator(store, bus)
TASKS: set = set()

app = FastAPI(title="C0–C7 Investigation Lab", version="0.1.0")
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")


def _seed_sample() -> None:
    if store.list_datasets():
        return
    pack = json.loads(SAMPLE.read_text())
    store.insert_dataset(
        {
            "id": "ds-sample-0042",
            "name": pack.get("name") or pack["incident_id"],
            "incident_id": pack["incident_id"],
            "created_at": utcnow(),
            "pack": pack,
        }
    )


@app.on_event("startup")
def startup() -> None:
    _seed_sample()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND / "index.html")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/conditions")
def list_conditions() -> dict[str, Any]:
    return {
        "conditions": [
            {"id": cid, **{k: v for k, v in get_condition(cid).items() if k != "capabilities"}}
            | {"capabilities": get_condition(cid)["capabilities"]}
            for cid in condition_ids()
        ]
    }


@app.get("/api/architecture")
def get_architecture(condition: str = "C3") -> dict[str, Any]:
    if condition not in CONDITIONS:
        raise HTTPException(404, f"unknown condition {condition}")
    return architecture_view(condition)


@app.get("/api/datasets")
def list_datasets() -> dict[str, Any]:
    datasets = []
    for item in store.list_datasets():
        datasets.append({k: v for k, v in item.items() if k != "pack"} | {"passport": dataset_passport(item["pack"])})
    return {"datasets": datasets}


@app.get("/api/datasets/{dataset_id}")
def get_dataset(dataset_id: str) -> dict[str, Any]:
    dataset = store.get_dataset(dataset_id)
    if not dataset:
        raise HTTPException(404, "dataset not found")
    pack = dataset["pack"]
    preview = {}
    for source, items in (pack.get("telemetry") or {}).items():
        preview[source] = (items or [])[:5]
    return {
        **{k: v for k, v in dataset.items() if k != "pack"},
        "passport": dataset_passport(pack),
        "preview": preview,
        "alert": pack.get("alert"),
        "scope": pack.get("scope"),
        "fixed_query_pack": pack.get("fixed_query_pack"),
        "oracle_plan": pack.get("oracle_plan"),
        "oracle_evidence": pack.get("oracle_evidence"),
    }


@app.post("/api/datasets")
async def upload_dataset(request: Request, file: UploadFile | None = File(default=None)) -> dict[str, Any]:
    if file is not None:
        raw = await file.read()
        try:
            pack = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise HTTPException(400, f"invalid JSON: {exc}") from exc
        name = Path(file.filename or pack.get("incident_id") or "uploaded-incident").stem
    else:
        pack = await request.json()
        name = pack.get("name") or pack.get("incident_id") or "uploaded-incident"
    errors = validate_pack(pack)
    if errors:
        raise HTTPException(400, {"errors": errors})
    dataset_id = f"ds-{uuid.uuid4().hex[:10]}"
    record = {
        "id": dataset_id,
        "name": pack.get("name") or name,
        "incident_id": pack["incident_id"],
        "created_at": utcnow(),
        "pack": pack,
    }
    store.insert_dataset(record)
    dataset = store.get_dataset(dataset_id)
    return {k: v for k, v in dataset.items() if k != "pack"} | {"passport": dataset_passport(pack)}


@app.get("/api/runs")
def list_runs() -> dict[str, Any]:
    runs = []
    for run in store.list_runs():
        runs.append(_public_run(run))
    return {"runs": runs}


@app.get("/api/runs/c3")
def list_c3_runs() -> dict[str, Any]:
    return {"runs": [_public_run(run) for run in store.list_completed_condition("C3")]}


@app.post("/api/runs")
async def create_run(payload: dict[str, Any]) -> dict[str, Any]:
    condition = payload.get("condition")
    dataset_id = payload.get("dataset_id")
    if condition not in CONDITIONS:
        raise HTTPException(400, "condition must be one of C0–C7")
    dataset = store.get_dataset(dataset_id or "")
    if not dataset:
        raise HTTPException(404, "dataset not found")
    profile = get_condition(condition)
    matched_run_id = payload.get("matched_run_id")
    if profile["matched_run_required"]:
        matched = store.get_run(matched_run_id or "")
        if not matched or matched["condition"] != "C3" or matched["status"] != "completed":
            raise HTTPException(400, "C5 requires matched_run_id of a completed C3 run")
        events = store.list_events(matched["id"])
        has_evidence = any(
            event["kind"] == "tool_observation" and (event["payload"] or {}).get("records")
            for event in events
        )
        if not has_evidence:
            raise HTTPException(400, "Matched C3 run has zero evidence; C5 is not backfilled")
    elif matched_run_id:
        raise HTTPException(400, "matched_run_id is only valid for C5")

    budgets = {
        "max_tool_calls": int((payload.get("budgets") or {}).get("max_tool_calls", 12)),
        "max_records_per_call": int((payload.get("budgets") or {}).get("max_records_per_call", 100)),
        "max_runtime_seconds": int((payload.get("budgets") or {}).get("max_runtime_seconds", 300)),
        "max_model_tokens": int((payload.get("budgets") or {}).get("max_model_tokens", 32000)),
    }
    run_id = payload.get("run_id") or f"run-{uuid.uuid4().hex[:12]}"
    seed = int(payload.get("seed") or 42)
    manifest = {
        "schema_version": "1.0",
        "run_id": run_id,
        "incident_id": dataset["incident_id"],
        "condition_id": condition,
        "dataset_id": dataset_id,
        "seed": seed,
        "model_profile": "reference-investigator-v1",
        "service_manifest": {
            "investigation_api": "0.1.0",
            "condition_controller": "0.1.0",
            "model_gateway": "reference-investigator-v1",
            "knowledge_service": "kb-2026-07-01" if profile["knowledge"]["enabled"] else None,
            "agent_orchestrator": "0.1.0" if profile["capabilities"]["adaptive_loop"] else None,
            "state_service": "0.1.0" if profile["state"]["enabled"] else None,
            "telemetry_gateway": "0.1.0" if profile["search"]["enabled"] else None,
        },
        "artifact_versions": {
            "output_schema": "report-1.0",
            "knowledge_index": "kb-2026-07-01",
            "tool_schema": "tools-1.0",
        },
        "allowed_interfaces": profile["allowed_interfaces"],
        "source_run": {"condition_id": "C3", "run_id": matched_run_id} if matched_run_id else None,
    }
    manifest["service_manifest_hash"] = config_digest(manifest["service_manifest"])
    record = {
        "id": run_id,
        "dataset_id": dataset_id,
        "condition": condition,
        "status": "queued",
        "created_at": utcnow(),
        "seed": seed,
        "budgets": budgets,
        "matched_run_id": matched_run_id,
        "manifest": manifest,
        "state": None,
        "report": None,
        "error": None,
    }
    store.insert_run(record)
    import asyncio

    task = asyncio.create_task(orchestrator.run(run_id))
    TASKS.add(task)
    task.add_done_callback(TASKS.discard)
    return _public_run(store.get_run(run_id))


@app.get("/api/runs/{run_id}")
def get_run(run_id: str) -> dict[str, Any]:
    run = store.get_run(run_id)
    if not run:
        raise HTTPException(404, "run not found")
    dataset = store.get_dataset(run["dataset_id"])
    return {
        **_public_run(run),
        "architecture": architecture_view(run["condition"]),
        "dataset": {k: v for k, v in dataset.items() if k != "pack"} if dataset else None,
        "events": store.list_events(run_id),
    }


@app.get("/api/runs/{run_id}/events")
def get_events(run_id: str, after: int = -1) -> dict[str, Any]:
    if not store.get_run(run_id):
        raise HTTPException(404, "run not found")
    return {"events": store.list_events(run_id, after=after)}


@app.get("/api/runs/{run_id}/stream")
async def stream_run(run_id: str) -> StreamingResponse:
    if not store.get_run(run_id):
        raise HTTPException(404, "run not found")

    async def gen():
        queue = await bus.subscribe(run_id)
        last = -1
        try:
            for event in store.list_events(run_id):
                last = event["sequence"]
                yield _sse(event)
            run = store.get_run(run_id)
            if run and run["status"] in {"completed", "failed"}:
                yield _sse({"kind": "eof", "run": _public_run(run)})
                return
            while True:
                event = await queue.get()
                seq = event.get("sequence")
                if isinstance(seq, int) and seq <= last:
                    continue
                if isinstance(seq, int):
                    last = seq
                yield _sse(event)
                if event["kind"] in {"run_completed", "run_failed"}:
                    yield _sse({"kind": "eof", "run": _public_run(store.get_run(run_id))})
                    break
        finally:
            await bus.unsubscribe(run_id, queue)

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
    )


def _public_run(run: dict[str, Any] | None) -> dict[str, Any]:
    if not run:
        return {}
    return {
        "id": run["id"],
        "dataset_id": run["dataset_id"],
        "condition": run["condition"],
        "status": run["status"],
        "created_at": run["created_at"],
        "started_at": run["started_at"],
        "completed_at": run["completed_at"],
        "seed": run["seed"],
        "budgets": run["budgets"],
        "matched_run_id": run["matched_run_id"],
        "manifest": run["manifest"],
        "state": run["state"],
        "report": run["report"],
        "error": run["error"],
    }


def _sse(payload: dict[str, Any]) -> str:
    return f"data: {json.dumps(payload)}\n\n"
