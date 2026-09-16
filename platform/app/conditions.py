from __future__ import annotations

from typing import Any

PLANES: list[dict[str, Any]] = [
    {
        "id": "control",
        "label": "Control plane",
        "blurb": "Owns the investigation loop, prompts, state, and policy.",
        "services": [
            {
                "id": "investigation-api",
                "label": "Investigation API",
                "role": "Accept runs, validate scope, return results.",
                "capability": "api",
            },
            {
                "id": "agent-orchestrator",
                "label": "Orchestrator",
                "role": "Route actions, enforce budgets, stop the loop.",
                "capability": "adaptive_loop",
            },
            {
                "id": "context-builder",
                "label": "Context builder",
                "role": "Assemble bounded prompts from alert, state, tools, knowledge.",
                "capability": "always",
            },
            {
                "id": "model-gateway",
                "label": "Model gateway",
                "role": "Pinned structured decisions. No datastore credentials.",
                "capability": "always",
            },
            {
                "id": "state-service",
                "label": "State service",
                "role": "Hypotheses, evidence ledger, entities, stop state.",
                "capability": "structured_state",
            },
            {
                "id": "policy-engine",
                "label": "Policy engine",
                "role": "Allowlist, scope, read-only, result caps.",
                "capability": "adaptive_loop",
            },
        ],
    },
    {
        "id": "knowledge",
        "label": "Knowledge plane",
        "blurb": "Versioned ATT&CK / Sigma / playbook passages. Never treated as proof.",
        "services": [
            {
                "id": "knowledge-service",
                "label": "Knowledge service",
                "role": "Retrieve versioned passages by question and corpus tags.",
                "capability": "knowledge",
            }
        ],
    },
    {
        "id": "evidence",
        "label": "Evidence plane",
        "blurb": "Read-only typed tools over uploaded incident telemetry.",
        "services": [
            {
                "id": "telemetry-gateway",
                "label": "Telemetry gateway",
                "role": "Typed tools, stable evidence IDs, observation envelopes.",
                "capability": "search",
            },
            {
                "id": "telemetry-store",
                "label": "Telemetry store",
                "role": "Incident-scoped logs. Ground truth is sealed.",
                "capability": "store",
            },
            {
                "id": "fixed-retrieval",
                "label": "Fixed retrieval",
                "role": "Analyst query pack. Model cannot choose queries.",
                "capability": "fixed_retrieval",
            },
            {
                "id": "matched-evidence",
                "label": "Matched evidence",
                "role": "Passive C3 records with tool names and order stripped.",
                "capability": "matched_evidence",
            },
            {
                "id": "oracle-evidence",
                "label": "Oracle evidence",
                "role": "Expert-minimal decisive set.",
                "capability": "oracle_evidence",
            },
            {
                "id": "oracle-plan",
                "label": "Oracle plan",
                "role": "Expert investigation plan; agent may still adapt.",
                "capability": "oracle_plan",
            },
        ],
    },
    {
        "id": "reporting",
        "label": "Reporting & evaluation",
        "blurb": "Grounded report, deterministic validator, append-only trajectory.",
        "services": [
            {
                "id": "report-service",
                "label": "Report service",
                "role": "Final schema. Repair cannot invent evidence.",
                "capability": "always",
            },
            {
                "id": "report-validator",
                "label": "Report validator",
                "role": "Citations, verdict vocabulary, ATT&CK syntax.",
                "capability": "always",
            },
            {
                "id": "trajectory-service",
                "label": "Trajectory service",
                "role": "Append-only events and replay checkpoints.",
                "capability": "always",
            },
        ],
    },
]

SEARCH_TOOLS = [
    "grep_logs",
    "query_events",
    "find_process_tree",
    "build_timeline",
    "search_related",
]

STAGES = [
    {"id": "create_run", "label": "Create run"},
    {"id": "initialize_state", "label": "Initialize state"},
    {"id": "build_context", "label": "Build context"},
    {"id": "generate_decision", "label": "Generate decision"},
    {"id": "validate_action", "label": "Validate action"},
    {"id": "execute_action", "label": "Execute action"},
    {"id": "record_observation", "label": "Record observation"},
    {"id": "update_state", "label": "Update state"},
    {"id": "generate_report", "label": "Generate report"},
    {"id": "validate_report", "label": "Validate report"},
    {"id": "finalize", "label": "Finalize trajectory"},
]


def _profile(
    *,
    name: str,
    summary: str,
    context_mode: str,
    knowledge: dict[str, Any],
    search: dict[str, Any],
    state_enabled: bool,
    tools: list[str],
    special: str | None = None,
    matched_c3: bool = False,
) -> dict[str, Any]:
    return {
        "name": name,
        "summary": summary,
        "context_mode": context_mode,
        "knowledge": knowledge,
        "search": search,
        "state": {"enabled": state_enabled, "schema_version": "1.0"},
        "oracle": {
            "plan_provider": "oracle_plan" in tools,
            "evidence_provider": "load_oracle_evidence" in tools,
        },
        "matched_run_required": matched_c3,
        "allowed_interfaces": tools,
        "special": special,
        "capabilities": {
            "knowledge": bool(knowledge.get("enabled")),
            "adaptive_loop": search.get("control_mode") == "adaptive_agent",
            "structured_state": state_enabled,
            "search": bool(search.get("enabled")) and search.get("control_mode") == "adaptive_agent",
            "store": True,
            "fixed_retrieval": "execute_fixed_retrieval" in tools,
            "matched_evidence": matched_c3,
            "oracle_evidence": "load_oracle_evidence" in tools,
            "oracle_plan": "load_oracle_plan" in tools,
            "api": True,
            "always": True,
        },
    }


