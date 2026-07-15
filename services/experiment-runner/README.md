# Experiment Runner

Commented Rust reference implementation for C0-C7.

## Build

```bash
cargo test
cargo build --release
```

## Validate

```bash
cargo run -- validate-config
```

## Run C3 and C5

```bash
cargo run -- run --condition C3 --incident incidents/example.yaml --seed 100 --run-id c3-example
cargo run -- run --condition C5 --incident incidents/example.yaml --seed 100 --matched-run runs/c3-example --run-id c5-example
```

## Run a batch

```bash
cargo run -- run-batch --conditions C0,C1,C2,C3,C4,C6,C7 --incident incidents/example.yaml --repetitions 3 --seed-start 100
```

C5 is separate because each C5 run must reference a specific completed C3 trajectory.

## Artifacts

```text
runs/<run-id>/
├── manifest.yaml
├── trajectory.jsonl
├── report.json
└── result.json
```

`src/executor.rs` contains deterministic reference adapters. Replace them with real model, knowledge, telemetry, oracle, and fixed-retrieval clients while retaining the interface checks and trajectory format.
