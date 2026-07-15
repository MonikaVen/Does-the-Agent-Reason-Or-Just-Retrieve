FROM rust:1.81-bookworm AS builder
WORKDIR /app

COPY Cargo.toml ./
COPY src ./src

RUN cargo build --release

FROM debian:bookworm-slim
WORKDIR /app
COPY --from=builder /app/target/release/experiment-runner /usr/local/bin/experiment-runner
ENTRYPOINT ["/usr/local/bin/experiment-runner"]
