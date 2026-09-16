# Implementation Plan: Visible C0–C7 Lab (Python)

The experimental design in `Architecture.md` is unchanged. What changed is
the delivery: **ignore the Rust harness**, implement the platform in Python,
and make the architecture itself the user interface.

The research question is still: does the agent reason over evidence, or just
retrieve useful context? A hidden pipeline cannot answer that. The lab has
to show, for every condition, which services are actually on, which action
was chosen, why, what evidence came back, and how beliefs moved.

---

## Architecture idea: the diagram is the product

A conventional “upload / spinner / chat transcript” UI would hide the only
thing this project cares about. The straightforward design is a **glass
cockpit** over the four planes in Figure 1.

```text
Upload incident pack  →  Telemetry store (read-only, scoped)
Pick C0–C7            →  Condition controller lights/greys each service
Start run             →  Orchestrator walks the loop
Every service call    →  Trajectory event (SSE) + node pulse + stage tick
State + report        →  Always on screen, cited evidence must exist
```

Why this is the right shape:

1. **Straightforward.** One FastAPI process. Modules map 1:1 onto
   `Architecture.md` services. No broker, no empty Docker stubs.
2. **Transparent.** Disabled tools return `SERVICE_DISABLED` at the
   interface. The frontend greys those nodes *before* the run, so isolation
   is visible, not merely asserted.
3. **Followable.** Progress is not a percentage bar. It is the 11-stage
   loop from §5, the live service graph, the expected-discrimination text
   on each decision, and the evidence ledger filling in.

Swap the model later (real LLM behind `model-gateway`) without changing the
cockpit. The reference investigator is pinned, structured, and honest about
not being an LLM.

---

## What is implemented now (`platform/`)

| Piece | Role |
|---|---|
| FastAPI investigation API | Upload datasets, create runs, stream events |
| Condition controller | C0–C7 allowlists + architecture view for the UI |
| Orchestrator | Adaptive loop (C2/C3/C7) and one-shot paths (C0/C1/C4/C5/C6) |
| Context builder | Layered, bounded prompts; telemetry/KB marked untrusted |
| Model gateway | `ReferenceInvestigator` — structured decisions + reports |
| State / policy / knowledge / telemetry | Real typed modules, not stubs |
| Report validator | Verdict vocab, citations must be in this run’s ledger |
| Frontend lab | Condition rail, data passport, live four-plane canvas, trajectory, state, report |

Data in is an incident pack: `incident_id`, `alert`, `telemetry.{source}[]`
with stable `event_id`s. Optional `fixed_query_pack`, `oracle_evidence`,
`oracle_plan`. Uploaded JSON *is* the telemetry store. Ground truth never
enters those records.

---

## Remaining work (still required for the paper)

The cockpit is the first complete slice. It does not yet replace every
section of `Architecture.md`.

1. **Pinned LLM adapter** in `model-gateway` — **done** for Ollama, GPT,
   Claude, Grok, and Groq, plus a reference investigator. Cloud keys are
   stored locally and never written into trajectories.
2. **Replay / trajectory surgery** (§11): prefix reconstruct, one
   intervention, hide original final answer, paired seeds.
3. **Metrics service** (§4.13 / §14.8): outcome metrics for all
   conditions; process metrics only when those services ran; N/A not zero.
4. **Counterfactual incident twins** and a larger sealed dataset.
5. **Split deployments** only after the in-process C3 loop and replay are
   correct. Compose profiles in `orchestration/RunOptions.md` remain the
   target topology.

Do not start by wrapping the old Rust CLI or standing up empty HTTP
services for every Compose name.

---

## How to run

```bash
cd platform
python3 -m pip install -r requirements.txt pytest pytest-asyncio
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open `http://127.0.0.1:8000`. A sample encoded-PowerShell incident is
preloaded. Upload another JSON pack, select a condition (the graph updates
immediately), start a run, and watch the trajectory.

C5 requires a completed C3 run on the same dataset.

---

## Design constraints (unchanged from the architecture)

- Disabled services are unreachable, not merely omitted from a prompt.
- Knowledge passages are never evidence IDs.
- Every factual claim cites an observation from the same run.
- Environment is read-only and incident-scoped.
- Observable state, not private chain-of-thought.
- Ground truth, oracle packs, and C5 matching stay sealed from the model.
