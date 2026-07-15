use crate::error::RunnerError;
use crate::manifest::{InvestigationReport, RunManifest, TrajectoryEvent};
use serde::Serialize;
use std::fs::{self, OpenOptions};
use std::io::Write;
use std::path::{Path, PathBuf};

pub struct RunStorage {
    pub run_dir: PathBuf,
}

impl RunStorage {
    pub fn create(output_root: &Path, run_id: &str, overwrite: bool) -> Result<Self, RunnerError> {
        let run_dir = output_root.join(run_id);
        if run_dir.exists() {
            if overwrite {
                fs::remove_dir_all(&run_dir).map_err(|e| RunnerError::io(&run_dir, e))?;
            } else {
                return Err(RunnerError::RunExists(run_dir));
            }
        }
        fs::create_dir_all(&run_dir).map_err(|e| RunnerError::io(&run_dir, e))?;
        Ok(Self { run_dir })
    }

    pub fn write_manifest(&self, manifest: &RunManifest) -> Result<PathBuf, RunnerError> {
        let path = self.run_dir.join("manifest.yaml");
        fs::write(&path, serde_yaml::to_string(manifest)?)
            .map_err(|e| RunnerError::io(&path, e))?;
        let mut permissions = fs::metadata(&path).map_err(|e| RunnerError::io(&path, e))?.permissions();
        permissions.set_readonly(true);
        fs::set_permissions(&path, permissions).map_err(|e| RunnerError::io(&path, e))?;
        Ok(path)
    }

    pub fn append_trajectory(&self, event: &TrajectoryEvent) -> Result<PathBuf, RunnerError> {
        let path = self.run_dir.join("trajectory.jsonl");
        let mut file = OpenOptions::new().create(true).append(true).open(&path)
            .map_err(|e| RunnerError::io(&path, e))?;
        writeln!(file, "{}", serde_json::to_string(event)?)
            .map_err(|e| RunnerError::io(&path, e))?;
        file.sync_data().map_err(|e| RunnerError::io(&path, e))?;
        Ok(path)
    }

    pub fn write_report(&self, report: &InvestigationReport) -> Result<PathBuf, RunnerError> {
        self.write_json("report.json", report)
    }

    pub fn write_json<T: Serialize>(&self, filename: &str, value: &T) -> Result<PathBuf, RunnerError> {
        let path = self.run_dir.join(filename);
        fs::write(&path, serde_json::to_vec_pretty(value)?)
            .map_err(|e| RunnerError::io(&path, e))?;
        Ok(path)
    }
}
