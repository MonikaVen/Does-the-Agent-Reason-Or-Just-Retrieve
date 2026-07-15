mod config;
mod error;
mod executor;
mod manifest;
mod runner;
mod storage;

use error::RunnerError;
use runner::{BatchRequest, RunRequest, Runner};
use std::env;
use std::path::PathBuf;

/// Reproducible C0-C7 experiment runner.
///
/// The runner resolves a condition from YAML configuration, validates its
/// permissions and dependencies, writes an immutable run manifest, executes
/// the condition workflow, and stores all artifacts.
struct Cli {
    experiment: PathBuf,
    conditions: PathBuf,
    command: Command,
}

enum Command {
    ValidateConfig,
    Run {
        condition: String,
        incident: PathBuf,
        seed: u64,
        matched_run: Option<PathBuf>,
        run_id: Option<String>,
        overwrite: bool,
    },
    RunBatch {
        conditions: Vec<String>,
        incident: PathBuf,
        repetitions: Option<u32>,
        seed_start: u64,
        overwrite: bool,
    },
    ShowCondition {
        condition: String,
    },
}

fn main() {
    if let Err(error) = real_main() {
        eprintln!("error: {error}");
        std::process::exit(error.exit_code());
    }
}

fn real_main() -> Result<(), RunnerError> {
    let cli = parse_cli(env::args())?;
    let runner = Runner::load(&cli.experiment, &cli.conditions)?;

    match cli.command {
        Command::ValidateConfig => {
            runner.validate_all()?;
            println!("{}", serde_json::json!({"status": "valid"}));
        }
        Command::ShowCondition { condition } => {
            println!("{}", serde_json::to_string_pretty(runner.condition(&condition)?)?);
        }
        Command::Run { condition, incident, seed, matched_run, run_id, overwrite } => {
            let result = runner.run(RunRequest {
                condition,
                incident_path: incident,
                seed,
                matched_run,
                explicit_run_id: run_id,
                overwrite,
            })?;
            println!("{}", serde_json::to_string_pretty(&result)?);
        }
        Command::RunBatch { conditions, incident, repetitions, seed_start, overwrite } => {
            let result = runner.run_batch(BatchRequest {
                conditions,
                incident_path: incident,
                repetitions,
                seed_start,
                overwrite,
            })?;
            println!("{}", serde_json::to_string_pretty(&result)?);
        }
    }

    Ok(())
}

fn parse_cli<I, S>(args: I) -> Result<Cli, RunnerError>
where
    I: IntoIterator<Item = S>,
    S: Into<String>,
{
    let values: Vec<String> = args.into_iter().map(Into::into).collect();
    if values.len() < 2 {
        return Err(RunnerError::Config("expected a subcommand".into()));
    }

    let mut experiment = PathBuf::from("configs/experiment.yaml");
    let mut conditions = PathBuf::from("configs/conditions.yaml");
    let mut idx = 1;

    while idx < values.len() {
        let token = values[idx].as_str();
        if token == "--experiment" {
            if idx + 1 >= values.len() {
                return Err(RunnerError::Config("--experiment requires a path".into()));
            }
            experiment = PathBuf::from(values[idx + 1].clone());
            idx += 2;
        } else if token == "--conditions" {
            if idx + 1 >= values.len() {
                return Err(RunnerError::Config("--conditions requires a path".into()));
            }
            conditions = PathBuf::from(values[idx + 1].clone());
            idx += 2;
        } else {
            break;
        }
    }

    let command = match values.get(idx).map(|value| value.as_str()) {
        Some("validate-config") => Command::ValidateConfig,
        Some("show-condition") => {
            let condition = values.get(idx + 1).cloned().ok_or_else(|| {
                RunnerError::Config("show-condition requires a condition name".into())
            })?;
            Command::ShowCondition { condition }
        }
        Some("run") => parse_run_command(&values[idx + 1..])?,
        Some("run-batch") => parse_run_batch_command(&values[idx + 1..])?,
        Some(other) if !other.starts_with('-') => Command::Run {
            condition: other.to_string(),
            incident: PathBuf::from("incidents/example.yaml"),
            seed: 0,
            matched_run: None,
            run_id: None,
            overwrite: false,
        },
        Some(other) => return Err(RunnerError::Config(format!("unsupported subcommand '{other}'"))),
        None => return Err(RunnerError::Config("expected a subcommand".into())),
    };

    Ok(Cli { experiment, conditions, command })
}

