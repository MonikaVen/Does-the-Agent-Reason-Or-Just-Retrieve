use crate::config::{load_yaml, validate_catalog, ConditionCatalog, ConditionDefinition, ExperimentConfig};
use crate::error::RunnerError;
use crate::executor::{ConditionExecutor, DefaultConditionExecutor, ExecutionContext};
use crate::manifest::{BatchResult, Incident, MatchedSource, RunManifest, RunResult, TrajectoryEvent};
use crate::storage::RunStorage;
use chrono::Utc;
use serde::Serialize;
use sha2::{Digest, Sha256};
use std::path::{Path, PathBuf};
use std::process;
use std::time::{SystemTime, UNIX_EPOCH};

pub struct Runner {
    experiment: ExperimentConfig,
    catalog: ConditionCatalog,
}

pub struct RunRequest {
    pub condition: String,
    pub incident_path: PathBuf,
    pub seed: u64,
    pub matched_run: Option<PathBuf>,
    pub explicit_run_id: Option<String>,
    pub overwrite: bool,
}

pub struct BatchRequest {
    pub conditions: Vec<String>,
    pub incident_path: PathBuf,
    pub repetitions: Option<u32>,
    pub seed_start: u64,
    pub overwrite: bool,
}

impl Runner {
    pub fn load(experiment_path: &Path, conditions_path: &Path) -> Result<Self, RunnerError> {
        let runner = Self {
            experiment: load_yaml(experiment_path)?,
            catalog: load_yaml(conditions_path)?,
        };
        runner.validate_all()?;
        Ok(runner)
    }

    pub fn validate_all(&self) -> Result<(), RunnerError> {
        if self.experiment.schema_version != "1" {
            return Err(RunnerError::Config(format!(
                "unsupported experiment schema version '{}'", self.experiment.schema_version
            )));
        }
        if self.experiment.defaults.repetitions == 0 {
            return Err(RunnerError::Config("defaults.repetitions must be greater than zero".into()));
        }
        validate_catalog(&self.catalog)
    }

    pub fn condition(&self, id: &str) -> Result<&ConditionDefinition, RunnerError> {
        self.catalog.conditions.get(id).ok_or_else(|| RunnerError::UnknownCondition(id.into()))
    }

    pub fn run(&self, request: RunRequest) -> Result<RunResult, RunnerError> {
        let started_at = Utc::now();
        let definition = self.condition(&request.condition)?.clone();
        let incident: Incident = load_yaml(&request.incident_path)?;
        let matched_source = self.resolve_dependency(&request.condition, &definition, request.matched_run.as_deref())?;

        let run_id = request.explicit_run_id.unwrap_or_else(|| {
            generate_run_id(&request.condition)
        });
        let storage = RunStorage::create(
            Path::new(&self.experiment.artifacts.output_root), &run_id, request.overwrite
        )?;

        let manifest = RunManifest {
            schema_version: "1".into(),
            run_id: run_id.clone(),
            experiment_id: self.experiment.experiment_id.clone(),
            condition: request.condition.clone(),
            condition_name: definition.name.clone(),
            incident_id: incident.incident_id.clone(),
            incident_path: request.incident_path.display().to_string(),
            dataset: self.experiment.dataset.clone(),
            model: self.experiment.model.clone(),
            seed: request.seed,
            created_at: started_at,
            capabilities: definition.capabilities.clone(),
            input_mode: definition.input_mode.clone(),
            allowed_interfaces: definition.allowed_interfaces.clone(),
            budgets: self.experiment.defaults.clone(),
            matched_source: matched_source.clone(),
            config_digest_sha256: config_digest(&self.experiment, &definition)?,
        };

        let manifest_path = storage.write_manifest(&manifest)?;
        storage.append_trajectory(&TrajectoryEvent {
            sequence: 0,
            timestamp: Utc::now(),
            kind: "run_started".into(),
            service: "experiment-runner".into(),
            payload: serde_json::json!({
                "run_id": run_id, "condition": request.condition, "seed": request.seed
            }),
        })?;

        let output = DefaultConditionExecutor.execute(&ExecutionContext {
            manifest: &manifest,
            incident: &incident,
            matched_source: matched_source.as_ref(),
        })?;
        for event in &output.events {
            storage.append_trajectory(event)?;
        }
        validate_report(&manifest, &output.report)?;
        let report_path = storage.write_report(&output.report)?;
        let trajectory_path = storage.run_dir.join("trajectory.jsonl");

        let result = RunResult {
            run_id: manifest.run_id.clone(),
            condition: manifest.condition.clone(),
            status: "completed".into(),
            started_at,
            completed_at: Utc::now(),
            run_directory: storage.run_dir.display().to_string(),
            manifest_path: manifest_path.display().to_string(),
            trajectory_path: trajectory_path.display().to_string(),
            report_path: report_path.display().to_string(),
        };
        storage.write_json("result.json", &result)?;
        Ok(result)
    }

