from __future__ import annotations

import asyncio
import json
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import FileResponse, PlainTextResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from .bus import EventBus
from .codegen import generate_experiment
from .conditions import CONDITIONS, architecture_view, condition_ids, get_condition
from .experiment_report import summarize_run, write_report
from .llm import PROVIDERS, PROVIDER_INDEX, probe_ollama
from .orchestrator import Orchestrator, config_digest, dataset_passport, validate_pack
from .packs import DATA_KINDS, empty_pack, merge_part, packs_present, part_errors
from .store import DATA_DIR, ROOT, Store, utcnow

FRONTEND = ROOT / "frontend"
SAMPLE = DATA_DIR / "sample_incident.json"

store = Store()
bus = EventBus(store)
orchestrator = Orchestrator(store, bus)
TASKS: set = set()
SUITE: dict[str, Any] = {"status": "idle", "runs": []}
SUITE_CONDITIONS = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7"]


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


def _prefer_ollama() -> None:
    status = probe_ollama(store.get_setting("ollama_base_url", "http://127.0.0.1:11434"))
    if not status["ok"] or not status["models"]:
        return
    preferred = "llama3.2:1b" if "llama3.2:1b" in status["models"] else status["models"][0]
    store.set_setting("provider", "ollama")
    store.set_setting("model", preferred)
    store.set_setting("ollama_models", status["models"])


@asynccontextmanager
async def lifespan(_app: FastAPI):
    _seed_sample()
    _prefer_ollama()
    yield


app = FastAPI(title="C0–C7 Investigation Lab", version="0.2.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")


def _configured_providers() -> list[str]:
    names = ["reference", "ollama"]
    for item in store.list_secret_public():
        if item["configured"] and item["provider"] not in names:
            names.append(item["provider"])
    return names


def _architecture(condition: str, provider: str | None = None, dataset_id: str | None = None) -> dict[str, Any]:
    pack = None
    if dataset_id:
        dataset = store.get_dataset(dataset_id)
        pack = dataset["pack"] if dataset else None
    return architecture_view(
        condition,
        provider=provider or store.get_setting("provider", "reference"),
        configured_providers=_configured_providers(),
        packs_present=packs_present(pack),
    )


async def _read_json_upload(request: Request, file: UploadFile | None) -> Any:
    if file is not None:
        raw = await file.read()
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise HTTPException(400, f"invalid JSON: {exc}") from exc
    return await request.json()


def _public_dataset(dataset: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in dataset.items() if k != "pack"} | {"passport": dataset_passport(dataset["pack"])}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND / "index.html")


@app.get("/api/health")
def health() -> dict[str, Any]:
    ollama = probe_ollama(store.get_setting("ollama_base_url", "http://127.0.0.1:11434"))
    return {
        "status": "ok",
        "ollama": ollama,
        "provider": store.get_setting("provider", "reference"),
        "model": store.get_setting("model"),
    }


@app.get("/api/conditions")
def list_conditions() -> dict[str, Any]:
    return {
        "conditions": [
            {"id": cid, **{k: v for k, v in get_condition(cid).items() if k != "capabilities"}}
            | {"capabilities": get_condition(cid)["capabilities"]}
            for cid in condition_ids()
        ]
    }


@app.get("/api/providers")
def list_providers() -> dict[str, Any]:
    secrets = {item["provider"]: item for item in store.list_secret_public()}
    ollama_url = store.get_setting("ollama_base_url", "http://127.0.0.1:11434")
    ollama = probe_ollama(ollama_url)
    providers = []
    for meta in PROVIDERS:
        public = secrets.get(meta["id"])
        entry = {
            **meta,
            "configured": (not meta["needs_key"]) or bool(public and public["configured"]),
            "hint": None if not meta["needs_key"] else (public or {}).get("hint"),
            "base_url": ollama_url if meta["id"] == "ollama" else (public or {}).get("base_url"),
        }
        if meta["id"] == "ollama" and ollama["models"]:
            entry["models"] = ollama["models"]
            entry["online"] = ollama["ok"]
        providers.append(entry)
    selected_provider = store.get_setting("provider", "ollama" if ollama["ok"] else "reference")
    selected_model = store.get_setting("model") or (
        "llama3.2:1b" if selected_provider == "ollama" else PROVIDER_INDEX[selected_provider]["default_model"]
    )
    return {
        "providers": providers,
        "selected": {
            "provider": selected_provider,
            "model": selected_model,
            "ollama_base_url": ollama_url,
        },
        "ollama": ollama,
        "data_kinds": DATA_KINDS,
    }


