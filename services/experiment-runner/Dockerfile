FROM rust:1-bookworm AS builder
WORKDIR /app
COPY Cargo.toml ./
COPY src ./src
RUN cargo build --release

FROM debian:bookworm-slim
RUN useradd --create-home --uid 10001 runner
WORKDIR /app
COPY --from=builder /app/target/release/experiment-runner /usr/local/bin/experiment-runner
COPY configs ./configs
USER runner
ENTRYPOINT ["experiment-runner"]
