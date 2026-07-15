use std::process::Command;

#[test]
fn validate_config_command_succeeds() {
    let binary = env!("CARGO_BIN_EXE_experiment-runner");
    let status = Command::new(binary)
        .args(["validate-config"])
        .status()
        .expect("failed to launch binary");
    assert!(status.success());
}
