# 🔗 Distributed Tracing — Following a Request Through the System

> *A metric says "something is slow." A trace says "it's the reranker, on line 4, taking 1.8 seconds." Traces are how you find the where.*

---

## Traces, Spans, and Context (`traces_spans_context.py`)

Three concepts you must internalize:

**Span** — a single unit of work with a start time, end time, and metadata. "The LLM call." "The database query." "The retrieval step."

**Trace** — the full tree of spans for one request. The root span (the whole request) contains child spans (each step), which may contain their own children.

**Context** — the thread that links spans together. It carries the trace ID and current span ID so that when one function calls another, the child span knows its parent.

```
Trace: chat_request (2000ms)                    [root span]
├── authenticate (10ms)                          [child]
├── rate_limit_check (5ms)                        [child]
├── retrieve_context (300ms)                      [child]
│   ├── embed_query (50ms)                        [grandchild]
│   ├── vector_search (200ms)                     [grandchild]
│   └── rerank (50ms)                             [grandchild]
├── llm_call (1650ms)                             [child]  ← the bottleneck
└── format_response (5ms)                         [child]
```

One glance at this tree tells you the LLM call dominates. No guessing.

---

## OpenTelemetry Fundamentals (`opentelemetry_fundamentals.py`)

OpenTelemetry (OTel) is the open standard for observability. It's vendor-neutral: instrument once, send to any backend (Jaeger, Tempo, Datadog, Honeycomb, LangSmith).

**Why it matters:** Before OTel, every observability vendor had proprietary SDKs. Switch vendors → rewrite all instrumentation. OTel decouples instrumentation from backend. This is why it won.

The OTel pipeline:
```
Your code (instrumented with OTel SDK)
  → OTel Collector (receives, processes, batches)
  → Backend(s) of your choice
```

---

## OTel Python SDK (`otel_python_sdk.py`)

Setting up tracing in a Python app:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="otel-collector:4317"))
)
tracer = trace.get_tracer(__name__)
```

`BatchSpanProcessor` batches spans and ships them asynchronously — never blocking your request. This is critical: tracing must not add latency.

---

## Automatic Instrumentation (`automatic_instrumentation.py`)

The fastest way to get value. OTel provides auto-instrumentation for common libraries — FastAPI, requests, httpx, SQLAlchemy, Redis — that creates spans without you writing any tracing code.

```python
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

FastAPIInstrumentor.instrument_app(app)   # every HTTP request auto-traced
HTTPXClientInstrumentor().instrument()     # every outbound call auto-traced
```

Start here. You get 80% of the value with near-zero effort. Then add manual spans for your business logic.

---

## Manual Span Creation (`manual_span_creation.py`)

Auto-instrumentation traces the plumbing. Manual spans trace *your logic* — the retrieval, the reranking, the agent reasoning.

```python
async def retrieve_context(query: str):
    with tracer.start_as_current_span("retrieve_context") as span:
        span.set_attribute("query.length", len(query))
        embedding = await embed(query)         # its own auto-span
        results = await vector_search(embedding)
        span.set_attribute("results.count", len(results))
        span.set_attribute("results.top_score", results[0].score)
        return results
```

The rule: create a span for any operation you'd want to see separately when debugging.

---

## Span Attributes and Events (`span_attributes_and_events.py`)

Spans carry data that makes them useful:

**Attributes** — key-value metadata about the span. `model="gpt-4o"`, `tokens=847`, `cache_hit=false`. Filterable and searchable.

**Events** — timestamped moments within a span. "First token received." "Retry attempted." Useful for marking key points in a long operation.

**Status** — did the span succeed or error? Set explicitly so failed spans stand out.

For AI: attach the model, token counts, cost, temperature, and (redacted or hashed) prompt/response as attributes. This is what turns a generic trace into an LLM trace.

---

## Trace Context Propagation (`trace_context_propagation.py`)

The hard part of *distributed* tracing: keeping the trace connected across service boundaries.

When Service A calls Service B, the trace context (trace ID, parent span ID) must travel in the HTTP headers so B's spans attach to A's trace instead of starting a new one.

```
Service A span → injects traceparent header → HTTP request →
Service B extracts traceparent → continues the same trace
```

OTel handles this automatically for instrumented HTTP clients. The result: one trace spans your entire microservice architecture, not fragments per service.

---

## Sampling Strategies (`sampling_strategies.py`)

Tracing every request at scale is expensive. Sampling keeps cost bounded.

- **Head sampling:** Decide at the trace start (e.g., keep 10%). Cheap but might drop the trace you need.
- **Tail sampling:** Buffer the full trace, decide at the end. Keep 100% of slow/errored traces, sample the rest. Best signal, more infrastructure.
- **Rate-limited sampling:** Cap traces per second to control cost.

**AI-specific:** Always keep traces for errored requests, high-cost requests, and low-quality responses. Sample the fast, cheap, correct ones.

---

## Trace Analysis Patterns (`trace_analysis_patterns.py`)

What to look for when reading traces:

- **The long pole:** Which span dominates the total time? Optimize there.
- **Serial vs parallel:** Are independent operations running sequentially when they could be concurrent?
- **Unexpected calls:** Is there a database query in the LLM path that shouldn't be there?
- **N+1 patterns:** The same span type repeated many times (a loop making individual calls).
- **Gaps:** Time in the trace unaccounted for by any span (missing instrumentation).

---

## Debugging with Traces (`debugging_with_traces.py`)

The trace-first debugging workflow:
1. A metric or user report says "requests are slow / failing."
2. Find an example trace (filter by high latency or error status).
3. Read the span tree — the problem span is usually visually obvious.
4. Read that span's attributes and events for detail.
5. Jump to the logs for that span (via shared trace ID) for the exact error.

Trace → span → attributes → logs. This path resolves most production AI issues faster than any other method.

---

## Files in This Directory

| File | What It Covers |
|---|---|
| `traces_spans_context.py` | The three core concepts |
| `opentelemetry_fundamentals.py` | Why OTel, how the pipeline works |
| `otel_python_sdk.py` | Setting up tracing in Python |
| `automatic_instrumentation.py` | 80% value, near-zero effort |
| `manual_span_creation.py` | Tracing your business logic |
| `span_attributes_and_events.py` | Making spans useful |
| `trace_context_propagation.py` | Keeping traces connected across services |
| `sampling_strategies.py` | Bounding cost at scale |
| `trace_analysis_patterns.py` | What to look for |
| `debugging_with_traces.py` | The trace-first workflow |

---

*Previous: [← Metrics](../metrics/README.md) · Next: [LLM Observability →](../llm_observability/README.md)*

*Back to [main README](../../README.md)*
