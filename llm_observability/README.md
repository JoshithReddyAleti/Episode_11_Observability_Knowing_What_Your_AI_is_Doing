# 🤖 LLM Observability — Seeing Inside the Model Calls

> *Standard observability watches the pipes. LLM observability watches what actually flows through them — the prompts, the completions, the tokens, the cost.*

---

## What Makes LLM Observability Different (`what_makes_llm_different.py`)

A standard API call is a black box you don't need to see inside: input → output, success or error. An LLM call is a black box you *must* see inside, because:

- The same input produces different outputs (non-determinism)
- The output can be wrong while looking right (silent failure)
- The cost varies per call (token-based)
- The behavior depends on invisible parameters (temperature, model version, system prompt)

LLM observability means capturing the *semantic* layer — the actual content and parameters of every model interaction — not just timing and status.

---

## Prompt Tracking (`prompt_tracking.py`)

Log the actual prompt sent to the model — the full assembled prompt, including system prompt, retrieved context, conversation history, and user query.

**Why:** When a response is bad, the prompt is the first suspect. Was the context relevant? Did the system prompt get truncated? Was there prompt injection in the user input? You can't answer without seeing the exact prompt.

**The caution:** Prompts contain PII. Redact or hash before storing (see structured_logging). For sensitive domains, store a hash for correlation and the redacted version for debugging.

**Track:** prompt template version, assembled prompt (redacted), prompt token count, which context was injected.

---

## Response Tracking (`response_tracking.py`)

Log the model's actual output — the completion text, finish reason, and any structured data.

**Track:** response text (redacted), finish reason (stop / length / content_filter / tool_calls), output token count, whether it was a refusal, response length.

**Why finish_reason matters:** A response truncated because it hit the token limit (`finish_reason: length`) is a different problem than one that completed naturally (`stop`). Users see a cut-off answer; you see the reason.

---

## Token Usage Tracking (`token_usage_tracking.py`)

Tokens are the unit of both cost and context. Track them obsessively.

**Track per request:** input tokens, output tokens, total tokens, and the ratio. A sudden jump in input tokens usually means a prompt template change or context bloat. A jump in output tokens means the model is being more verbose (cost implications).

Tokens are a leading indicator — a token spike precedes a cost spike, often before finance notices.

---

## Model Version Tracking (`model_version_tracking.py`)

**The silent regression source.** Model providers update models behind stable names. "gpt-4o" today may behave differently than "gpt-4o" last month.

**Track:** the exact model string and, where available, the model version/snapshot. When quality changes with no code change, model version is the first thing to check. Pin to versioned snapshots in production (`gpt-4o-2024-11-20`) and track when you migrate.

---

## Temperature and Parameters (`temperature_and_params.py`)

The invisible knobs that change behavior. Track: temperature, top_p, max_tokens, frequency/presence penalties, stop sequences.

**Why:** A response that's suddenly more random or repetitive might be a parameter change, not a model problem. If these aren't logged, you're debugging blind.

---

## Latency Breakdown (`latency_breakdown.py`)

"The LLM call took 2 seconds" is not enough. Break it down:

- **Queue time** — waiting for a slot (rate limiting, connection pool)
- **Time to first token (TTFT)** — how long until generation starts. This is *perceived* latency for streaming.
- **Inter-token latency** — generation speed once started
- **Total generation time** — TTFT + all tokens

TTFT and total time are different problems. High TTFT = provider slow to start (routing, cold start). High total time with low TTFT = long response (many tokens). Each has different fixes.

---

## Streaming Observability (`streaming_observability.py`)

Streaming responses complicate observability — the response arrives token by token, not all at once.

**Track:** time to first token, total streaming duration, tokens streamed, whether the stream completed or was interrupted, and time between tokens (stalls indicate provider issues).

A stream that starts fast but stalls mid-response is a specific failure users hate. You only catch it by measuring inter-token timing.

---

## Function Call Tracing (`function_call_tracing.py`)

When the LLM calls tools/functions, trace each one:

**Track:** which function the model chose, the arguments it generated, whether the arguments were valid, the function's result, and whether the model used the result correctly.

This is the bridge to agent observability. A model that picks the wrong tool or generates malformed arguments is a common, traceable failure.

---

## Error Categorization (`error_categorization.py`)

LLM errors aren't all the same. Categorize them so metrics are meaningful:

- **Rate limit (429)** — provider throttling → retry/fallback
- **Context length exceeded** — prompt too long → truncation needed
- **Content filter** — provider blocked content → policy issue
- **Timeout** — provider too slow → fallback
- **Invalid request** — malformed call → bug
- **Provider outage (5xx)** — provider down → fallback
- **Auth error** — bad key → never transient, alert immediately

Each category has a different response and a different owner. Lumping them into "LLM error" hides actionable signal.

---

## LLM-Specific Dashboards (`llm_specific_dashboards.py`)

The panels every LLM operations dashboard needs:
- Requests/sec and error rate by category
- Token usage (input/output) over time
- Cost per hour and cost per request
- TTFT and total latency percentiles
- Model usage distribution
- Cache hit rate
- Fallback and refusal rates

See [`src/dashboards/`](../dashboards/README.md) for full dashboard designs.

---

## Files in This Directory

| File | What It Covers |
|---|---|
| `what_makes_llm_different.py` | Why the semantic layer matters |
| `prompt_tracking.py` | Capturing the actual prompt (safely) |
| `response_tracking.py` | Completion, finish reason, refusals |
| `token_usage_tracking.py` | The unit of cost and context |
| `model_version_tracking.py` | The silent regression source |
| `temperature_and_params.py` | The invisible behavior knobs |
| `latency_breakdown.py` | Queue, TTFT, generation time |
| `streaming_observability.py` | Token-by-token visibility |
| `function_call_tracing.py` | Tool selection and arguments |
| `error_categorization.py` | Making error metrics actionable |
| `llm_specific_dashboards.py` | The panels that matter |

---

*Previous: [← Distributed Tracing](../distributed_tracing/README.md) · Next: [RAG Observability →](../rag_observability/README.md)*

*Back to [main README](../../README.md)*
