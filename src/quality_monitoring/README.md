# ✅ Quality Monitoring — Catching Silent Degradation

> *A 200 status code means the request succeeded. It says nothing about whether the answer was any good. That gap is where AI quietly fails.*

---

## The Problem This Solves

Episode 8 taught offline evaluation — testing quality before deploy. But models drift, data changes, and prompts get edited. Quality that was great at deploy time can degrade silently in production. Quality monitoring is offline evaluation's production counterpart: continuously measuring whether real responses are actually good.

---

## Online Evaluation (`online_evaluation.py`)

Evaluate real production responses, continuously, as they happen (or on a sample).

Unlike offline eval (fixed test set, before deploy), online eval runs on live traffic. It catches issues that only appear with real user queries — the distribution of production inputs is always different from your test set.

**Approach:** Sample production requests, run evaluators (LLM-as-judge, heuristics, reference-free metrics) on them, and track the scores as time-series metrics. A dropping score triggers investigation.

---

## User Feedback Loops (`user_feedback_loops.py`)

The most direct quality signal: what users tell you. Capture and structure it.

**Explicit feedback:** thumbs up/down, star ratings, "report this response," corrections. Track rates and correlate with request attributes (which model, which feature, which prompt version scored worse).

Feedback is gold but sparse — most users never rate. Combine with implicit signals below.

---

## Thumbs Up/Down Tracking (`thumbs_up_down_tracking.py`)

The workhorse feedback mechanism. Track the thumbs-down rate as a core quality metric.

**Key practice:** correlate thumbs-down with everything else you observe. A thumbs-down rate that jumps for one model version, one feature, or after one prompt change points directly at the cause. Segment the metric by model, feature, tenant, and prompt version.

---

## Implicit Feedback Signals (`implicit_feedback_signals.py`)

Users vote with behavior even when they don't click a button:
- **Regeneration** — they asked for a different answer (dissatisfaction)
- **Copy** — they copied the response (satisfaction)
- **Follow-up rephrasing** — they re-asked differently (the first answer failed)
- **Abandonment** — they left mid-conversation (frustration)
- **Conversation length** — very short can mean quick success or quick giving-up

Implicit signals are abundant where explicit feedback is scarce. Together they give a fuller quality picture.

---

## Quality Drift Detection (`quality_drift_detection.py`)

Detect gradual quality decline over time — the kind no single response reveals.

**Track:** rolling averages of quality scores (online eval, feedback) and alert on a sustained downward trend. Quality drift is slow and silent; by the time users complain loudly, it's been degrading for weeks. Trend detection catches it early. (Statistical methods in [`src/drift_detection/`](../drift_detection/README.md).)

---

## Regression Detection (`regression_detection.py`)

Catch quality drops caused by *changes* — a new prompt, a new model version, a new retrieval config.

**Approach:** compare quality metrics before and after each change. A/B or before/after comparison on quality scores reveals whether a "safe" change actually hurt quality. This is what stops a well-intentioned prompt tweak from silently degrading production.

---

## LLM-as-Judge Online (`llm_as_judge_online.py`)

Use a strong LLM to grade production responses in real time (or on a sample). Episode 8 covered the technique; here it runs continuously in production.

**Track:** judge scores as metrics, segmented by feature/model/prompt. Watch for the judge's known biases (position, verbosity, self-preference — Episode 8) and calibrate. Online LLM-as-judge scales quality measurement far beyond what human review could — but sample and cost-control it (it's LLM calls that cost money).

---

## Golden Set Monitoring (`golden_set_monitoring.py`)

Maintain a curated set of representative queries with known-good answers. Run them against production regularly (e.g., hourly/daily).

**Why:** The golden set is a constant. If production answers to the golden set change or degrade, something in your system changed — even if you didn't deploy anything (model version drift, data changes). It's a canary for silent regressions, and unlike live traffic, it's stable enough to compare over time.

---

## Output Length Anomalies (`output_length_anomalies.py`)

Response length is a cheap, powerful quality proxy. Track its distribution.

**Signals:** responses suddenly much shorter (truncation, refusals, model change) or much longer (verbosity regression, prompt loop, cost implications). A shift in the length distribution often precedes a quality complaint and is trivially cheap to monitor.

---

## Refusal Rate Tracking (`refusal_rate_tracking.py`)

How often does the model decline to answer? Track the refusal rate carefully.

**Why it matters both ways:** A *rising* refusal rate can mean the model got more conservative (a version change), your content is triggering safety filters, or users are asking harder questions. A *falling* refusal rate can mean safety guardrails weakened. Either direction is a signal. Segment by feature and model to localize the cause.

---

## Files in This Directory

| File | What It Covers |
|---|---|
| `online_evaluation.py` | Evaluating live production responses |
| `user_feedback_loops.py` | Capturing explicit feedback |
| `thumbs_up_down_tracking.py` | The workhorse metric, correlated |
| `implicit_feedback_signals.py` | Behavior as quality signal |
| `quality_drift_detection.py` | Catching gradual decline |
| `regression_detection.py` | Catching change-induced drops |
| `llm_as_judge_online.py` | Continuous LLM grading |
| `golden_set_monitoring.py` | The canary for silent regressions |
| `output_length_anomalies.py` | Length as a cheap quality proxy |
| `refusal_rate_tracking.py` | When the model says no |

---

*Previous: [← Cost Observability](../cost_observability/README.md) · Next: [Drift Detection →](../drift_detection/README.md)*

*Back to [main README](../../README.md)*
