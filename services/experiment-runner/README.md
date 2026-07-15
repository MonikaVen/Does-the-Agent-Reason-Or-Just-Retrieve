# Experiment Runner Service

This service is the `experiment-runner` component used by the orchestration stack to execute evaluation conditions.

It is implemented in Rust as a small CLI binary and is built into the Docker service defined in `../orchestration/Orchestration.yaml`.

## Purpose

The experiment runner is responsible for accepting a single experiment condition and executing the corresponding experiment flow.

At present, the service is a minimal scaffold that exposes the CLI contract for the orchestration system.

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

- `run` - required subcommand
- `--condition <CONDITION>` - required experiment condition identifier

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

If this service is later extended to consume structured input, the equivalent JSON request body would be:

```json
{
  "condition": "C0"
}
```

### Output

The current implementation prints a single text line to stdout:

```text
experiment-runner executing condition C0
```

A future version may replace this with structured JSON output such as:

```json
{
  "condition": "C0",
  "status": "started",
  "timestamp": "2026-07-15T00:00:00Z"
}
```

## Docker build

The `Dockerfile` builds the Rust binary in a multi-stage container:

- `rust:1.81-bookworm` builder stage compiles the binary
- `debian:bookworm-slim` runtime image contains only the final executable

## Extension points

This README documents the current scaffold. The service can be extended with:

- richer experiment execution logic
- additional CLI flags for logging, config path, or output destination
- structured stdout / JSON result serialization
- HTTP or gRPC service wrapper for remote orchestration
- database or message queue integration for experiment lifecycle state
