# 📝 Structured Logging — Making Events Queryable

> *Logs you can't query are just a wall of text. Structured logging turns events into data.*

---

## The Core Shift

**Unstructured (useless at scale):**
```python
print(f"User {user_id} sent a request that used {tokens} tokens")
# Output: "User abc123 sent a request that used 847 tokens"
```

**Structured (queryable):**
```python
logger.info("chat_request", extra={
    "user_id": "abc123",
    "tokens": 847,
    "model": "gpt-4o-mini",
    "cost_usd": 0.003,
    "latency_ms": 850,
    "request_id": "req_xyz789",
})
```

The second is JSON. You can query it: *"show me all requests where tokens > 5000 AND model = gpt-4o"* becomes one filter, not a regex nightmare across gigabytes of text.

**This single change is the highest-leverage observability improvement you can make.** Everything else builds on queryable events.

---

## JSON Logging Basics (`json_logging_basics.py`)

Every log line is a JSON object with consistent fields:

```json
{
  "timestamp": "2026-07-27T14:32:05.123Z",
  "level": "INFO",
  "event": "chat_request",
  "service": "chat-api",
  "environment": "production",
  "request_id": "req_xyz789",
  "user_id": "abc123",
  "message": "Chat request completed",
  "tokens": 847,
  "cost_usd": 0.003,
  "latency_ms": 850
}
```

**Required fields on every log:** timestamp, level, event, service, environment, request_id. These make logs correlatable and filterable. Everything else is context-specific.

---

## Log Levels and When to Use Them (`log_levels_and_when.py`)

Levels are not decoration. They control volume, cost, and alertability.

- **DEBUG** — detailed diagnostic info. Off in production by default (too much volume/cost). Turn on temporarily to investigate.
- **INFO** — normal operations worth recording. Request completed, job started. The default for business events.
- **WARNING** — something unexpected but handled. Fell back to backup model. Retry succeeded on attempt 2.
- **ERROR** — something failed that shouldn't. A request errored. A tool call failed permanently.
- **CRITICAL** — the system itself is in danger. Database unreachable. All LLM providers down.

**AI-specific guidance:** A hallucination is not an ERROR (the system worked as designed). It's a *quality signal* — track it as a metric, not a log level. Reserve ERROR for actual failures.

---

## Contextual Logging (`contextual_logging.py`)

Context should attach automatically, not be passed manually to every log call.

**The problem:** You want every log within a request to include the request_id, user_id, and tenant_id — without threading them through every function.

**The solution:** Context-local storage (Python's `contextvars`). Set the context once at the start of a request; every log within that request inherits it automatically.

```python
# Set once at request start
set_log_context(request_id="req_123", user_id="abc", tenant_id="acme")

# Every log below automatically includes all three — no manual passing
logger.info("retrieval_started")   # includes request_id, user_id, tenant_id
logger.info("llm_call_complete")   # includes them too
```

This is what makes logs from a single request stitchable across dozens of functions.

---

## Request ID Propagation (`request_id_propagation.py`)

The single most important field in your logs. A request ID (correlation ID) links every log, metric, and trace from one user request.

**The flow:**
1. Request arrives → generate a unique request_id (or accept one from an upstream service)
2. Attach it to the logging context
3. Pass it downstream (to the LLM gateway, database calls, other services) via headers
4. Every log everywhere includes it
5. When debugging, filter by one request_id → see the entire journey

Without request IDs, logs from concurrent requests interleave into meaningless noise. With them, you can isolate one user's exact experience.

---

## User ID Tracking (`user_id_tracking.py`)

Attach user (and tenant) identity to logs — carefully.

**Why:** "User X reports bad answers" becomes debuggable when you can filter to that user's requests.

**The caution:** User IDs can be PII depending on your scheme. Use opaque internal IDs, never emails or names, in logs. Map to real identity only in a secure, access-controlled system.

---

## Sensitive Data Redaction (`sensitive_data_redaction.py`)

**The AI-specific landmine.** Prompts and responses often contain PII, secrets, or confidential data. Logging them naively is a compliance disaster.

**Redaction strategies:**
- **Pattern-based:** Regex for emails, phone numbers, SSNs, credit cards, API keys → replace with `[REDACTED_EMAIL]`
- **Entity-based:** NER model detects names, locations, organizations → redact
- **Allowlist:** Only log fields you've explicitly approved as safe
- **Hashing:** Log a hash of sensitive values so you can correlate without exposing

**Rule:** Redact at the logging layer, before data leaves your process. Never rely on redacting downstream — by then it's already in transit and at rest.

```python
def redact(text: str) -> str:
    text = EMAIL_PATTERN.sub("[EMAIL]", text)
    text = SSN_PATTERN.sub("[SSN]", text)
    text = CREDIT_CARD_PATTERN.sub("[CC]", text)
    text = API_KEY_PATTERN.sub("[KEY]", text)
    return text
```

---

## Log Sampling Strategies (`log_sampling_strategies.py`)

At scale, logging every request is expensive. Sampling reduces volume while keeping signal.

- **Head sampling:** Decide at request start whether to log (e.g., log 10% of requests). Simple, but you might miss the rare failure.
- **Tail sampling:** Log everything to a buffer, decide at the end whether to keep it. Keep 100% of errors, 1% of successes. Best signal-to-cost ratio.
- **Adaptive sampling:** Sample more during incidents, less during calm. Dynamic rate based on error rate.

**AI-specific rule:** Always keep 100% of: errors, high-cost requests, low-quality-scored responses, and flagged content. Sample the boring successful requests.

---

## Async Logging (`async_logging.py`)

Logging must never block the request. Writing a log line to disk or shipping it over the network takes milliseconds — multiply by thousands of requests and it becomes a latency source.

**The pattern:** Logs go to an in-memory queue instantly; a background worker ships them to the backend. The request never waits for the log to be persisted.

Every production logging library (structlog, loguru with enqueue, standard logging with QueueHandler) supports this. Use it.

---

## Log Correlation (`log_correlation.py`)

The payoff of everything above: linking logs across services and pillars.

**Within a request:** All logs share a request_id → reconstruct the full request.

**Across services:** The request_id propagates via headers → follow a request through microservices.

**Across pillars:** The same request_id appears in the trace and is queryable from a metric spike → jump from "latency spiked" to "here are the exact slow requests" to "here's what they logged."

This correlation is what turns three separate data streams into one coherent picture.

---

## Files in This Directory

| File | What It Covers |
|---|---|
| `json_logging_basics.py` | Structured JSON log format |
| `log_levels_and_when.py` | DEBUG through CRITICAL, used correctly |
| `contextual_logging.py` | Automatic context via contextvars |
| `request_id_propagation.py` | The correlation ID (most important field) |
| `user_id_tracking.py` | Identity without PII leaks |
| `sensitive_data_redaction.py` | Redacting PII from prompts/responses |
| `log_sampling_strategies.py` | Head, tail, adaptive sampling |
| `async_logging.py` | Never block the request |
| `log_correlation.py` | Linking across requests, services, pillars |

---

*Previous: [← Foundations](../foundations/README.md) · Next: [Metrics →](../metrics/README.md)*

*Back to [main README](../../README.md)*
