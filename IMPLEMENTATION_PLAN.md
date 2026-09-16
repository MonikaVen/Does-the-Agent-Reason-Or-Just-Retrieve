# Implementation Plan: C0–C7 Experimental Agent Platform

This plan translates `Architecture.md`, `README.md`, and the orchestration
files into a build order. It is written against the repository as it exists
today: a complete experimental specification, Compose service graph, and a
Rust experiment-runner that validates C0–C7 configs and writes artifacts
through **reference adapters**, not live services.

The goal is not a generic multi-agent product. It is a **causally
interpretable evaluation platform**: same model, same alert, same output
schema, condition-specific capability isolation, full trajectories, and
counterfactual replay.

---

## 1. Current State

| Area | Status |
|---|---|
| Experimental design and service contracts | Specified in `Architecture.md` |
| Condition activation matrix C0–C7 | Specified; encoded in `services/experiment-runner/configs/conditions.yaml` |
| Compose topology | Declared in `compose.yaml` and `orchestration/Orchestration.yaml` |
| Experiment runner CLI, manifests, JSONL trajectories | Implemented as a local reference harness |
| Live services (`agent-orchestrator`, `model-gateway`, `telemetry-gateway`, …) | **Not present** — Compose builds paths that have no source trees |
| Investigation API, state service, telemetry store, report validator, metrics | Specified, not implemented |
| Versioned knowledge index and incident telemetry datasets | Not in repo (only `incidents/example.yaml`) |
| Replay / trajectory surgery | Specified, not implemented |
| Metrics service | Specified, not implemented |

What the runner already gives us and should be kept:

- Condition catalog with capability flags and `allowed_interfaces`
- Interface-level disablement (`SERVICE_DISABLED` style errors)
- C5 dependency on a completed C3 trajectory
- Immutable `manifest.yaml`, append-only `trajectory.jsonl`, `report.json`
- Config digest hashing and seed / run-id plumbing
- Batch execution for C0–C4, C6, C7 (C5 remains paired)

What must be replaced: `DefaultConditionExecutor` in
`services/experiment-runner/src/executor.rs`. It currently fabricates one
inconclusive report and dummy events. The architecture requires real typed
clients behind the same interface checks.

---

## 2. Design Constraints That Drive the Build Order

These are non-negotiable from the architecture. Implementation choices that
violate them invalidate the experiment.

1. **Causal isolation.** Disabled services are unreachable at the interface,
   not merely omitted from a prompt. A C1 run that can call `query_events`
   is a failed experiment, even if the model never chooses the tool.
2. **Evidence traceability.** Every factual claim cites a stable evidence ID
   that originated in a recorded tool observation of the same run.
3. **Knowledge is not proof.** KB passages are guidance. They never become
   incident evidence IDs.
4. **Read-only, scoped environment.** No write / containment / account
   mutation tools. Every query is bound to incident, time range, and allowed
   sources.
5. **Observable state, not private CoT.** Hypotheses, confidence, evidence
   ledger, and stop rationale are structured and checkpointed.
6. **Pinned evaluation surface.** Model family, decoding parameters, initial
   alert, and final-report schema stay fixed across conditions.
7. **Replay-ready trajectories.** Every step is reconstructible so a later
   intervention can replace one component and rerun downstream execution.
8. **Ground truth is sealed.** Labels, oracle packs, and matched C3 evidence
   constructors are inaccessible to the model, context builder, knowledge
   service, and telemetry gateway.

---

## 3. Target Shape

Four planes, matching Figure 1, plus a condition controller that materializes
the C0–C7 service graph before each run.

```text
Client / experiment-runner
        │
        ▼
investigation-api ──► condition-controller (service manifest + allowlist)
        │
        ▼
┌──────────────── Control plane ────────────────┐
│ orchestrator, context-builder, model-gateway, │
│ state-service, policy-engine                  │
└───────────┬───────────────────┬───────────────┘
            │                   │
            ▼                   ▼
   Knowledge plane        Evidence plane
   knowledge-service      telemetry-gateway
   versioned KB index     typed tools → telemetry-store
            │                   │
            └─────────┬─────────┘
                      ▼
         Reporting / evaluation plane
         report-service → report-validator
         trajectory-service (append-only)
         metrics-service (async / batch)
```

Compose already sketches deployment units. Reconcile names rather than
inventing a second topology:

