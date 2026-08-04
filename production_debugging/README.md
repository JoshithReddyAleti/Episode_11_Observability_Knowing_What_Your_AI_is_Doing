# 🔧 Production Debugging — Using Observability When It Matters

> *All the instrumentation in the world is worthless if you don't know how to use it under pressure. This is the playbook.*

---

## The Debugging Workflow (`debugging_workflow.md`)

The universal path, backed by the three pillars:
1. **Notice** — an alert fires or a user reports an issue (symptom).
2. **Scope** — is it everyone or one user? One feature or all? One model? (metrics, segmented).
3. **Locate** — find an example trace of the failure. The problem step is usually visually obvious.
4. **Detail** — read that span's attributes/events and the correlated logs for the exact error.
5. **Confirm** — form a hypothesis, verify it against the data.
6. **Fix + verify** — deploy the fix, watch the metric recover.

Metric (scope) → Trace (locate) → Log (detail). Internalize this path; it resolves most incidents.

---

## Trace-First Debugging (`trace_first_debugging.py`)

For AI systems, start from the trace, not the log. The trace shows the whole request flow — retrieval, LLM call, tool calls — in one view, so you immediately see *where* it went wrong before diving into *what* went wrong.

Filter traces by the symptom (high latency, error status, low quality score, high cost), pick a representative one, and read the span tree. This is faster than grepping logs because it preserves structure and causality.

---

## Log Correlation Analysis (`log_correlation_analysis.py`)

Once the trace localizes the problem, use the shared request/trace ID to pull *all* logs for that request. Read them in sequence to reconstruct the exact story — the prompt assembled, the context retrieved, the parameters used, the error thrown.

For patterns across many requests, aggregate logs by a common attribute (all failures with the same error, all requests from the affected tenant) to find what they share.

---

## Metric Correlation (`metric_correlation.py`)

When did the problem start, and what else changed then? Overlay metrics on a timeline:
- Did the latency spike coincide with a deploy? A traffic surge? A model version change? A cost jump?

Correlation on the timeline is often the whole diagnosis: "latency spiked at 14:32, exactly when the deploy went out" points straight at the cause. Annotate deploys and known events on your dashboards to make this instant.

---

## Slow Request Debugging (`slow_request_debugging.py`)

The step-by-step for latency issues:
1. Confirm scope with latency percentiles (is p99 up? for which endpoint/model?).
2. Pull a slow trace. Find the long-pole span.
3. Common culprits: LLM provider slow (high TTFT), retrieval slow (vector search as index grew), serial calls that could be parallel, a retry loop, connection pool exhaustion (saturation).
4. Confirm from span attributes, fix the specific stage.

---

## Hallucination Debugging (`hallucination_debugging.py`)

A user reports a confidently wrong answer. The workflow:
1. Pull the trace for that request.
2. **Check retrieval:** was the correct information retrieved? (RAG observability) If not → retrieval problem.
3. **Check context:** did the correct info make it into the final prompt? If not → reranking/assembly dropped it.
4. **Check generation:** was the info in context but the model contradicted it? → generation/grounding problem (prompt, model, temperature).
5. **Check the source:** was the retrieved info itself wrong? → data quality problem.

Each branch has a different fix. Without RAG/LLM observability, you can't distinguish them.

---

## Cost Spike Debugging (`cost_spike_debugging.py`)

Cost alert fires. The workflow:
1. **Segment** the spike: which user, tenant, feature, or model drove it? (cost attribution)
2. **Common causes:** a prompt template change (input tokens up), a verbosity regression (output tokens up), cache hit rate drop, a retry/agent loop, one abusive user, a model routing change sending traffic to an expensive model.
3. **Confirm** by correlating the cost jump on the timeline with deploys/changes.
4. **Fix:** revert the change, add a limit, fix the cache, block the abuser.

---

## Quality Regression Debugging (`quality_regression_debugging.py`)

Quality metrics dropped. The workflow:
1. **When** did it start? (quality dashboard timeline)
2. **What changed then?** New prompt version? New model version? New retrieval config? Data update? (correlate with change annotations)
3. **Segment:** is it all traffic or a specific feature/model/tenant?
4. **Compare** good-period vs bad-period examples side by side (golden set is ideal here).
5. **Fix + verify** the quality metric recovers.

Model version drift is a frequent, sneaky cause — always check whether the provider updated the model.

---

## Production Debugging Playbook (`production_debugging_playbook.md`)

A consolidated reference: symptom → likely causes → data to check → fix. Covers the common AI incidents (slow, wrong, expensive, degraded, down) as quick-reference runbooks the on-call engineer can follow at 3 AM without thinking from scratch.

---

## Files in This Directory

| File | What It Covers |
|---|---|
| `debugging_workflow.md` | The universal metric→trace→log path |
| `trace_first_debugging.py` | Why traces come first for AI |
| `log_correlation_analysis.py` | Reconstructing the story from logs |
| `metric_correlation.py` | What changed, and when |
| `slow_request_debugging.py` | Latency issues, step by step |
| `hallucination_debugging.py` | Retrieval vs context vs generation |
| `cost_spike_debugging.py` | Finding what drove the cost |
| `quality_regression_debugging.py` | What changed to hurt quality |
| `production_debugging_playbook.md` | Consolidated 3 AM runbooks |

---

*Previous: [← Dashboards](../dashboards/README.md) · Next: [Observability Tools →](../observability_tools/README.md)*

*Back to [main README](../../README.md)*
