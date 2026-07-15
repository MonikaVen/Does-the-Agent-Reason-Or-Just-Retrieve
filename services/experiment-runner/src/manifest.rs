use crate::config::{Capabilities, ExecutionBudgets, InputMode};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RunManifest {
    pub schema_version: String,
    pub run_id: String,
    pub experiment_id: String,
    pub condition: String,
    pub condition_name: String,
    pub incident_id: String,
    pub incident_path: String,
    pub dataset: String,
    pub model: String,
    pub seed: u64,
    pub created_at: DateTime<Utc>,
    pub capabilities: Capabilities,
    pub input_mode: InputMode,
    pub allowed_interfaces: BTreeSet<String>,
    pub budgets: ExecutionBudgets,
    pub matched_source: Option<MatchedSource>,
    pub config_digest_sha256: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MatchedSource {
    pub run_id: String,
    pub condition: String,
    pub manifest_path: String,
    pub trajectory_path: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Incident {
    pub incident_id: String,
    pub alert: serde_json::Value,
    #[serde(default)]
    pub fixed_raw_context: Vec<EvidenceRecord>,
    #[serde(default)]
    pub oracle_evidence: Vec<EvidenceRecord>,
    #[serde(default)]
    pub oracle_plan: Vec<PlanStep>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EvidenceRecord {
    pub event_id: String,
    pub source: String,
    pub timestamp: String,
    pub data: serde_json::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PlanStep {
    pub order: u32,
    pub question: String,
    pub tool: String,
    pub arguments: serde_json::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrajectoryEvent {
    pub sequence: u64,
    pub timestamp: DateTime<Utc>,
    pub kind: String,
    pub service: String,
    pub payload: serde_json::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InvestigationReport {
    pub verdict: String,
    pub confidence: f64,
    pub summary: String,
    pub evidence_ids: Vec<String>,
    pub remaining_uncertainty: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RunResult {
    pub run_id: String,
    pub condition: String,
    pub status: String,
    pub started_at: DateTime<Utc>,
    pub completed_at: DateTime<Utc>,
    pub run_directory: String,
    pub manifest_path: String,
    pub trajectory_path: String,
    pub report_path: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BatchResult {
    pub status: String,
    pub runs: Vec<RunResult>,
}