CONDITIONS: dict[str, dict[str, Any]] = {
    "C0": _profile(
        name="Raw LLM",
        summary="One fixed raw-log window. No knowledge, no search, no loop.",
        context_mode="fixed_raw",
        knowledge={"enabled": False, "retrieval_mode": "off", "top_k": 0},
        search={"enabled": False, "control_mode": "disabled", "tool_allowlist": []},
        state_enabled=False,
        tools=["submit_report"],
    ),
    "C1": _profile(
        name="Knowledge-only",
        summary="Same raw window as C0, plus versioned knowledge passages.",
        context_mode="fixed_raw",
        knowledge={"enabled": True, "retrieval_mode": "agent_selected", "top_k": 4},
        search={"enabled": False, "control_mode": "disabled", "tool_allowlist": []},
        state_enabled=False,
        tools=["retrieve_knowledge", "submit_report"],
    ),
    "C2": _profile(
        name="Search-only agent",
        summary="Adaptive telemetry search and structured state. Knowledge is unplugged.",
        context_mode="alert_only",
        knowledge={"enabled": False, "retrieval_mode": "off", "top_k": 0},
        search={"enabled": True, "control_mode": "adaptive_agent", "tool_allowlist": SEARCH_TOOLS},
        state_enabled=True,
        tools=[*SEARCH_TOOLS, "submit_report"],
    ),
    "C3": _profile(
        name="Full agent",
        summary="Knowledge retrieval and adaptive search. No oracle evidence or plan.",
        context_mode="alert_only",
        knowledge={"enabled": True, "retrieval_mode": "agent_selected", "top_k": 4},
        search={"enabled": True, "control_mode": "adaptive_agent", "tool_allowlist": SEARCH_TOOLS},
        state_enabled=True,
        tools=["retrieve_knowledge", *SEARCH_TOOLS, "submit_report"],
    ),
    "C4": _profile(
        name="Fixed retrieval",
        summary="Analyst query pack runs first. The model only interprets passive results.",
        context_mode="passive_fixed",
        knowledge={"enabled": True, "retrieval_mode": "fixed", "top_k": 4},
        search={"enabled": True, "control_mode": "fixed_executor", "tool_allowlist": []},
        state_enabled=False,
        tools=["execute_fixed_retrieval", "retrieve_knowledge", "submit_report"],
        special="analyst query pack",
    ),
    "C5": _profile(
        name="Passive matched evidence",
        summary="Exact telemetry C3 retrieved, with tool names and search order removed.",
        context_mode="passive_matched",
        knowledge={"enabled": True, "retrieval_mode": "passive", "top_k": 4},
        search={"enabled": False, "control_mode": "disabled", "tool_allowlist": []},
        state_enabled=False,
        tools=["retrieve_knowledge", "submit_report"],
        special="matched C3 run required",
        matched_c3=True,
    ),
    "C6": _profile(
        name="Oracle evidence",
        summary="Expert-minimal decisive telemetry plus knowledge. Upper bound on interpretation.",
        context_mode="oracle_evidence",
        knowledge={"enabled": True, "retrieval_mode": "passive", "top_k": 4},
        search={"enabled": False, "control_mode": "disabled", "tool_allowlist": []},
        state_enabled=False,
        tools=["load_oracle_evidence", "retrieve_knowledge", "submit_report"],
        special="oracle evidence pack",
    ),
    "C7": _profile(
        name="Oracle plan",
        summary="Expert plan is injected. The adaptive loop may still revise arguments and beliefs.",
        context_mode="alert_only",
        knowledge={"enabled": True, "retrieval_mode": "agent_selected", "top_k": 4},
        search={"enabled": True, "control_mode": "adaptive_agent", "tool_allowlist": SEARCH_TOOLS},
        state_enabled=True,
        tools=["load_oracle_plan", "retrieve_knowledge", *SEARCH_TOOLS, "submit_report"],
        special="oracle plan pack",
    ),
}


def condition_ids() -> list[str]:
    return list(CONDITIONS.keys())


def get_condition(condition_id: str) -> dict[str, Any]:
    if condition_id not in CONDITIONS:
        raise KeyError(condition_id)
    return CONDITIONS[condition_id]


def interface_enabled(condition_id: str, name: str) -> bool:
    return name in get_condition(condition_id)["allowed_interfaces"]


def architecture_view(condition_id: str) -> dict[str, Any]:
    profile = get_condition(condition_id)
    caps = profile["capabilities"]
    planes = []
    for plane in PLANES:
        services = []
        for service in plane["services"]:
            enabled = bool(caps.get(service["capability"], False))
            if service["id"] == "telemetry-store":
                enabled = True
            if service["id"] == "telemetry-gateway":
                enabled = bool(profile["search"]["enabled"])
            services.append({**service, "enabled": enabled})
        planes.append({**plane, "services": services})
    return {
        "condition_id": condition_id,
        "profile": profile,
        "planes": planes,
        "stages": STAGES,
        "search_tools": SEARCH_TOOLS,
    }


def disabled_error(condition_id: str, service: str, operation: str) -> dict[str, Any]:
    return {
        "status": "error",
        "error_code": "SERVICE_DISABLED",
        "condition_id": condition_id,
        "service": service,
        "operation": operation,
        "message": f"{service} is disabled for condition {condition_id}.",
        "retryable": False,
    }
