use std::path::PathBuf;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum RunnerError {
    #[error("configuration error: {0}")]
    Config(String),
    #[error("unknown condition '{0}'; expected one of C0-C7")]
    UnknownCondition(String),
    #[error("condition dependency error: {0}")]
    Dependency(String),
    #[error("workflow error: {0}")]
    Workflow(String),
    #[error("run directory already exists: {0}")]
    RunExists(PathBuf),
    #[error("I/O error at {path}: {source}")]
    Io { path: PathBuf, #[source] source: std::io::Error },
    #[error("YAML error: {0}")]
    Yaml(#[from] serde_yaml::Error),
    #[error("JSON error: {0}")]
    Json(#[from] serde_json::Error),
}

impl RunnerError {
    pub fn io(path: impl Into<PathBuf>, source: std::io::Error) -> Self {
        Self::Io { path: path.into(), source }
    }

    pub fn exit_code(&self) -> i32 {
        match self {
            Self::Config(_) | Self::UnknownCondition(_) => 2,
            Self::Dependency(_) => 3,
            Self::Workflow(_) => 4,
            Self::RunExists(_) => 5,
            _ => 1,
        }
    }
}
