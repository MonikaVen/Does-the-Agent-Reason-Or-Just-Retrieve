from __future__ import annotations

import asyncio
import hashlib
import json
import os
from typing import Any

from . import state as state_mod
from .bus import EventBus
from .conditions import architecture_view, disabled_error, get_condition, interface_enabled
from .context import build_context
from .knowledge import KnowledgeService
from .llm import ModelGateway
from .packs import packs_present
from .policy import PolicyEngine
from .report import validate_report
from .store import Store, utcnow
from .telemetry import TelemetryGateway, TelemetryStore, flatten_pack, normalize_record

STEP_DELAY = float(os.environ.get("LAB_STEP_DELAY", "0.16"))


class Orchestrator:
    def __init__(self, store: Store, bus: EventBus) -> None:
        self.store = store
        self.bus = bus
        self.knowledge = KnowledgeService()

    async def run(self, run_id: str) -> None:
        run = self.store.get_run(run_id)
        if not run:
            return
        dataset = self.store.get_dataset(run["dataset_id"])
        pack = dataset["pack"]
        profile = get_condition(run["condition"])
        try:
            self.store.update_run(run_id, status="running", started_at=utcnow())
            await self._execute(run, dataset, pack, profile)
        except Exception as exc:  # noqa: BLE001 — surface any engine failure on the run
            await self.bus.emit(
                run_id,
                "run_failed",
                "agent-orchestrator",
                {"error": str(exc)},
                stage="finalize",
            )
            self.store.update_run(run_id, status="failed", completed_at=utcnow(), error=str(exc))

    async def _execute(
        self,
        run: dict[str, Any],
        dataset: dict[str, Any],
        pack: dict[str, Any],
        profile: dict[str, Any],
    ) -> None:
        run_id = run["id"]
        condition = run["condition"]
        budgets = run["budgets"]
        model_cfg = ((run.get("manifest") or {}).get("model") or {})
        provider = model_cfg.get("provider") or "reference"
        model_name = model_cfg.get("model")
        secret = self.store.get_secret(provider) or {}
        connector_secrets = dict(secret.get("extra") or {})
        if secret.get("api_key"):
            connector_secrets["api_key"] = secret["api_key"]
        if provider == "ollama" and not connector_secrets.get("base_url"):
            connector_secrets["base_url"] = self.store.get_setting("ollama_base_url") or "http://127.0.0.1:11434"
        model = ModelGateway(provider, model_name, connector_secrets)
        self.knowledge = KnowledgeService(extra=pack.get("knowledge_corpus"))
        await self._stage(run_id, "create_run", "investigation-api", {"condition": condition, "provider": provider, "model": model.model})

        telemetry_store = TelemetryStore(pack)
        gateway = TelemetryGateway(telemetry_store, max_records=int(budgets.get("max_records_per_call", 100)))
        policy = PolicyEngine(condition, pack, int(budgets.get("max_records_per_call", 100)))

        state = None
        if profile["state"]["enabled"]:
            await self._stage(run_id, "initialize_state", "state-service")
            state = state_mod.initial_state(run_id, budgets)
            self.store.update_run(run_id, state=state)
            await self.bus.emit(run_id, "state_initialized", "state-service", state, "initialize_state")

        observations: list[dict[str, Any]] = []
        knowledge_passages: list[dict[str, Any]] = []
        evidence_ids: set[str] = set()

        if profile["oracle"]["plan_provider"]:
            plan = pack.get("oracle_plan") or []
            await self._call(run_id, "oracle-plan", "oracle_plan_loaded", {"steps": plan})
            if state is not None:
                state = {**state, "oracle_plan": plan}

        if profile["search"]["control_mode"] == "fixed_executor":
            obs, passages, ids = await self._fixed_retrieval(run_id, pack, gateway, policy)
            observations.extend(obs)
            knowledge_passages.extend(passages)
            evidence_ids.update(ids)

        if condition == "C5":
            obs, ids = await self._matched_evidence(run_id, run, pack)
            observations.extend(obs)
            evidence_ids.update(ids)

        if profile["oracle"]["evidence_provider"]:
            records = [normalize_record(item.get("source") or "oracle", item) for item in pack.get("oracle_evidence") or []]
            public = [
                {
                    "evidence_id": item.get("evidence_id"),
                    "source": item.get("source"),
                    "timestamp": item.get("timestamp"),
                    "host": item.get("host"),
                    "fields": item.get("fields") or {},
                }
                for item in records
            ]
            observation = {
                "tool": "load_oracle_evidence",
                "status": "success",
                "records": public,
                "record_count": len(public),
                "truncated": False,
            }
            await self._call(run_id, "oracle-evidence", "oracle_evidence_loaded", observation)
            observations.append(observation)
            evidence_ids.update(item["evidence_id"] for item in public if item.get("evidence_id"))

        if profile["context_mode"] == "fixed_raw":
            raw = flatten_pack(pack)
            evidence_ids.update(item.get("evidence_id") for item in raw if item.get("evidence_id"))

        adaptive = profile["search"]["control_mode"] == "adaptive_agent"
        tools = list(profile["allowed_interfaces"])
        max_calls = int(budgets.get("max_tool_calls", 12))
        steps = 0

        if adaptive:
            while True:
                if state and int(state["budget_state"]["tool_calls_remaining"]) <= 0:
                    state = state_mod.mark_stop(state, "Tool-call budget exhausted.")
                    break
                if steps >= max_calls:
                    if state:
                        state = state_mod.mark_stop(state, "Step budget exhausted.")
                    break

                await self._stage(run_id, "build_context", "context-builder")
                context = build_context(
                    condition_id=condition,
                    profile=profile,
                    pack=pack,
                    state=state,
                    observations=observations,
                    knowledge=knowledge_passages,
                    tools=tools,
                )
                await self.bus.emit(
                    run_id,
                    "context_built",
                    "context-builder",
                    {
                        "mode": context["context_mode"],
                        "layers": [layer["name"] for layer in context["layers"]],
                        "truncation": context["truncation"],
                    },
                    "build_context",
                )

                await self._stage(run_id, "generate_decision", "model-gateway")
                decision = await asyncio.to_thread(model.generate_decision, context)
                await self.bus.emit(
                    run_id,
                    "decision",
                    "model-gateway",
                    {**decision, "provider": provider, "model": model.model},
                    "generate_decision",
                )
                if state is not None:
                    state = state_mod.apply_beliefs(
                        state, decision.get("hypotheses") or [], decision.get("next_question")
                    )
                    self.store.update_run(run_id, state=state)
                    await self.bus.emit(run_id, "state_updated", "state-service", {"hypotheses": state["hypotheses"]}, "update_state")

                if decision.get("stop") or decision.get("selected_action", {}).get("tool") == "submit_report":
                    if state is not None:
                        state = state_mod.mark_stop(state, decision.get("stop_reason") or "Model requested stop.")
                    break

                action = decision.get("selected_action") or {}
                await self._stage(run_id, "validate_action", "policy-engine")
                policy_decision = policy.validate(action)
                await self.bus.emit(run_id, "policy_decision", "policy-engine", policy_decision, "validate_action")
                if policy_decision["decision"] != "allow":
                    await self.bus.emit(
                        run_id,
                        "action_rejected",
                        "policy-engine",
                        policy_decision.get("error") or policy_decision,
                        "validate_action",
                    )
                    if state is not None:
                        state = state_mod.mark_stop(state, policy_decision.get("reason") or "Policy rejected the action.")
                    break

                normalized = policy_decision["normalized_action"]
                await self._stage(run_id, "execute_action", self._service_for(normalized["tool"]))
                observation = await self._execute_tool(
                    run_id, condition, normalized["tool"], normalized["arguments"], gateway
                )
                await self._stage(run_id, "record_observation", "trajectory-service")
                await self.bus.emit(
                    run_id,
                    "tool_observation",
                    self._service_for(normalized["tool"]),
                    observation,
                    "record_observation",
                )
                observations.append(observation)
                for record in observation.get("records") or []:
                    if record.get("evidence_id"):
                        evidence_ids.add(record["evidence_id"])
                if observation.get("passages"):
                    knowledge_passages = observation["passages"]
                    if state is not None:
                        state = state_mod.apply_knowledge(state, knowledge_passages)

                if state is not None and normalized["tool"] != "retrieve_knowledge":
                    await self._stage(run_id, "update_state", "state-service")
                    state = state_mod.apply_observation(state, observation, normalized)
                    self.store.update_run(run_id, state=state)
                    await self.bus.emit(run_id, "state_updated", "state-service", state, "update_state")
                steps += 1
        else:
            if profile["knowledge"]["enabled"] and profile["knowledge"]["retrieval_mode"] in {
                "agent_selected",
                "passive",
                "fixed",
            }:
                if not knowledge_passages:
                    knowledge_passages = await self._retrieve_knowledge(
                        run_id,
                        condition,
                        {
                            "question": (pack.get("alert") or {}).get("summary") or "incident investigation",
                            "corpus_tags": ["detection", "procedural"],
                            "top_k": profile["knowledge"].get("top_k") or 4,
                        },
                    )

            await self._stage(run_id, "build_context", "context-builder")
            context = build_context(
                condition_id=condition,
                profile=profile,
                pack=pack,
                state=state,
                observations=observations,
                knowledge=knowledge_passages,
                tools=tools,
            )
            await self.bus.emit(
                run_id,
                "context_built",
                "context-builder",
                {"mode": context["context_mode"], "layers": [layer["name"] for layer in context["layers"]]},
                "build_context",
            )
            await self._stage(run_id, "generate_decision", "model-gateway")
            # One-shot conditions still go through the gateway so the node lights up.
            one_shot = {
                "schema_version": "1.0",
                "hypotheses": [],
                "stop": True,
                "stop_reason": "Condition has no adaptive loop.",
                "selected_action": {"tool": "submit_report", "arguments": {}},
                "expected_discrimination": "Interpret the supplied context without choosing further queries.",
            }
            await self.bus.emit(run_id, "decision", "model-gateway", one_shot, "generate_decision")

        await self._stage(run_id, "generate_report", "report-service")
        final_context = build_context(
            condition_id=condition,
            profile=profile,
            pack=pack,
            state=state,
            observations=observations,
            knowledge=knowledge_passages,
            tools=tools,
        )
        report = await asyncio.to_thread(model.generate_report, final_context)
        await self.bus.emit(run_id, "report_generated", "report-service", report, "generate_report")

        await self._stage(run_id, "validate_report", "report-validator")
        validation = validate_report(report, evidence_ids)
        await self.bus.emit(run_id, "report_validated", "report-validator", validation, "validate_report")
        if not validation["ok"]:
            report = {
                **report,
                "verdict": "inconclusive",
                "remaining_uncertainty": "; ".join(validation["errors"]),
            }
            validation = validate_report(report, evidence_ids)

        await self._stage(run_id, "finalize", "trajectory-service")
        if state is not None:
            state = state_mod.mark_stop(state, (state.get("stop_state") or {}).get("reason") or "Report submitted.")
        self.store.update_run(
            run_id,
            status="completed",
            completed_at=utcnow(),
            state=state,
            report=report,
            manifest={
                **(run.get("manifest") or {}),
                "evidence_ids": sorted(evidence_ids),
                "validation": validation,
                "architecture": architecture_view(
                    condition,
                    provider=provider,
                    packs_present=packs_present(pack),
                ),
            },
        )
        await self.bus.emit(
            run_id,
            "run_completed",
            "investigation-api",
            {"verdict": report.get("verdict"), "confidence": report.get("confidence")},
            "finalize",
        )

    async def _fixed_retrieval(
        self,
        run_id: str,
        pack: dict[str, Any],
        gateway: TelemetryGateway,
        policy: PolicyEngine,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], set[str]]:
        pack_obj = pack.get("fixed_query_pack") or {"version": "empty", "queries": []}
        await self._call(run_id, "fixed-retrieval", "fixed_plan_loaded", {"version": pack_obj.get("version"), "queries": pack_obj.get("queries")})
        observations = []
        passages: list[dict[str, Any]] = []
        ids: set[str] = set()
        for query in pack_obj.get("queries") or []:
            tool = query.get("tool")
            arguments = query.get("arguments") or {}
            if tool == "retrieve_knowledge":
                passages = await self._retrieve_knowledge(run_id, "C4", arguments)
                continue
            decision = policy.validate({"tool": tool, "arguments": arguments, "action_id": "fixed"})
            # C4's executor is allowed to run telemetry even though the agent allowlist
            # does not expose those tools. The policy check still enforces incident scope.
            if tool in {"grep_logs", "query_events", "find_process_tree", "build_timeline", "search_related"}:
                observation = gateway.execute(tool, arguments)
                await self.bus.emit(run_id, "tool_observation", "fixed-retrieval", observation, "execute_action")
                observations.append(observation)
                for record in observation.get("records") or []:
                    if record.get("evidence_id"):
                        ids.add(record["evidence_id"])
            elif decision["decision"] != "allow":
                await self.bus.emit(run_id, "action_rejected", "policy-engine", decision, "validate_action")
        await self._call(run_id, "fixed-retrieval", "fixed_retrieval_completed", {"evidence_ids": sorted(ids)})
        return observations, passages, ids

    async def _matched_evidence(
        self, run_id: str, run: dict[str, Any], pack: dict[str, Any]
    ) -> tuple[list[dict[str, Any]], set[str]]:
        source_id = run.get("matched_run_id")
        if not source_id:
            raise RuntimeError("C5 requires a completed C3 run")
        events = self.store.list_events(source_id)
        records = []
        for event in events:
            if event["kind"] != "tool_observation":
                continue
            for record in (event["payload"] or {}).get("records") or []:
                stripped = {
                    "evidence_id": record.get("evidence_id"),
                    "source": record.get("source"),
                    "timestamp": record.get("timestamp"),
                    "host": record.get("host"),
                    "fields": record.get("fields") or {},
                }
                records.append(stripped)
        # Reorder deterministically so C5 does not leak C3 search order.
        records.sort(key=lambda rec: rec.get("evidence_id") or "")
        ids = {rec["evidence_id"] for rec in records if rec.get("evidence_id")}
        if not ids:
            raise RuntimeError("Matched C3 run produced zero evidence; C5 is not silently backfilled.")
        observation = {
            "tool": "passive_matched_evidence",
            "status": "success",
            "records": records,
            "record_count": len(records),
            "truncated": False,
            "order_removed": True,
            "source_run_id": source_id,
        }
        await self._call(run_id, "matched-evidence", "matched_evidence_loaded", observation)
        return [observation], ids

    async def _execute_tool(
        self,
        run_id: str,
        condition: str,
        tool: str,
        arguments: dict[str, Any],
        gateway: TelemetryGateway,
    ) -> dict[str, Any]:
        if not interface_enabled(condition, tool):
            return disabled_error(condition, self._service_for(tool), tool)
        if tool == "retrieve_knowledge":
            passages = await self._retrieve_knowledge(run_id, condition, arguments)
            return {"tool": tool, "status": "success", "passages": passages, "records": [], "record_count": 0}
        await self.bus.emit(
            run_id,
            "tool_requested",
            "telemetry-gateway",
            {"tool": tool, "arguments": arguments},
            "execute_action",
        )
        return gateway.execute(tool, arguments)

    async def _retrieve_knowledge(self, run_id: str, condition: str, arguments: dict[str, Any]) -> list[dict[str, Any]]:
        if not interface_enabled(condition, "retrieve_knowledge"):
            await self.bus.emit(
                run_id,
                "service_disabled",
                "knowledge-service",
                disabled_error(condition, "knowledge-service", "retrieve_knowledge"),
            )
            return []
        result = self.knowledge.search(
            arguments.get("question") or "",
            arguments.get("corpus_tags") or [],
            int(arguments.get("top_k") or 4),
        )
        await self._call(run_id, "knowledge-service", "knowledge_retrieved", result)
        return result["passages"]

    async def _stage(self, run_id: str, stage: str, service: str, payload: dict[str, Any] | None = None) -> None:
        await self.bus.emit(run_id, "stage", service, payload or {"stage": stage}, stage)
        await asyncio.sleep(STEP_DELAY)

    async def _call(self, run_id: str, service: str, kind: str, payload: dict[str, Any]) -> None:
        await self.bus.emit(run_id, kind, service, payload, "execute_action")
        await asyncio.sleep(STEP_DELAY / 2)

    def _service_for(self, tool: str) -> str:
        mapping = {
            "retrieve_knowledge": "knowledge-service",
            "submit_report": "report-service",
            "execute_fixed_retrieval": "fixed-retrieval",
            "load_oracle_evidence": "oracle-evidence",
            "load_oracle_plan": "oracle-plan",
        }
        return mapping.get(tool, "telemetry-gateway")