| Architecture service | Compose / repo name | Notes |
|---|---|---|
| investigation-api + condition controller | `experiment-runner` | Keep as the external entry and run harness |
| agent-orchestrator | `agent-orchestrator` | Adaptive loop for C2/C3/C7 |
| context-builder | `context-builder` | All conditions |
| model-gateway | `model-gateway` | All conditions; pinned model profile |
| state-service | *(missing from Compose)* | Add; required for C2/C3/C7 |
| policy-engine | `policy-engine` | C2/C3/C7; also used to hard-fail disabled tools |
| knowledge-service | `knowledge-service` | Profile `knowledge` |
| telemetry-gateway | `telemetry-gateway` | Profile `search` |
| telemetry-store | *(missing)* | Start as a library/adapter behind the gateway |
| report-service | `report-service` | All conditions |
| report-validator | fold into `report-service` initially | Keep a separate crate/module |
| trajectory-service | `trajectory-store` | Append-only Postgres + files |
| metrics-service | *(missing)* | Batch job; add after real trajectories exist |
| fixed-retrieval executor | `fixed-retrieval-service` | C4 |
| matched-evidence constructor | `matched-evidence-builder` | C5 |
| oracle-evidence provider | `oracle-evidence-service` | C6 |
| oracle-plan provider | `oracle-plan-service` | C7 |

**Prototype rule from §12:** implement logical services as **typed modules
in one process first**, with independent logs and schema validation. Extract
to Docker services when the C3 loop is correct. Do not start by standing up
empty HTTP stubs for every Compose service.

---

## 4. Shared Contracts (do this before any service)

Create a versioned contract package used by runner, orchestrator, and every
gateway. Suggested layout:

```text
contracts/
  schemas/
    investigation-request.json
    agent-decision.json
    investigation-state.json
    policy-decision.json
    knowledge-search.json
    tool-request.json
    tool-observation.json
    final-report.json
    trajectory-event.json
    service-disabled.json
    condition-config.json
    service-manifest.json
    replay-request.json
  tools/
    grep_logs.json
    query_events.json
    find_process_tree.json
    build_timeline.json
    search_related.json
    retrieve_knowledge.json
    submit_report.json
```

Rust crates can generate types from these schemas (or a hand-written
`contracts` crate that is the source of truth and emits JSON Schema). Either
way:

- One `schema_version` per document (`"1.0"` in the architecture examples).
- Deterministic `SERVICE_DISABLED` envelope for every gated interface.
- Evidence IDs assigned only by the telemetry gateway (or matched/oracle
  constructors, which are **not** agent-accessible as tools).
- Report schema identical for every condition.

Also freeze a **model profile** object: model name, version, temperature,
seed policy, max tokens, structured-output schema hash. Store it on every
manifest.

---

## 5. Phased Delivery

Each phase ends with a runnable artifact and an acceptance check. Later
phases must not weaken earlier isolation.

### Phase 0 — Platform skeleton

**Purpose.** Make runs auditable and conditions enforceable before any model
call is interesting.

Work:

1. Extract shared schemas and error envelopes from `Architecture.md` §6 and
   §14.7 into `contracts/`.
2. Expand `RunManifest` to the service-manifest schema in §14.6
   (`service_manifest`, `service_manifest_hash`, `artifact_versions`,
   `source_run`).
3. Implement a `ConditionController` that, given `condition_id`, produces:
   - enabled service set
   - tool allowlist
   - `context_mode`
   - knowledge/search/state/oracle flags
   - Compose profile equivalent (for later Docker runs)
4. Gate every tool and internal client through the allowlist. Disabled calls
   return `SERVICE_DISABLED` and are written to the trajectory **without**
   contacting the model or environment.
5. Postgres schema for runs, events, and state checkpoints (Compose already
   expects `postgres:17` / `agent_eval`). File JSONL remains the researcher-
   facing export.
6. OpenTelemetry (or equivalent) trace ID on every run, propagated into
   trajectory events.
7. Delete or clearly archive `services/experiment-runner-old` so there is
   one runner contract.

**Exit check.** `validate-config` still passes. A dry-run of C0–C7 writes a
manifest whose hash and allowlist match `conditions.yaml`, and a deliberate
`query_events` call under C0/C1 fails with `SERVICE_DISABLED`.

### Phase 1 — C0 vertical slice (raw LLM)

**Purpose.** Prove the reporting plane and pinned model path with no search
and no knowledge.

Active path: experiment-runner → context-builder (`fixed_raw`) →
model-gateway → report-service → report-validator → trajectory-store.

