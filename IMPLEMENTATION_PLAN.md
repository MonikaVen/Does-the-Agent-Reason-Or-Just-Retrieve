# Implementation Plan: C0–C7 Lab (Python, CLI)

The experimental design in `Architecture.md` is unchanged. Delivery is a
Python experiment runner with **no frontend**. Isolation is visible on the
terminal (`python -m app architecture C3`) and in the trajectory log.

The research question is still: does the agent reason over evidence, or just
retrieve useful context?

```text
Load incident pack     →  Telemetry store (read-only, scoped)
Pick C0–C7             →  Condition controller enable/disable each service
python -m app run C3   →  Orchestrator walks the loop
Every service call     →  Trajectory line on stdout + SQLite events
python -m app suite    →  experiment-report.md for the whole matrix
```

1. **Straightforward.** One in-process Python lab. Modules map 1:1 onto
   `Architecture.md` services. No browser, no broker, no empty Docker stubs.
2. **Transparent.** Disabled tools return `SERVICE_DISABLED` at the
   interface. `architecture` prints which services are on before a run.
3. **Followable.** Progress is the 11-stage loop from §5 printed as events,
   plus expected-discrimination text on each decision.

---

## What is implemented now (`platform/`)

| Piece | Role |
|---|---|
| CLI (`python -m app`) | load packs, run one condition or C0–C7, write report |
| Condition controller | C0–C7 allowlists + architecture dump |
| Orchestrator | Adaptive loop (C2/C3/C7) and one-shot paths (C0/C1/C4/C5/C6) |
| Context builder | Layered, bounded prompts; telemetry/KB marked untrusted |
| Model gateway | Ollama (default, local), plus GPT / Claude / Grok / Groq adapters and a reference investigator |
| State / policy / knowledge / telemetry | Real typed modules, not stubs |
| Report validator | Verdict vocab, citations must be in this run’s ledger |
| Experiment report | `platform/reports/experiment-report.md` from a sequential C0–C7 suite |

---

## Remaining work (still required for the paper)

1. **Pinned LLM adapter** — **done** for Ollama, GPT, Claude, Grok, Groq, and a reference investigator.
2. **Replay / trajectory surgery** (§11).
3. **Metrics service** (§4.13 / §14.8).
4. **Counterfactual incident twins** and a larger sealed dataset.

---

## How to run

```bash
cd platform
python3 -m pip install -r requirements.txt
python3 -m app suite --provider ollama --model llama3.2:1b
python3 -m app run C3 --provider reference
python3 -m app architecture C0
```

C5 requires a completed C3 run on the same dataset (the suite wires this).

---

## Design constraints (unchanged from the architecture)

- Disabled services are unreachable, not merely omitted from a prompt.
- Knowledge passages are never evidence IDs.
- Every factual claim cites an observation from the same run.
- Environment is read-only and incident-scoped.
- Observable state, not private chain-of-thought.
- Ground truth, oracle packs, and C5 matching stay sealed from the model.
- No silent fallback from Ollama to the reference investigator.
