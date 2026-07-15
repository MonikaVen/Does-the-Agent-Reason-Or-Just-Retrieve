use chrono::Utc;
use serde::Serialize;
use std::env;

#[derive(Debug, PartialEq, Eq)]
struct Config {
    condition: String,
}

#[derive(Serialize)]
struct RunResponse {
    condition: String,
    status: String,
    timestamp: String,
}

fn parse_args<I, S>(args: I) -> Result<Config, String>
where
    I: IntoIterator<Item = S>,
    S: Into<String>,
{
    let mut values = args.into_iter().map(Into::into);
    let _exe = values.next();

    match values.next().as_deref() {
        Some("run") => {
            let mut condition = None;
            while let Some(arg) = values.next() {
                match arg.as_str() {
                    "--condition" => {
                        condition = values.next();
                    }
                    _ => return Err(format!("unexpected argument: {arg}")),
                }
            }

            let condition = condition.ok_or_else(|| "missing --condition argument".to_string())?;
            Ok(Config { condition })
        }
        Some(other) => Err(format!("unsupported subcommand: {other}")),
        None => Err("missing subcommand: expected 'run'".to_string()),
    }
}

fn build_response(config: Config) -> RunResponse {
    RunResponse {
        condition: config.condition,
        status: "started".to_string(),
        timestamp: Utc::now().to_rfc3339_opts(chrono::SecondsFormat::Secs, true),
    }
}

fn main() {
    match parse_args(env::args()) {
        Ok(config) => {
            let response = build_response(config);
            let json = serde_json::to_string(&response).expect("failed to serialize response");
            println!("{json}");
        }
        Err(err) => {
            eprintln!("error: {err}");
            std::process::exit(2);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{build_response, parse_args};

    #[test]
    fn parses_condition_from_run_command() {
        let config = parse_args(["experiment-runner", "run", "--condition", "C0"]).unwrap();
        assert_eq!(config.condition, "C0");
    }

    #[test]
    fn rejects_missing_condition() {
        let err = parse_args(["experiment-runner", "run"]).unwrap_err();
        assert_eq!(err, "missing --condition argument");
    }

    #[test]
    fn builds_json_response() {
        let config = parse_args(["experiment-runner", "run", "--condition", "C1"]).unwrap();
        let response = build_response(config);

        assert_eq!(response.condition, "C1");
        assert_eq!(response.status, "started");
        assert!(response.timestamp.ends_with('Z'));
    }
}
