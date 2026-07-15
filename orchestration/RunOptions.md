# C0 — Raw LLM
docker compose -f orchestration/Orchestration.yaml run --rm \
  experiment-runner run --condition C0

# C1 — Knowledge-only
docker compose -f orchestration/Orchestration.yaml --profile knowledge run --rm \
  experiment-runner run --condition C1

# C2 — Search-only agent
docker compose -f orchestration/Orchestration.yaml --profile search run --rm \
  experiment-runner run --condition C2

# C3 — Full agent
docker compose -f orchestration/Orchestration.yaml --profile knowledge --profile search run --rm \
  experiment-runner run --condition C3

# C4 — Fixed retrieval
docker compose -f orchestration/Orchestration.yaml --profile fixed-retrieval run --rm \
  experiment-runner run --condition C4

# C5 — Passive matched evidence
docker compose -f orchestration/Orchestration.yaml --profile knowledge --profile matched-evidence run --rm \
  experiment-runner run --condition C5

# C6 — Oracle evidence
docker compose -f orchestration/Orchestration.yaml --profile knowledge --profile oracle-evidence run --rm \
  experiment-runner run --condition C6

# C7 — Oracle plan
docker compose -f orchestration/Orchestration.yaml --profile knowledge --profile search \
  --profile oracle-plan run --rm \
  experiment-runner run --condition C7