@app.post("/api/providers/select")
async def select_provider(payload: dict[str, Any]) -> dict[str, Any]:
    provider = payload.get("provider") or "reference"
    if provider not in PROVIDER_INDEX:
        raise HTTPException(400, f"unknown provider {provider}")
    model = payload.get("model") or PROVIDER_INDEX[provider]["default_model"]
    store.set_setting("provider", provider)
    store.set_setting("model", model)
    if provider == "ollama" and payload.get("base_url"):
        store.set_setting("ollama_base_url", payload["base_url"])
        store.upsert_secret("ollama", "", {"base_url": payload["base_url"]})
    return {"provider": provider, "model": model}


@app.post("/api/secrets")
async def save_secret(payload: dict[str, Any]) -> dict[str, Any]:
    provider = payload.get("provider")
    if provider not in PROVIDER_INDEX or provider == "reference":
        raise HTTPException(400, "provider must be a cloud connector or ollama")
    key = (payload.get("api_key") or "").strip()
    extra = {}
    if payload.get("base_url"):
        extra["base_url"] = payload["base_url"]
    if PROVIDER_INDEX[provider]["needs_key"] and not key:
        existing = store.get_secret(provider)
        if not existing:
            raise HTTPException(400, f"{provider} requires an API key")
        key = existing["api_key"]
    store.upsert_secret(provider, key, extra)
    if provider == "ollama" and extra.get("base_url"):
        store.set_setting("ollama_base_url", extra["base_url"])
    return {"status": "saved", "provider": provider, "hint": f"••••{key[-4:]}" if len(key) >= 4 else "saved"}


@app.delete("/api/secrets/{provider}")
def delete_secret(provider: str) -> dict[str, str]:
    store.delete_secret(provider)
    return {"status": "deleted", "provider": provider}


@app.get("/api/architecture")
def get_architecture(
    condition: str = "C3",
    provider: str | None = None,
    dataset_id: str | None = None,
) -> dict[str, Any]:
    if condition not in CONDITIONS:
        raise HTTPException(404, f"unknown condition {condition}")
    return _architecture(condition, provider, dataset_id)


@app.get("/api/datasets")
def list_datasets() -> dict[str, Any]:
    return {"datasets": [_public_dataset(item) for item in store.list_datasets()]}


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
        **_public_dataset(dataset),
        "preview": preview,
        "alert": pack.get("alert"),
        "scope": pack.get("scope"),
        "fixed_query_pack": pack.get("fixed_query_pack"),
        "oracle_plan": pack.get("oracle_plan"),
        "oracle_evidence": pack.get("oracle_evidence"),
        "has_knowledge_corpus": bool(pack.get("knowledge_corpus")),
        "has_ground_truth": bool(pack.get("ground_truth")),
        "packs_present": packs_present(pack),
    }


@app.post("/api/datasets")
async def upload_dataset(request: Request, file: UploadFile | None = File(default=None)) -> dict[str, Any]:
    pack = await _read_json_upload(request, file)
    if file is not None:
        name = Path(file.filename or pack.get("incident_id") or "uploaded-incident").stem
    else:
        name = pack.get("name") or pack.get("incident_id") or "uploaded-incident"
    errors = validate_pack(pack)
    if errors:
        raise HTTPException(400, {"errors": errors})
    dataset_id = f"ds-{uuid.uuid4().hex[:10]}"
    store.insert_dataset(
        {
            "id": dataset_id,
            "name": pack.get("name") or name,
            "incident_id": pack["incident_id"],
            "created_at": utcnow(),
            "pack": pack,
        }
    )
    return _public_dataset(store.get_dataset(dataset_id))


