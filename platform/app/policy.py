from __future__ import annotations

from typing import Any

from .conditions import SEARCH_TOOLS, disabled_error, interface_enabled


class PolicyEngine:
    def __init__(self, condition_id: str, pack: dict[str, Any], max_records: int) -> None:
        self.condition_id = condition_id
        self.pack = pack
        self.max_records = max_records
        self.scope = pack.get("scope") or {}

    def validate(self, action: dict[str, Any]) -> dict[str, Any]:
        tool = action.get("tool")
        arguments = dict(action.get("arguments") or {})
        if not interface_enabled(self.condition_id, tool):
            return {
                "action_id": action.get("action_id"),
                "decision": "reject",
                "reason": disabled_error(self.condition_id, "policy-engine", tool)["message"],
                "error": disabled_error(self.condition_id, self._service_for(tool), tool),
                "normalized_action": None,
                "applied_limits": {},
            }
        if tool in SEARCH_TOOLS:
            host = arguments.get("host") or (arguments.get("filter") or {}).get("host")
            allowed_hosts = set(self.scope.get("hosts") or [])
            if host and allowed_hosts and host not in allowed_hosts:
                return {
                    "action_id": action.get("action_id"),
                    "decision": "reject",
                    "reason": f"Host {host} is outside incident scope.",
                    "normalized_action": None,
                    "applied_limits": {},
                }
            source = arguments.get("source")
            allowed_sources = set(self.scope.get("allowed_log_sources") or [])
            if source and allowed_sources and source not in allowed_sources:
                return {
                    "action_id": action.get("action_id"),
                    "decision": "reject",
                    "reason": f"Log source {source} is not permitted for this incident.",
                    "normalized_action": None,
                    "applied_limits": {},
                }
            arguments["limit"] = min(int(arguments.get("limit") or self.max_records), self.max_records)
            if "filter" in arguments and host and "host" not in arguments["filter"]:
                arguments["filter"] = {**arguments["filter"], "host": host}
        return {
            "action_id": action.get("action_id"),
            "decision": "allow",
            "reason": "Tool and arguments are permitted within incident scope.",
            "normalized_action": {"tool": tool, "arguments": arguments},
            "applied_limits": {"max_records": self.max_records, "timeout_ms": 5000},
        }

    def _service_for(self, tool: str) -> str:
        if tool == "retrieve_knowledge":
            return "knowledge-service"
        if tool in SEARCH_TOOLS:
            return "telemetry-gateway"
        if tool == "execute_fixed_retrieval":
            return "fixed-retrieval"
        if tool == "load_oracle_evidence":
            return "oracle-evidence"
        if tool == "load_oracle_plan":
            return "oracle-plan"
        return "policy-engine"
