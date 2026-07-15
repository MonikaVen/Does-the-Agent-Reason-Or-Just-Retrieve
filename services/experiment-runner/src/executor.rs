use crate::error::RunnerError;
use crate::manifest::{EvidenceRecord, Incident, InvestigationReport, MatchedSource, PlanStep, RunManifest, TrajectoryEvent};
use chrono::Utc;
use serde_json::{json, Value};
use std::collections::BTreeSet;
use std::fs;

pub struct ExecutionContext<'a> {
    pub manifest: &'a RunManifest,
    pub incident: &'a Incident,
    pub matched_source: Option<&'a MatchedSource>,
}

pub struct ExecutionOutput {
    pub report: InvestigationReport,
    pub events: Vec<TrajectoryEvent>,
}

pub trait ConditionExecutor {
    fn execute(&self, ctx: &ExecutionContext<'_>) -> Result<ExecutionOutput, RunnerError>;
}

pub struct DefaultConditionExecutor;

impl ConditionExecutor for DefaultConditionExecutor {
    fn execute(&self, ctx: &ExecutionContext<'_>) -> Result<ExecutionOutput, RunnerError> {
        match ctx.manifest.condition.as_str() {
            "C0" => fixed_context(ctx, false),
            "C1" => fixed_context(ctx, true),
            "C2" => adaptive(ctx, false, None),
            "C3" => adaptive(ctx, true, None),
            "C4" => fixed_retrieval(ctx),
            "C5" => matched_evidence(ctx),
            "C6" => oracle_evidence(ctx),
            "C7" => adaptive(ctx, true, Some(&ctx.incident.oracle_plan)),
            other => Err(RunnerError::UnknownCondition(other.into())),
        }
    }
}

fn event(sequence: u64, kind: &str, service: &str, payload: Value) -> TrajectoryEvent {
    TrajectoryEvent { sequence, timestamp: Utc::now(), kind: kind.into(), service: service.into(), payload }
}

fn report(condition: &str, evidence: &[EvidenceRecord]) -> InvestigationReport {
    InvestigationReport {
        verdict: "inconclusive".into(),
        confidence: 0.50,
        summary: format!(
            "{condition} completed with {} evidence record(s). Replace the reference executor with real service clients.",
            evidence.len()
        ),
        evidence_ids: evidence.iter().map(|e| e.event_id.clone()).collect(),
        remaining_uncertainty: "Reference runner does not call an external model.".into(),
    }
}

fn ensure_interface(manifest: &RunManifest, name: &str) -> Result<(), RunnerError> {
    if manifest.allowed_interfaces.contains(name) {
        Ok(())
    } else {
        Err(RunnerError::Workflow(format!(
            "SERVICE_DISABLED: '{name}' is disabled for {}", manifest.condition
        )))
    }
}

fn fixed_context(ctx: &ExecutionContext<'_>, knowledge: bool) -> Result<ExecutionOutput, RunnerError> {
    let mut events = vec![event(1, "input_prepared", "context-builder", json!({
        "mode": "fixed_raw_context",
        "record_count": ctx.incident.fixed_raw_context.len()
    }))];
    if knowledge {
        ensure_interface(ctx.manifest, "retrieve_knowledge")?;
        events.push(event(2, "knowledge_retrieved", "knowledge-service", json!({"passages": []})));
    }
    Ok(ExecutionOutput { report: report(&ctx.manifest.condition, &ctx.incident.fixed_raw_context), events })
}

fn adaptive(ctx: &ExecutionContext<'_>, knowledge: bool, plan: Option<&[PlanStep]>) -> Result<ExecutionOutput, RunnerError> {
    let mut events = Vec::new();
    let mut seq = 1;
    events.push(event(seq, "state_initialized", "state-service", json!({
        "hypotheses": [], "known_evidence": [], "stop": false
    })));
    seq += 1;

    if let Some(plan) = plan {
        ensure_interface(ctx.manifest, "load_oracle_plan")?;
        events.push(event(seq, "oracle_plan_loaded", "oracle-plan-service", serde_json::to_value(plan)?));
        seq += 1;
    }
    if knowledge {
        ensure_interface(ctx.manifest, "retrieve_knowledge")?;
        events.push(event(seq, "knowledge_retrieved", "knowledge-service", json!({"passages": []})));
        seq += 1;
    }

    ensure_interface(ctx.manifest, "query_events")?;
    events.push(event(seq, "tool_requested", "agent-orchestrator", json!({
        "tool": "query_events",
        "arguments": {"incident_id": ctx.incident.incident_id, "limit": ctx.manifest.budgets.maximum_records_per_call},
        "expected_discrimination": "Retrieve incident-scoped events for initial hypothesis formation."
    })));
    seq += 1;

    let selected: Vec<EvidenceRecord> = ctx.incident.fixed_raw_context.iter()
        .take(ctx.manifest.budgets.maximum_records_per_call as usize)
        .cloned().collect();
    events.push(event(seq, "tool_observation", "telemetry-gateway", json!({
        "tool": "query_events", "records": selected, "truncated": false
    })));
    seq += 1;
    events.push(event(seq, "state_updated", "state-service", json!({
        "known_evidence": selected.iter().map(|r| &r.event_id).collect::<Vec<_>>(),
        "stop": true,
        "stop_reason": "Reference executor performs one bounded query."
    })));

    Ok(ExecutionOutput { report: report(&ctx.manifest.condition, &selected), events })
}

fn fixed_retrieval(ctx: &ExecutionContext<'_>) -> Result<ExecutionOutput, RunnerError> {
    ensure_interface(ctx.manifest, "execute_fixed_retrieval")?;
    ensure_interface(ctx.manifest, "retrieve_knowledge")?;
    let evidence = ctx.incident.fixed_raw_context.clone();
    let events = vec![
        event(1, "fixed_plan_loaded", "fixed-retrieval-service", json!({"plan_id": "default-analyst-plan"})),
        event(2, "fixed_retrieval_completed", "fixed-retrieval-service", json!({
            "evidence_ids": evidence.iter().map(|r| &r.event_id).collect::<Vec<_>>()
        })),
        event(3, "knowledge_retrieved", "knowledge-service", json!({"passages": []})),
    ];
    Ok(ExecutionOutput { report: report("C4", &evidence), events })
}

fn matched_evidence(ctx: &ExecutionContext<'_>) -> Result<ExecutionOutput, RunnerError> {
    let source = ctx.matched_source.ok_or_else(|| RunnerError::Dependency("C5 requires C3 artifacts".into()))?;
    let text = fs::read_to_string(&source.trajectory_path)
        .map_err(|e| RunnerError::io(&source.trajectory_path, e))?;
    let ids = extract_evidence_ids(&text)?;
    let evidence: Vec<EvidenceRecord> = ctx.incident.fixed_raw_context.iter()
        .filter(|record| ids.contains(&record.event_id)).cloned().collect();
    let events = vec![
        event(1, "matched_evidence_loaded", "matched-evidence-builder", json!({
            "source_run_id": source.run_id, "evidence_ids": ids, "order_removed": true
        })),
        event(2, "passive_context_built", "context-builder", json!({"record_count": evidence.len()})),
    ];
    Ok(ExecutionOutput { report: report("C5", &evidence), events })
}

fn oracle_evidence(ctx: &ExecutionContext<'_>) -> Result<ExecutionOutput, RunnerError> {
    ensure_interface(ctx.manifest, "load_oracle_evidence")?;
    ensure_interface(ctx.manifest, "retrieve_knowledge")?;
    let evidence = ctx.incident.oracle_evidence.clone();
    Ok(ExecutionOutput {
        report: report("C6", &evidence),
        events: vec![
            event(1, "oracle_evidence_loaded", "oracle-evidence-service", json!({
                "evidence_ids": evidence.iter().map(|r| &r.event_id).collect::<Vec<_>>()
            })),
            event(2, "knowledge_retrieved", "knowledge-service", json!({"passages": []})),
        ],
    })
}

fn extract_evidence_ids(jsonl: &str) -> Result<BTreeSet<String>, RunnerError> {
    let mut ids = BTreeSet::new();
    for (index, line) in jsonl.lines().enumerate() {
        if line.trim().is_empty() { continue; }
        let value: Value = serde_json::from_str(line).map_err(|e| {
            RunnerError::Dependency(format!("invalid trajectory JSON at line {}: {e}", index + 1))
        })?;
        if value.get("kind").and_then(Value::as_str) != Some("tool_observation") { continue; }
        if let Some(records) = value.get("payload").and_then(|v| v.get("records")).and_then(Value::as_array) {
            for record in records {
                if let Some(id) = record.get("event_id").and_then(Value::as_str) {
                    ids.insert(id.to_string());
                }
            }
        }
    }
    Ok(ids)
}

#[cfg(test)]
mod tests {
    use super::extract_evidence_ids;

    #[test]
    fn extracts_only_structured_tool_observation_ids() {
        let input = r#"{"kind":"model_output","payload":{"event_id":"ignored"}}
{"kind":"tool_observation","payload":{"records":[{"event_id":"e1"},{"event_id":"e2"}]}}"#;
        let ids = extract_evidence_ids(input).unwrap();
        assert!(ids.contains("e1"));
        assert!(ids.contains("e2"));
        assert!(!ids.contains("ignored"));
    }
}