@app.post("/api/datasets/parts/{kind}")
async def upload_part(
    kind: str,
    request: Request,
    file: UploadFile | None = File(default=None),
    dataset_id: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = await _read_json_upload(request, file)
    errors = part_errors(kind, payload)
    if errors:
        raise HTTPException(400, {"errors": errors})
    if dataset_id:
        dataset = store.get_dataset(dataset_id)
        if not dataset:
            raise HTTPException(404, "dataset not found")
        pack = merge_part(dataset["pack"], kind, payload)
        name = pack.get("name") or dataset["name"]
        store.update_dataset_pack(dataset_id, pack, name=name)
    else:
        pack = merge_part(empty_pack(), kind, payload)
        if isinstance(payload, dict) and payload.get("incident_id"):
            pack["incident_id"] = payload["incident_id"]
        dataset_id = f"ds-{uuid.uuid4().hex[:10]}"
        store.insert_dataset(
            {
                "id": dataset_id,
                "name": pack.get("name") or pack["incident_id"],
                "incident_id": pack["incident_id"],
                "created_at": utcnow(),
                "pack": pack,
            }
        )
    return _public_dataset(store.get_dataset(dataset_id))


@app.get("/api/runs")
def list_runs() -> dict[str, Any]:
    return {"runs": [_public_run(run) for run in store.list_runs()]}


@app.get("/api/runs/c3")
def list_c3_runs() -> dict[str, Any]:
    return {"runs": [_public_run(run) for run in store.list_completed_condition("C3")]}


@app.post("/api/experiments/generate")
async def generate_experiment_code(payload: dict[str, Any]) -> dict[str, Any]:
    condition = payload.get("condition") or "C3"
    if condition not in CONDITIONS:
        raise HTTPException(400, "unknown condition")
    dataset_id = payload.get("dataset_id")
    if not store.get_dataset(dataset_id or ""):
        raise HTTPException(404, "dataset not found")
    spec = {
        "condition": condition,
        "dataset_id": dataset_id,
        "provider": payload.get("provider") or store.get_setting("provider", "reference"),
        "model": payload.get("model") or store.get_setting("model", "reference-investigator-v1"),
        "budgets": payload.get("budgets") or {},
        "matched_run_id": payload.get("matched_run_id"),
        "seed": payload.get("seed") or 42,
        "lab_url": payload.get("lab_url") or "http://127.0.0.1:8000",
    }
    generated = generate_experiment(spec)
    generated["architecture"] = _architecture(condition, spec["provider"], dataset_id)
    return generated


@app.get("/api/experiments/generate.py")
def download_experiment(
    condition: str = "C3",
    dataset_id: str = "",
    provider: str = "reference",
    model: str = "reference-investigator-v1",
    matched_run_id: str | None = None,
) -> PlainTextResponse:
    if not store.get_dataset(dataset_id):
        raise HTTPException(404, "dataset not found")
    generated = generate_experiment(
        {
            "condition": condition,
            "dataset_id": dataset_id,
            "provider": provider,
            "model": model,
            "matched_run_id": matched_run_id,
        }
    )
    return PlainTextResponse(
        generated["python"],
        media_type="text/x-python",
        headers={"Content-Disposition": f'attachment; filename="{generated["filename"]}"'},
    )


def _prepare_run(payload: dict[str, Any]) -> dict[str, Any]:
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

    provider = payload.get("provider") or store.get_setting("provider", "ollama")
    if provider not in PROVIDER_INDEX:
        raise HTTPException(400, f"unknown provider {provider}")
    model_name = payload.get("model") or store.get_setting("model") or PROVIDER_INDEX[provider]["default_model"]
    if PROVIDER_INDEX[provider]["needs_key"]:
        secret = store.get_secret(provider)
        if not secret or not secret.get("api_key"):
            raise HTTPException(400, f"Save an API key for {provider} before running.")
    if provider == "ollama":
        status = probe_ollama(store.get_setting("ollama_base_url", "http://127.0.0.1:11434"))
        if not status["ok"]:
            raise HTTPException(503, f"Ollama is not reachable: {status.get('error')}")
        if status["models"] and model_name not in status["models"] and f"{model_name}:latest" not in status["models"]:
            raise HTTPException(400, f"Ollama does not have model {model_name}. Pulled: {status['models']}")

    default_tools = 6 if provider == "ollama" else 12
    budgets = {
        "max_tool_calls": int((payload.get("budgets") or {}).get("max_tool_calls", default_tools)),
        "max_records_per_call": int((payload.get("budgets") or {}).get("max_records_per_call", 100)),
        "max_runtime_seconds": int((payload.get("budgets") or {}).get("max_runtime_seconds", 300)),
        "max_model_tokens": int((payload.get("budgets") or {}).get("max_model_tokens", 32000)),
    }
    run_id = payload.get("run_id") or f"run-{uuid.uuid4().hex[:12]}"
    seed = int(payload.get("seed") or 42)
    model_profile = {"provider": provider, "model": model_name}
    manifest = {
        "schema_version": "1.0",
        "run_id": run_id,
        "incident_id": dataset["incident_id"],
        "condition_id": condition,
        "dataset_id": dataset_id,
        "seed": seed,
        "model": model_profile,
        "model_profile": f"{provider}:{model_name}",
        "service_manifest": {
            "investigation_api": "0.3.0",
            "condition_controller": "0.3.0",
            "model_gateway": f"{provider}:{model_name}",
            "knowledge_service": "kb-2026-07-01" if profile["knowledge"]["enabled"] else None,
            "agent_orchestrator": "0.3.0" if profile["capabilities"]["adaptive_loop"] else None,
            "state_service": "0.3.0" if profile["state"]["enabled"] else None,
            "telemetry_gateway": "0.3.0" if profile["search"]["enabled"] else None,
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
    return record


@app.post("/api/runs")
async def create_run(payload: dict[str, Any]) -> dict[str, Any]:
    record = _prepare_run(payload)
    task = asyncio.create_task(orchestrator.run(record["id"]))
    TASKS.add(task)
    task.add_done_callback(TASKS.discard)
    return _public_run(store.get_run(record["id"]))


async def _run_suite(payload: dict[str, Any]) -> dict[str, Any]:
    dataset_id = payload["dataset_id"]
    dataset = store.get_dataset(dataset_id)
    conditions = payload.get("conditions") or list(SUITE_CONDITIONS)
    provider = payload.get("provider") or store.get_setting("provider", "ollama")
    model_name = payload.get("model") or store.get_setting("model")
    summaries: list[dict[str, Any]] = []
    c3_id = None
    SUITE.update(
        {
            "status": "running",
            "dataset_id": dataset_id,
            "incident_id": dataset["incident_id"],
            "provider": provider,
            "model": model_name,
            "current": None,
            "runs": summaries,
            "error": None,
            "started_at": utcnow(),
        }
    )
    try:
        for condition in conditions:
            request = {
                "dataset_id": dataset_id,
                "condition": condition,
                "provider": provider,
                "model": model_name,
                "budgets": payload.get("budgets") or {},
                "seed": payload.get("seed") or 42,
            }
            if condition == "C5":
                if not c3_id:
                    summary = {
                        "condition": "C5",
                        "status": "skipped",
                        "error": "C5 skipped; no completed C3 run in this suite.",
                    }
                    summaries.append(summary)
                    continue
                request["matched_run_id"] = c3_id
            record = _prepare_run(request)
            SUITE["current"] = {"condition": condition, "run_id": record["id"]}
            await orchestrator.run(record["id"])
            run = store.get_run(record["id"])
            summary = summarize_run(run, store.list_events(record["id"]))
            summaries.append(summary)
            if condition == "C3" and run and run["status"] == "completed":
                c3_id = run["id"]
        suite = {
            "generated_at": utcnow(),
            "dataset_id": dataset_id,
            "incident_id": dataset["incident_id"],
            "provider": provider,
            "model": model_name,
            "runs": summaries,
        }
        paths = write_report(suite)
        suite["files"] = paths
        SUITE.update({"status": "completed", "current": None, **suite})
        return dict(SUITE)
    except Exception as exc:  # noqa: BLE001
        SUITE.update({"status": "failed", "error": str(exc), "completed_at": utcnow()})
        raise


@app.post("/api/experiments/suite")
async def run_suite(payload: dict[str, Any]) -> dict[str, Any]:
    dataset_id = payload.get("dataset_id")
    dataset = store.get_dataset(dataset_id or "")
    if not dataset:
        raise HTTPException(404, "dataset not found")
    if SUITE.get("status") == "running":
        raise HTTPException(409, "A suite is already running")
    if payload.get("wait"):
        return await _run_suite(payload)
    task = asyncio.create_task(_run_suite(payload))
    TASKS.add(task)
    task.add_done_callback(TASKS.discard)
    return {
        "status": "running",
        "dataset_id": dataset_id,
        "provider": payload.get("provider"),
        "model": payload.get("model"),
    }


@app.get("/api/experiments/suite")
def suite_status() -> dict[str, Any]:
    return dict(SUITE)


@app.get("/api/experiments/report")
def latest_report() -> dict[str, Any]:
    path = ROOT / "reports" / "experiment-report.json"
    if not path.exists():
        raise HTTPException(404, "No experiment report yet. Run the C0–C7 suite.")
    return json.loads(path.read_text())


@app.get("/api/experiments/report.md")
def latest_report_markdown() -> FileResponse:
    path = ROOT / "reports" / "experiment-report.md"
    if not path.exists():
        raise HTTPException(404, "No experiment report yet. Run the C0–C7 suite.")
    return FileResponse(path, media_type="text/markdown", filename="experiment-report.md")


@app.get("/api/runs/{run_id}")
def get_run(run_id: str) -> dict[str, Any]:
    run = store.get_run(run_id)
    if not run:
        raise HTTPException(404, "run not found")
    dataset = store.get_dataset(run["dataset_id"])
    provider = ((run.get("manifest") or {}).get("model") or {}).get("provider")
    return {
        **_public_run(run),
        "architecture": _architecture(run["condition"], provider, run["dataset_id"]),
        "dataset": _public_dataset(dataset) if dataset else None,
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