Work:

1. **Context builder:** six-layer assembler, but for C0 only system policy,
   incident alert, the fixed raw-log window, and the report schema. No tool
   schemas. Truncation and token accounting recorded in trajectory metadata.
2. **Model gateway:** one provider adapter, structured output required,
   `AgentDecision` unused; C0 asks for a `FinalReport` directly (or a
   constrained “synthesize now” decision). Pin decoding parameters. Never
   pass datastore credentials.
3. **Report service:** map model output onto §6.8. One constrained repair
   pass if validation fails; **cannot add evidence**.
4. **Report validator:** schema completeness, verdict vocabulary
   (`malicious` | `benign` | `inconclusive`), confidence in `[0,1]`,
   evidence-ID existence against the C0 context window, ATT&CK syntax,
   citation coverage. Unsupported claims fail the run or are counted, never
   silently dropped.
5. Replace the reference C0 executor with these clients. Keep the CLI.

**Exit check.** One incident, pinned seed, produces `report.json` that
validates, cites only IDs present in `fixed_raw_context`, and a trajectory
that reconstructs prompt layers, model metadata, and validator outcome.

### Phase 2 — C1 (knowledge-only)

**Purpose.** Isolate external knowledge from adaptive search.

Work:

1. Knowledge corpus loader: versioned ATT&CK, Sigma metadata, detection
   guidance, investigation playbooks. Store `source_id`, `source_version`,
   `category` (`declarative` | `detection` | `procedural`), `index_version`.
2. `POST /internal/knowledge/search` (or in-process equivalent): question,
   `corpus_tags`, `top_k`.
3. Context builder adds retrieved passages in a delimited untrusted-data
   region (prompt-injection control from §9).
4. Register `retrieve_knowledge` only when the condition allowlist includes
   it. C0 must still fail if the model emits that tool.
5. Record index version, chunking policy, embedding model (if any), and
   `top_k` on the manifest.

**Exit check.** C1 run includes knowledge events; C0 binary with the same
incident cannot retrieve passages. Passages never appear as `evidence_id`s
in the report.

### Phase 3 — Evidence plane and C2/C3 adaptive loop

**Purpose.** This is the core agent and the hardest phase. C3 is the
complete adaptive agent; C2 is C3 with knowledge unplugged.

Work, in this order:

1. **Telemetry store.** Read-only adapters for process, identity, network,
   file, registry, and cloud audit data. Physical or logical separation of
   ground-truth labels. Incident scope token required on every query.
2. **Telemetry gateway** implementing the five search tools:

   | Tool | Discriminative job |
   |---|---|
   | `grep_logs` | lexical search |
   | `query_events` | structured filter / aggregate |
   | `find_process_tree` | entity pivot |
   | `build_timeline` | temporal synthesis |
   | `search_related` | multi-hop relations |

   Assign stable evidence IDs here. Normalize records to the observation
   envelope in §6.7. Enforce `max_records`, timeout, and source allowlist.
3. **Policy engine.** Allow / normalize / reject. Tool allowlist, incident
   scope, time range, result limits, query syntax, read-only. Rejected
   actions become trajectory events; the orchestrator may retry within
   budget or stop.
4. **State service.** `CreateState` from alert only (`s0` has no telemetry
   and no knowledge). `ApplyStatePatch` for hypotheses, confidence (with
   previous/new values), known and contradicting evidence, unresolved
   questions, entities, timeline, knowledge references, budgets, stop
   state. `CreateCheckpoint` before and after every action. Contradicting
   evidence cannot disappear without an explicit patch and rationale.
5. **Context builder (agent mode):** policy + alert + tool schemas +
   structured state + recent observations + (C3 only) knowledge. Dedup and
   token-budget allocation.
6. **Model gateway (agent mode):** structured `AgentDecision` (§6.2):
   hypotheses, known/contradicting evidence, next question, selected
   action, expected discrimination, stop flag.
7. **Orchestrator loop** (§5):

   ```text
   create run → s0
   loop:
     build context → generate decision
     if stop or budget exhausted: break
     validate action → execute knowledge or telemetry
     record observation → apply state patch
   generate + validate report
   finalize trajectory
   ```

   Budgets: `max_tool_calls`, `max_records_per_call`, `max_runtime_seconds`,
   `max_model_tokens`. Hard stop on exhaustion even if `stop=false`.
8. Wire C2 (knowledge client absent) and C3 (both knowledge and search).