    pub fn run_batch(&self, request: BatchRequest) -> Result<BatchResult, RunnerError> {
        if request.conditions.is_empty() {
            return Err(RunnerError::Config("run-batch requires at least one condition".into()));
        }
        if request.conditions.iter().any(|id| id == "C5") {
            return Err(RunnerError::Dependency(
                "C5 must be run separately with --matched-run pointing to C3 artifacts".into(),
            ));
        }

        let repetitions = request.repetitions.unwrap_or(self.experiment.defaults.repetitions);
        if repetitions == 0 {
            return Err(RunnerError::Config("repetitions must be greater than zero".into()));
        }

        let mut runs = Vec::new();
        for condition in &request.conditions {
            self.condition(condition)?;
            for repetition in 0..repetitions {
                let seed = request.seed_start + repetition as u64;
                runs.push(self.run(RunRequest {
                    condition: condition.clone(),
                    incident_path: request.incident_path.clone(),
                    seed,
                    matched_run: None,
                    explicit_run_id: Some(format!(
                        "{}-{}-r{}-s{}",
                        condition.to_lowercase(), sanitize_id(&request.incident_path), repetition, seed
                    )),
                    overwrite: request.overwrite,
                })?);
            }
        }
        Ok(BatchResult { status: "completed".into(), runs })
    }

    fn resolve_dependency(
        &self,
        condition_id: &str,
        definition: &ConditionDefinition,
        matched_run: Option<&Path>,
    ) -> Result<Option<MatchedSource>, RunnerError> {
        if condition_id != "C5" {
            if matched_run.is_some() {
                return Err(RunnerError::Dependency("--matched-run is valid only for C5".into()));
            }
            return Ok(None);
        }

        let path = matched_run.ok_or_else(|| {
            RunnerError::Dependency("C5 requires --matched-run <C3 run directory>".into())
        })?;
        let manifest_path = if path.is_dir() { path.join("manifest.yaml") } else { path.to_path_buf() };
        let source_manifest: RunManifest = load_yaml(&manifest_path)?;
        if source_manifest.condition != "C3" {
            return Err(RunnerError::Dependency(format!(
                "C5 source must be C3, found {}", source_manifest.condition
            )));
        }
        let trajectory_path = manifest_path.parent()
            .ok_or_else(|| RunnerError::Dependency("invalid matched manifest path".into()))?
            .join("trajectory.jsonl");
        if !trajectory_path.exists() {
            return Err(RunnerError::Dependency(format!(
                "matched C3 trajectory does not exist: {}", trajectory_path.display()
            )));
        }
        let declared = definition.depends_on.as_ref().ok_or_else(|| {
            RunnerError::Dependency("C5 definition has no dependency declaration".into())
        })?;
        if declared.condition != "C3" {
            return Err(RunnerError::Dependency("C5 dependency declaration is not C3".into()));
        }

        Ok(Some(MatchedSource {
            run_id: source_manifest.run_id,
            condition: source_manifest.condition,
            manifest_path: manifest_path.display().to_string(),
            trajectory_path: trajectory_path.display().to_string(),
        }))
    }
}

fn validate_report(manifest: &RunManifest, report: &crate::manifest::InvestigationReport) -> Result<(), RunnerError> {
    if !matches!(report.verdict.as_str(), "malicious" | "benign" | "inconclusive") {
        return Err(RunnerError::Workflow(format!("invalid verdict '{}'", report.verdict)));
    }
    if !(0.0..=1.0).contains(&report.confidence) {
        return Err(RunnerError::Workflow("confidence must be between 0 and 1".into()));
    }
    if !manifest.allowed_interfaces.contains("submit_report") {
        return Err(RunnerError::Workflow("submit_report is disabled".into()));
    }
    Ok(())
}

fn config_digest<T: Serialize, U: Serialize>(a: &T, b: &U) -> Result<String, RunnerError> {
    let bytes = serde_json::to_vec(&(a, b))?;
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    Ok(format!("{:x}", hasher.finalize()))
}

fn sanitize_id(path: &Path) -> String {
    path.file_stem().and_then(|v| v.to_str()).unwrap_or("incident")
        .chars().map(|c| if c.is_ascii_alphanumeric() { c } else { '-' }).collect()
}

fn generate_run_id(condition: &str) -> String {
    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_nanos();
    format!("{}-{}-{}", condition.to_lowercase(), process::id(), timestamp)
}
