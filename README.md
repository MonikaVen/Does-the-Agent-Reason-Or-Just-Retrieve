# Does the Agent Reason, or Just Retrieve?

Paper code for evaluating whether AI agents genuinely reason over evidence during cybersecurity incident investigations or primarily benefit from retrieval, context selection, and system scaffolding.

![Does the Agent Reason, or Just Retrieve?](/images/AIAgentReasoningIntro.png)

## Introduction

Large language model agents are increasingly used for cybersecurity investigations. These systems can retrieve security knowledge, search telemetry, construct attack timelines, update hypotheses, and produce incident reports.

However, strong end-to-end performance does not reveal **why** an agent succeeds.

A tool-augmented system may produce the correct result because:

- the underlying model already knows the answer;
- a knowledge base provides useful terminology or investigation guidance;
- retrieval exposes the decisive evidence;
- deterministic scaffolding encodes an expert workflow;
- the agent adaptively selects informative actions;
- the agent updates its hypotheses in response to new evidence.

This project introduces a causal evaluation framework for separating these explanations.

The central research question is:

> **Does the agent reason over evidence, or does it just retrieve useful context?**

The runnable lab is Python. Upload typed agent data (alert, telemetry,
knowledge, C4/C6/C7 packs), pin Ollama or a cloud model (GPT, Claude, Grok,
Groq) with a local API key, regenerate the architecture graph, and download
experiment code. See [`platform/README.md`](platform/README.md).

```bash
cd platform
python3 -m pip install -r requirements.txt
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Rather than treating generated explanations or chain-of-thought text as proof of reasoning, the framework evaluates observable behavior:

1. whether the agent selects actions that distinguish competing hypotheses;
2. whether its beliefs change when the evidence changes;
3. whether later actions depend on earlier observations;
4. whether its final conclusion depends on the evidence it cites.

---

## Research Objectives

The evaluation addresses five primary questions:

1. Does adaptive telemetry search improve performance beyond passive access to the same evidence?
2. Does external security knowledge improve evidence discovery or mainly improve terminology and ATT&CK mapping?
3. Which trajectory components causally determine investigation success?
4. Do agentic gains generalize to counterfactual incidents and unseen attack procedures?
5. Does the agent correctly identify the cause of its own failures?

---

## Main Paper Idea

The framework decomposes observed agent performance into four capability dimensions:

| Capability | Description |
|---|---|
| **Parametric knowledge** | Security knowledge already encoded in the language model. |
| **External knowledge retrieval** | Access to ATT&CK, Sigma rules, detection guidance, and investigation playbooks. |
| **Adaptive evidence acquisition** | The ability to issue informative telemetry queries and pivot based on observations. |
| **Stateful reasoning and revision** | The ability to maintain hypotheses, update confidence, track evidence, and decide when to stop. |

The experimental design varies these capabilities while keeping the underlying language model, initial alert, decoding settings, and output schema fixed wherever possible.

---

## Methodology Overview

```mermaid
flowchart LR
    A["Counterfactual Incident Twins<br/>Same initial alert<br/>Different ground truth"] -->
    B["Experimental Conditions<br/>C0–C7"]

    B --> C["Investigation Execution"]

    C --> D["Trajectory Recorder<br/>Plans<br/>Queries<br/>Tool calls<br/>Knowledge passages<br/>Observations<br/>Belief updates<br/>Final report"]

    D --> E["Trajectory Surgery<br/>Replace or remove one component"]

    E --> F["Counterfactual Replay<br/>Replay downstream execution<br/>across repeated runs"]

    F --> G["Causal Attribution<br/>Measure changes in outcome probability"]

    G --> H["Evaluation Results<br/>Performance<br/>Evidence quality<br/>Process quality<br/>Causal effects<br/>Robustness"]

    classDef source fill:#eef4ff,stroke:#2457a7,stroke-width:2px;
    classDef condition fill:#eef9ee,stroke:#2e7d32,stroke-width:2px;
    classDef execution fill:#f4efff,stroke:#6d28d9,stroke-width:2px;
    classDef intervention fill:#fff0f0,stroke:#c62828,stroke-width:2px;
    classDef result fill:#fff8e7,stroke:#b7791f,stroke-width:2px;

    class A source;
    class B condition;
    class C,D execution;
    class E,F intervention;
    class G,H result;