**Exit check.**

- C2 cannot call `retrieve_knowledge`.
- C3 can call both knowledge and telemetry.
- Every report citation resolves to a `tool_observation` in the same run.
- Re-running a prefix with pinned model + seed reproduces checkpoint state
  within documented stochastic limits.
- No tool writes or reads outside incident scope.

### Phase 4 — C4, C5, C6, C7 providers

These conditions exist to **ablate** adaptivity, query choice, evidence
selection, and planning. Implement only after C3 trajectories are real;
C5 is defined in terms of C3.

**C4 Fixed retrieval**

- Analyst query pack (versioned YAML): ordered telemetry queries + fixed
  knowledge retrieval.
- Deterministic executor runs the pack before any model call.
- Model receives passive context; tool schemas are not registered.
- Store query-pack version and returned evidence IDs on the manifest.

**C5 Passive matched evidence**

- Require a completed C3 source run with ≥1 retrieved evidence record.
- Zero-evidence C3 runs are reported separately, never backfilled.
- Constructor copies evidence records, strips tool names and search order,
  reorders, and supplies them with knowledge passages as passive context.
- Telemetry gateway and adaptive loop are not registered.

**C6 Oracle evidence**

- Expert-minimal decisive telemetry set + enabled knowledge context.
- Store oracle artifact id, authorship, review status, minimality-review
  metadata.
- Search and adaptive state disabled.

**C7 Oracle plan**

- Expert investigation plan injected via `load_oracle_plan`.
- Adaptive loop, state, knowledge, and tools remain on.
- Agent may adapt arguments and beliefs but starts from the oracle plan.
- Store plan artifact metadata like C6.

**Exit check.** Service-manifest hashes differ across C3–C7 as specified in
§14.1. Disabled interfaces fail closed. C5 refuses to start without a
valid C3 source.

### Phase 5 — Replay and causal metrics

**Purpose.** Answer the paper’s causal questions. Do not compute “reasoning”
from chain-of-thought text.

**Trajectory service / replay** (`Architecture.md` §11):

- Reconstruct a trajectory prefix.
- Apply one intervention: `plan_repair`, `query_repair`,
  `knowledge_ablation`, `observation_swap`, `evidence_ablation`,
  `state_repair`, `stop_repair`, `synthesis_repair`.
- Rerun downstream execution with paired seeds, `preserve_prefix=true`,
  `hide_original_final_answer=true`.
- A repaired report cannot cite evidence removed by the intervention.

**Metrics service** (batch, not in the hot loop):

| Family | Examples | Applicable when |
|---|---|---|
| Outcome | incident accuracy, macro-F1, calibration | all conditions |
| Evidence | precision/recall, unsupported-claim rate | all conditions |
| Process | useful-query rate, stopping quality, belief-update | C2/C3/C7 |
| Fixed-query efficiency | C4 only | C4 |
| Plan adherence / planning bottleneck | C7 only | C7 |
| Causal | CRG, evidence dependence, adaptive dependency | replay-enabled runs |

Undefined metrics for a condition are **N/A**, never zero.

**Exit check.** One query-repair replay on a C3 run changes downstream
actions without leaking the original final answer. Metrics tables emit N/A
for C0 adaptive-dependency.

### Phase 6 — Dataset, orchestration, and split deployments

Work:

1. Incident dataset format: alert, scoped telemetry partitions, sealed
   ground truth, optional C4 query pack, C6 oracle evidence, C7 oracle plan,
   counterfactual twin linkage (same alert, different truth).
2. Align root `compose.yaml` and `orchestration/Orchestration.yaml` (they
   currently duplicate). Keep profiles from `orchestration/RunOptions.md`.
3. Add missing Compose units: `state-service`, `metrics-service` (batch),
   telemetry volume/store. Secrets already anticipated (`postgres_password`).
4. Split out process boundaries in the order §12 recommends: model gateway,
   knowledge service, telemetry gateway, trajectory store, metrics.
5. Network isolation: `telemetry` and `knowledge` networks stay internal;
   the model never reaches those stores directly.

---

## 6. Control Loop and Module Responsibilities

Use the architecture RPCs as module APIs even while in-process.

