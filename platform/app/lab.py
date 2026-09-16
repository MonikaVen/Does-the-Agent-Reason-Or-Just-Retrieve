from __future__ import annotations

import json
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .bus import EventBus
from .conditions import CONDITIONS, architecture_view, get_condition
from .experiment_report import summarize_run, write_report
from .llm import PROVIDER_INDEX, probe_ollama
from .orchestrator import Orchestrator, config_digest, validate_pack
from .packs import empty_pack, merge_part, packs_present, part_errors
from .store import DATA_DIR, Store, utcnow

SAMPLE = DATA_DIR / "sample_incident.json"
SUITE_CONDITIONS = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7"]


class LabError(RuntimeError):
    pass


class Lab:
    def __init__(self, db_path: Path | None = None, on_event: Callable[[dict[str, Any]], None] | None = None) -> None:
        self.store = Store(db_path)
        self.bus = EventBus(self.store, on_event=on_event)
        self.orchestrator = Orchestrator(self.store, self.bus)

    def seed_sample(self) -> dict[str, Any] | None:
        if self.store.list_datasets():
            return None
        return self.load_pack(json.loads(SAMPLE.read_text()), dataset_id="ds-sample-0042")

    def prefer_ollama(self) -> dict[str, Any]:
        status = probe_ollama(self.store.get_setting("ollama_base_url", "http://127.0.0.1:11434"))
        if status["ok"] and status["models"]:
            preferred = "llama3.2:1b" if "llama3.2:1b" in status["models"] else status["models"][0]
            self.store.set_setting("provider", "ollama")
            self.store.set_setting("model", preferred)
            self.store.set_setting("ollama_models", status["models"])
        return status

    def health(self) -> dict[str, Any]:
        ollama = probe_ollama(self.store.get_setting("ollama_base_url", "http://127.0.0.1:11434"))
        return {
            "ollama": ollama,
            "provider": self.store.get_setting("provider", "ollama" if ollama["ok"] else "reference"),
            "model": self.store.get_setting("model"),
            "datasets": len(self.store.list_datasets()),
            "runs": len(self.store.list_runs()),
        }

    def load_pack(self, pack: dict[str, Any], name: str | None = None, dataset_id: str | None = None) -> dict[str, Any]:
        errors = validate_pack(pack)
        if errors:
            raise LabError("; ".join(errors))
        dataset_id = dataset_id or f"ds-{uuid.uuid4().hex[:10]}"
        self.store.insert_dataset(
            {
                "id": dataset_id,
                "name": pack.get("name") or name or pack["incident_id"],
                "incident_id": pack["incident_id"],
                "created_at": utcnow(),
                "pack": pack,
            }
        )
        return self.store.get_dataset(dataset_id)

    def load_pack_file(self, path: str | Path) -> dict[str, Any]:
        file_path = Path(path)
        pack = json.loads(file_path.read_text())
        return self.load_pack(pack, name=file_path.stem)

    def merge_kind(self, kind: str, payload: Any, dataset_id: str | None = None) -> dict[str, Any]:
        errors = part_errors(kind, payload)
        if errors:
            raise LabError("; ".join(errors))
        if dataset_id:
            dataset = self.store.get_dataset(dataset_id)
            if not dataset:
                raise LabError(f"dataset {dataset_id} not found")
            pack = merge_part(dataset["pack"], kind, payload)
            name = pack.get("name") or dataset["name"]
            self.store.update_dataset_pack(dataset_id, pack, name=name)
        else:
            pack = merge_part(empty_pack(), kind, payload)
            if isinstance(payload, dict) and payload.get("incident_id"):
                pack["incident_id"] = payload["incident_id"]
            dataset_id = f"ds-{uuid.uuid4().hex[:10]}"
            self.store.insert_dataset(
                {
                    "id": dataset_id,
                    "name": pack.get("name") or pack["incident_id"],
                    "incident_id": pack["incident_id"],
                    "created_at": utcnow(),
                    "pack": pack,
                }
            )
        return self.store.get_dataset(dataset_id)

    def ensure_dataset(self, pack_path: str | Path | None = None, dataset_id: str | None = None) -> dict[str, Any]:
        if pack_path:
            return self.load_pack_file(pack_path)
        if dataset_id:
            dataset = self.store.get_dataset(dataset_id)
            if not dataset:
                raise LabError(f"dataset {dataset_id} not found")
            return dataset
        self.seed_sample()
        datasets = self.store.list_datasets()
        if not datasets:
            raise LabError("no dataset loaded")
        return datasets[0]

    def set_provider(self, provider: str, model: str | None = None, base_url: str | None = None) -> None:
        if provider not in PROVIDER_INDEX:
            raise LabError(f"unknown provider {provider}")
        self.store.set_setting("provider", provider)
        self.store.set_setting("model", model or PROVIDER_INDEX[provider]["default_model"])
        if provider == "ollama" and base_url:
            self.store.set_setting("ollama_base_url", base_url)
            self.store.upsert_secret("ollama", "", {"base_url": base_url})

    def set_secret(self, provider: str, api_key: str = "", base_url: str | None = None) -> None:
        if provider not in PROVIDER_INDEX or provider == "reference":
            raise LabError("provider must be a cloud connector or ollama")
        extra = {}
        if base_url:
            extra["base_url"] = base_url
        key = api_key.strip()
        if PROVIDER_INDEX[provider]["needs_key"] and not key:
            existing = self.store.get_secret(provider)
            if not existing:
                raise LabError(f"{provider} requires an API key")
            key = existing["api_key"]
        self.store.upsert_secret(provider, key, extra)
        if provider == "ollama" and extra.get("base_url"):
            self.store.set_setting("ollama_base_url", extra["base_url"])

    def architecture(self, condition: str, provider: str | None = None, dataset_id: str | None = None) -> dict[str, Any]:
        pack = None
        if dataset_id:
            dataset = self.store.get_dataset(dataset_id)
            pack = dataset["pack"] if dataset else None
        configured = ["reference", "ollama"]
        for item in self.store.list_secret_public():
            if item["configured"] and item["provider"] not in configured:
                configured.append(item["provider"])
        return architecture_view(
            condition,
            provider=provider or self.store.get_setting("provider", "ollama"),
            configured_providers=configured,
            packs_present=packs_present(pack),
        )

    def prepare_run(
        self,
        *,
        condition: str,
        dataset_id: str,
        provider: str | None = None,
        model: str | None = None,
        matched_run_id: str | None = None,
        budgets: dict[str, Any] | None = None,
        seed: int = 42,
        run_id: str | None = None,
    ) -> dict[str, Any]:
        if condition not in CONDITIONS:
            raise LabError("condition must be one of C0–C7")
        dataset = self.store.get_dataset(dataset_id)
        if not dataset:
            raise LabError("dataset not found")
        profile = get_condition(condition)
        if profile["matched_run_required"]:
            matched = self.store.get_run(matched_run_id or "")
            if not matched or matched["condition"] != "C3" or matched["status"] != "completed":
                raise LabError("C5 requires matched_run_id of a completed C3 run")
            events = self.store.list_events(matched["id"])
            has_evidence = any(
                event["kind"] == "tool_observation" and (event["payload"] or {}).get("records")
                for event in events
            )
            if not has_evidence:
                raise LabError("Matched C3 run has zero evidence; C5 is not backfilled")
        elif matched_run_id:
            raise LabError("matched_run_id is only valid for C5")

        provider = provider or self.store.get_setting("provider", "ollama")
        if provider not in PROVIDER_INDEX:
            raise LabError(f"unknown provider {provider}")
        model_name = model or self.store.get_setting("model") or PROVIDER_INDEX[provider]["default_model"]
        if PROVIDER_INDEX[provider]["needs_key"]:
            secret = self.store.get_secret(provider)
            if not secret or not secret.get("api_key"):
                raise LabError(f"Save an API key for {provider} before running.")
        if provider == "ollama":
            status = probe_ollama(self.store.get_setting("ollama_base_url", "http://127.0.0.1:11434"))
            if not status["ok"]:
                raise LabError(f"Ollama is not reachable: {status.get('error')}")
            if status["models"] and model_name not in status["models"] and f"{model_name}:latest" not in status["models"]:
                raise LabError(f"Ollama does not have model {model_name}. Pulled: {status['models']}")

        default_tools = 6 if provider == "ollama" else 12
        budgets = budgets or {}
        resolved_budgets = {
            "max_tool_calls": int(budgets.get("max_tool_calls", default_tools)),
            "max_records_per_call": int(budgets.get("max_records_per_call", 100)),
            "max_runtime_seconds": int(budgets.get("max_runtime_seconds", 300)),
            "max_model_tokens": int(budgets.get("max_model_tokens", 32000)),
        }
        run_id = run_id or f"run-{uuid.uuid4().hex[:12]}"
        model_profile = {"provider": provider, "model": model_name}
        manifest = {
            "schema_version": "1.0",
            "run_id": run_id,
            "incident_id": dataset["incident_id"],
            "condition_id": condition,
            "dataset_id": dataset_id,
            "seed": int(seed),
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
            "seed": int(seed),
            "budgets": resolved_budgets,
            "matched_run_id": matched_run_id,
            "manifest": manifest,
            "state": None,
            "report": None,
            "error": None,
        }
        self.store.insert_run(record)
        return record

    async def run_condition(
        self,
        condition: str,
        dataset_id: str,
        provider: str | None = None,
        model: str | None = None,
        matched_run_id: str | None = None,
        budgets: dict[str, Any] | None = None,
        seed: int = 42,
    ) -> dict[str, Any]:
        record = self.prepare_run(
            condition=condition,
            dataset_id=dataset_id,
            provider=provider,
            model=model,
            matched_run_id=matched_run_id,
            budgets=budgets,
            seed=seed,
        )
        await self.orchestrator.run(record["id"])
        run = self.store.get_run(record["id"])
        return summarize_run(run, self.store.list_events(record["id"]))

    async def run_suite(
        self,
        dataset_id: str,
        provider: str | None = None,
        model: str | None = None,
        conditions: list[str] | None = None,
        budgets: dict[str, Any] | None = None,
        seed: int = 42,
        report_dir: Path | None = None,
    ) -> dict[str, Any]:
        dataset = self.store.get_dataset(dataset_id)
        if not dataset:
            raise LabError("dataset not found")
        conditions = conditions or list(SUITE_CONDITIONS)
        provider = provider or self.store.get_setting("provider", "ollama")
        model_name = model or self.store.get_setting("model") or PROVIDER_INDEX[provider]["default_model"]
        summaries: list[dict[str, Any]] = []
        c3_id = None
        for condition in conditions:
            if condition == "C5" and not c3_id:
                summaries.append(
                    {
                        "condition": "C5",
                        "status": "skipped",
                        "error": "C5 skipped; no completed C3 run in this suite.",
                    }
                )
                continue
            summary = await self.run_condition(
                condition,
                dataset_id,
                provider=provider,
                model=model_name,
                matched_run_id=c3_id if condition == "C5" else None,
                budgets=budgets,
                seed=seed,
            )
            summaries.append(summary)
            if condition == "C3" and summary.get("status") == "completed":
                c3_id = summary.get("run_id")
        suite = {
            "generated_at": utcnow(),
            "dataset_id": dataset_id,
            "incident_id": dataset["incident_id"],
            "provider": provider,
            "model": model_name,
            "runs": summaries,
        }
        suite["files"] = write_report(suite, directory=report_dir)
        return suite