def dataset_passport(pack: dict[str, Any]) -> dict[str, Any]:
    telemetry = pack.get("telemetry") or {}
    counts = {source: len(items or []) for source, items in telemetry.items()}
    return {
        "incident_id": pack.get("incident_id"),
        "name": pack.get("name") or pack.get("incident_id"),
        "alert": pack.get("alert") or {},
        "scope": pack.get("scope") or {},
        "record_counts": counts,
        "record_total": sum(counts.values()),
        "has_oracle_evidence": bool(pack.get("oracle_evidence")),
        "has_oracle_plan": bool(pack.get("oracle_plan")),
        "has_fixed_query_pack": bool(pack.get("fixed_query_pack")),
        "has_knowledge_corpus": bool(pack.get("knowledge_corpus")),
        "has_ground_truth": bool(pack.get("ground_truth")),
        "packs_present": {
            "alert": bool(pack.get("alert")),
            "telemetry": bool(telemetry),
            "knowledge": bool(pack.get("knowledge_corpus")),
            "query_pack": bool(pack.get("fixed_query_pack")),
            "oracle_evidence": bool(pack.get("oracle_evidence")),
            "oracle_plan": bool(pack.get("oracle_plan")),
            "ground_truth": bool(pack.get("ground_truth")),
        },
    }


def validate_pack(pack: dict[str, Any]) -> list[str]:
    errors = []
    if not pack.get("incident_id"):
        errors.append("incident_id is required")
    if not isinstance(pack.get("alert"), dict) or not pack["alert"]:
        errors.append("alert object is required")
    telemetry = pack.get("telemetry")
    if not isinstance(telemetry, dict) or not telemetry:
        errors.append("telemetry object with named log sources is required")
    else:
        for source, items in telemetry.items():
            if not isinstance(items, list):
                errors.append(f"telemetry.{source} must be a list")
                continue
            for index, item in enumerate(items):
                if not isinstance(item, dict):
                    errors.append(f"telemetry.{source}[{index}] must be an object")
                elif not item.get("event_id"):
                    errors.append(f"telemetry.{source}[{index}] is missing event_id")
    return errors


def config_digest(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
