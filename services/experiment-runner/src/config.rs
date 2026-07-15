use crate::error::RunnerError;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ExecutionBudgets {
    pub repetitions: u32,
    pub maximum_model_calls: u32,
    pub maximum_tool_calls: u32,
    pub maximum_records_per_call: u32,
    pub maximum_runtime_seconds: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ArtifactConfig {
    pub output_root: String,
    pub save_model_inputs: bool,
    pub save_tool_results: bool,
    pub save_state_history: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExperimentConfig {
    pub schema_version: String,
    pub experiment_id: String,
    pub dataset: String,
    pub model: String,
    pub defaults: ExecutionBudgets,
    pub artifacts: ArtifactConfig,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Capabilities {
    pub knowledge_access: bool,
    pub adaptive_search: bool,
    pub structured_state: bool,
    pub fixed_retrieval: bool,
    pub passive_matched_evidence: bool,
    pub oracle_evidence: bool,
    pub oracle_plan: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum InputMode {
    FixedRawContext,
    InitialAlert,
    DeterministicRetrieval,
    MatchedC3Evidence,
    OracleEvidence,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ConditionDependency {
    pub condition: String,
    pub artifact: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConditionDefinition {
    pub name: String,
    pub capabilities: Capabilities,
    pub input_mode: InputMode,
    #[serde(default)]
    pub allowed_interfaces: BTreeSet<String>,
    #[serde(default)]
    pub depends_on: Option<ConditionDependency>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConditionCatalog {
    pub schema_version: String,
    pub conditions: BTreeMap<String, ConditionDefinition>,
}

pub fn load_yaml<T: for<'de> Deserialize<'de>>(path: &Path) -> Result<T, RunnerError> {
    let text = fs::read_to_string(path).map_err(|e| RunnerError::io(path, e))?;
    Ok(serde_yaml::from_str(&text)?)
}

pub fn validate_catalog(catalog: &ConditionCatalog) -> Result<(), RunnerError> {
    let required: BTreeSet<String> = (0..=7).map(|n| format!("C{n}")).collect();
    let actual: BTreeSet<String> = catalog.conditions.keys().cloned().collect();
    if actual != required {
        return Err(RunnerError::Config(format!(
            "condition catalog must contain exactly C0-C7; found {actual:?}"
        )));
    }

    for (id, condition) in &catalog.conditions {
        validate_condition(id, condition)?;
    }
    Ok(())
}

fn validate_condition(id: &str, condition: &ConditionDefinition) -> Result<(), RunnerError> {
    let has = |name: &str| condition.allowed_interfaces.contains(name);
    if condition.capabilities.knowledge_access != has("retrieve_knowledge") {
        return Err(RunnerError::Config(format!(
            "{id}: knowledge_access must match retrieve_knowledge"
        )));
    }

    let search = ["grep_logs", "query_events", "find_process_tree", "build_timeline", "search_related"];
    if condition.capabilities.adaptive_search != search.iter().any(|name| has(name)) {
        return Err(RunnerError::Config(format!(
            "{id}: adaptive_search must match telemetry interfaces"
        )));
    }

    if condition.capabilities.fixed_retrieval != has("execute_fixed_retrieval") {
        return Err(RunnerError::Config(format!("{id}: fixed-retrieval mismatch")));
    }
    if condition.capabilities.oracle_evidence != has("load_oracle_evidence") {
        return Err(RunnerError::Config(format!("{id}: oracle-evidence mismatch")));
    }
    if condition.capabilities.oracle_plan != has("load_oracle_plan") {
        return Err(RunnerError::Config(format!("{id}: oracle-plan mismatch")));
    }
    if !has("submit_report") {
        return Err(RunnerError::Config(format!("{id}: submit_report must be enabled")));
    }

    if id == "C5" {
        let dependency = condition.depends_on.as_ref().ok_or_else(|| {
            RunnerError::Config("C5 must declare its C3 trajectory dependency".into())
        })?;
        if dependency.condition != "C3" || dependency.artifact != "trajectory" {
            return Err(RunnerError::Config(
                "C5 dependency must be condition=C3 and artifact=trajectory".into(),
            ));
        }
    } else if condition.depends_on.is_some() {
        return Err(RunnerError::Config(format!("{id}: only C5 may declare a dependency")));
    }

    Ok(())
}