fn parse_run_command(args: &[String]) -> Result<Command, RunnerError> {
    let mut condition = None;
    let mut incident = None;
    let mut seed = 0u64;
    let mut matched_run = None;
    let mut run_id = None;
    let mut overwrite = false;

    let mut idx = 0;
    while idx < args.len() {
        match args[idx].as_str() {
            "--condition" => {
                condition = Some(args.get(idx + 1).cloned().ok_or_else(|| {
                    RunnerError::Config("--condition requires a value".into())
                })?);
                idx += 2;
            }
            "--incident" => {
                incident = Some(PathBuf::from(args.get(idx + 1).cloned().ok_or_else(|| {
                    RunnerError::Config("--incident requires a path".into())
                })?));
                idx += 2;
            }
            "--seed" => {
                seed = args.get(idx + 1).ok_or_else(|| RunnerError::Config("--seed requires a value".into()))?.parse::<u64>().map_err(|_| RunnerError::Config("--seed must be a number".into()))?;
                idx += 2;
            }
            "--matched-run" => {
                matched_run = Some(PathBuf::from(args.get(idx + 1).cloned().ok_or_else(|| {
                    RunnerError::Config("--matched-run requires a path".into())
                })?));
                idx += 2;
            }
            "--run-id" => {
                run_id = Some(args.get(idx + 1).cloned().ok_or_else(|| {
                    RunnerError::Config("--run-id requires a value".into())
                })?);
                idx += 2;
            }
            "--overwrite" => {
                overwrite = true;
                idx += 1;
            }
            other => return Err(RunnerError::Config(format!("unsupported option '{other}' for run"))),
        }
    }

    Ok(Command::Run {
        condition: condition.ok_or_else(|| RunnerError::Config("run requires --condition".into()))?,
        incident: incident.ok_or_else(|| RunnerError::Config("run requires --incident".into()))?,
        seed,
        matched_run,
        run_id,
        overwrite,
    })
}

fn parse_run_batch_command(args: &[String]) -> Result<Command, RunnerError> {
    let mut conditions = Vec::new();
    let mut incident = None;
    let mut repetitions = None;
    let mut seed_start = 0u64;
    let mut overwrite = false;

    let mut idx = 0;
    while idx < args.len() {
        match args[idx].as_str() {
            "--conditions" => {
                let values = args.get(idx + 1).cloned().ok_or_else(|| {
                    RunnerError::Config("--conditions requires a value".into())
                })?;
                conditions.extend(values.split(',').filter(|value| !value.is_empty()).map(str::to_string));
                idx += 2;
            }
            "--incident" => {
                incident = Some(PathBuf::from(args.get(idx + 1).cloned().ok_or_else(|| {
                    RunnerError::Config("--incident requires a path".into())
                })?));
                idx += 2;
            }
            "--repetitions" => {
                repetitions = Some(args.get(idx + 1).ok_or_else(|| RunnerError::Config("--repetitions requires a value".into()))?.parse::<u32>().map_err(|_| RunnerError::Config("--repetitions must be a number".into()))?);
                idx += 2;
            }
            "--seed-start" => {
                seed_start = args.get(idx + 1).ok_or_else(|| RunnerError::Config("--seed-start requires a value".into()))?.parse::<u64>().map_err(|_| RunnerError::Config("--seed-start must be a number".into()))?;
                idx += 2;
            }
            "--overwrite" => {
                overwrite = true;
                idx += 1;
            }
            other => return Err(RunnerError::Config(format!("unsupported option '{other}' for run-batch"))),
        }
    }

    if conditions.is_empty() {
        return Err(RunnerError::Config("run-batch requires --conditions".into()));
    }

    Ok(Command::RunBatch {
        conditions,
        incident: incident.ok_or_else(|| RunnerError::Config("run-batch requires --incident".into()))?,
        repetitions,
        seed_start,
        overwrite,
    })
}