def format_architecture(view: dict[str, Any]) -> str:
    lines = [
        f"{view['condition_id']} · {view['profile']['name']} · {view.get('provider') or 'ollama'}",
        view["profile"]["summary"],
        "",
    ]
    for plane in view["planes"]:
        lines.append(f"{plane['label']}")
        for svc in plane["services"]:
            mark = "ON" if svc["enabled"] else "off"
            extra = []
            if svc.get("selected"):
                extra.append("pinned")
            if svc.get("loaded"):
                extra.append("data")
            suffix = f" ({', '.join(extra)})" if extra else ""
            lines.append(f"  [{mark}] {svc['label']}{suffix}")
        lines.append("")
    return "\n".join(lines)


def format_event(event: dict[str, Any]) -> str:
    payload = event.get("payload") or {}
    why = (
        payload.get("expected_discrimination")
        or payload.get("reason")
        or payload.get("summary")
        or payload.get("error")
        or payload.get("message")
        or (f"{payload['record_count']} records" if payload.get("record_count") is not None else "")
        or payload.get("tool")
        or payload.get("stage")
        or ""
    )
    seq = event.get("sequence", 0)
    return f"{seq:03d}  {event.get('service')}  {event.get('kind')}  {why}".rstrip()


def format_summary(summary: dict[str, Any]) -> str:
    if summary.get("status") == "skipped":
        return f"{summary['condition']} skipped  {summary.get('error') or ''}"
    verdict = summary.get("verdict") or "—"
    error = f"  error={summary['error']}" if summary.get("error") else ""
    return (
        f"{summary.get('condition')} {summary.get('status')}  {verdict}  "
        f"tools={summary.get('tool_observations', 0)}  kb={summary.get('knowledge_retrievals', 0)}"
        f"{error}"
    )
