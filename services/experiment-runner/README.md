# Experiment Runner Service

This service is the `experiment-runner` component used by the orchestration stack to execute evaluation conditions.

It is implemented in Rust as a small CLI binary and is built into the Docker service defined in `../orchestration/Orchestration.yaml`.

## Purpose

The experiment runner accepts a single experiment condition and produces a structured execution event for downstream orchestration.

This version implements the future contract described in the documentation: the service now emits structured JSON instead of plain text.

## Build & Run

### Local development

From `services/experiment-runner`:

```bash
cargo test
cargo run -- run --condition C0
```

### Docker

From the repository root:

```bash
docker compose -f orchestration/Orchestration.yaml run --rm experiment-runner run --condition C0
```

This uses the service definition in `orchestration/Orchestration.yaml`.

## Service interface

The service exposes a CLI interface only.

### Command

```bash
experiment-runner run --condition <CONDITION>
```

### Parameters

- `run` — required subcommand
- `--condition <CONDITION>` — required experiment condition identifier

### Example

```bash
experiment-runner run --condition C0
```

### Exit codes

- `0` — success
- `2` — invalid arguments or missing `--condition`

## Data schema

The current input schema is simple and defined by the Rust `Config` struct.

```rust
struct Config {
    condition: String,
}
```

### JSON equivalent

If the service is represented as structured input, the equivalent JSON request body is:

```json
{
  "condition": "C0"
}
```

## Output schema

The service now emits structured JSON to stdout.

```json
{
  "condition": "C0",
  "status": "started",
  "timestamp": "2026-07-15T00:00:00Z"
}
```

### Response fields

- `condition` — the requested experiment condition
- `status` — the execution state, currently `started`
- `timestamp` — the UTC start time in ISO 8601 format

## Implementation details

`src/main.rs` now serializes a `RunResponse` struct using `serde_json` and uses `chrono` to generate the timestamp.

## Docker build

The `Dockerfile` builds the Rust binary in a multi-stage container:

- `rust:1.81-bookworm` builder stage compiles the binary
- `debian:bookworm-slim` runtime image contains only the final executable

## Extension points

This README documents the current future-ready scaffold. The service can be extended with:

- richer experiment execution logic
- additional CLI flags for logging, config path, or output destination
- HTTP or gRPC service wrapper for remote orchestration
- database or message queue integration for experiment lifecycle state