| Module | API | Must guarantee |
|---|---|---|
| Investigation / runner | `POST /v1/investigations`, GET run + trajectory | Validates condition + incident; no reasoning |
| Orchestrator | `StartRun`, `NextStep`, `ExecuteAction`, `StopRun` | Budget + stop enforcement |
| Context builder | `BuildContext` | Bounded, layered, truncation logged |
| Model gateway | `GenerateDecision` | Pinned model; structured output or `ModelError` |
| State service | `CreateState`, `GetState`, `ApplyStatePatch`, `CreateCheckpoint` | Alert-only s0; explicit patches |
| Policy engine | `ValidateAction` | Allow / normalize / reject |
| Knowledge | `POST /internal/knowledge/search` | Versioned passages, never evidence |
| Telemetry | `POST /internal/tools/{tool}` | IDs, scope, read-only |
| Report | `POST /internal/reports/generate` | No new evidence on repair |
| Validator | `POST /internal/reports/validate` | Deterministic |
| Trajectory | `POST /internal/trajectory/events`, `POST /internal/replay` | Append-only |
| Metrics | `POST /internal/metrics/evaluate` | Condition-aware applicability |

---

## 7. Data and Safety Implementation Notes

**Evidence IDs.** Minted once at observation time. Format should be stable
across replays of the same underlying record (`event-1021` style), not a
random UUID per call, so C5 matching and evidence ablation stay well-defined.

**State invariants to enforce in code, not comments:**

- Citation → observation → provenance chain
- Confidence updates log previous and new values
- Knowledge references stored separately from `known_evidence`
- Ground-truth fields absent from any struct the model or tools can see

**Prompt-injection.** Telemetry bodies and KB text wrapped in explicit
delimiters and labeled untrusted. Tool schemas and policy live outside that
region.

**Budgets.** Enforce in the orchestrator *and* again in the telemetry
gateway. Defense in depth so a buggy loop cannot dump the store.

---

## 8. Testing Strategy

Tests should protect experimental validity, not just code health.

1. **Contract tests.** Every request/response fixture in `Architecture.md`
   §6 round-trips the schema.
2. **Isolation tests.** For each condition, assert the disabled interface
   set from §14.1 returns `SERVICE_DISABLED` before any model/environment
   I/O. Table-drive this from `conditions.yaml` so catalog and tests cannot
   drift.
3. **Traceability tests.** Synthetic C3 run: tamper with a citation that
   has no observation → validator reject.
4. **C5 pairing tests.** Missing C3, non-C3 source, and zero-evidence C3
   each fail or route to the separate reporting path as specified.
5. **Replay tests.** Prefix reconstruction; each intervention type applied
   on a fixture trajectory; hidden original answer.
6. **Scope tests.** Query for another incident’s host or outside the time
   window is rejected by policy.
7. **Golden CLI tests.** Extend `services/experiment-runner/tests/cli.rs`
   beyond `validate-config` to C0–C7 dry-runs against `incidents/example.yaml`.

No browser or UI verification applies to this platform. Verification is CLI
runs, schema validation, and trajectory inspection.

---

## 9. Recommended Implementation Sequence (summary)

Build in this order so each step is a valid experiment, not a dangling
service:

1. Contracts + condition controller + trajectory/manifest completeness
2. C0: context → model → report → validate
3. C1: knowledge service
4. Telemetry store + gateway + policy + state + orchestrator → C2 then C3
5. C4 query pack, C5 matcher, C6/C7 oracles
6. Replay interventions
7. Metrics batch + dataset scale-out + Compose split

The existing experiment-runner remains the outer harness throughout.
Replace `DefaultConditionExecutor` incrementally (C0 first, then C1, …)
rather than rewriting the CLI.

---

## 10. Explicit Non-Goals for the First Complete C3

- Autonomous response, containment, or ticket writing
- Unrestricted web browsing or live production telemetry
- Multi-model routing or “best of N” decoding inside a condition
- Treating chain-of-thought as a reasoning metric
- HTTP service sprawl before the in-process C3 loop is correct

---

## 11. Acceptance Criteria Mapping

From `Architecture.md` §13, owned by the phases above:

| Criterion | Phase that proves it |
|---|---|
| Versioned schema validation | 0–1 |
| Evidence traceability | 3 |
| Isolation / read-only scope | 0 and 3 |
| State reproducibility | 3 |
| Replay without leaking the original answer | 5 |
| Single trace ID across services | 0, retained through 6 |
| C3 condition fidelity (KB + adaptive search, no oracle) | 3 |

When Phase 3 is done, the platform can run the paper’s primary contrast
(C0/C1 vs C2/C3). Phases 4–5 unlock the remaining causal claims.
