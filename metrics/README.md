# 📊 Metrics — The Numbers That Reveal Trends

> *Logs tell you about one request. Metrics tell you about a million. Both matter.*

---

## What Metrics Are

A metric is a numeric measurement tracked over time. Unlike logs (one event each), metrics aggregate: "requests per second," "p99 latency," "average cost per request." They're cheap to store forever, fast to query, and the foundation of dashboards and alerts.

The trade-off: metrics lose individual detail. You know the average cost tripled; you don't know *which* request caused it (that's what traces and logs are for).

---

## Prometheus Setup (`prometheus_setup.py`)

Prometheus is the de facto open-source metrics standard. Your app exposes a `/metrics` endpoint; Prometheus scrapes it every N seconds and stores time-series data.

```python
from prometheus_client import Counter, Histogram, Gauge, make_asgi_app

# Expose metrics endpoint
app.mount("/metrics", make_asgi_app())
```

Prometheus stores everything as time series. Grafana queries Prometheus to visualize. This is the backbone of open-source observability.

---

## Counters, Gauges, Histograms (`counters_gauges_histograms.py`)

The three metric types. Choosing correctly matters.

### Counter — only goes up
For things you count cumulatively: total requests, total errors, total tokens used.
```python
requests_total = Counter("requests_total", "Total requests", ["endpoint", "status"])
requests_total.labels(endpoint="/chat", status="200").inc()
```
You query the *rate* of a counter: `rate(requests_total[5m])` = requests per second.

### Gauge — goes up and down
For current state: active connections, queue depth, current memory usage.
```python
active_requests = Gauge("active_requests", "Requests in flight")
active_requests.inc()  # request starts
active_requests.dec()  # request ends
```

### Histogram — distributions
For measuring spread: latency, request size, cost. Buckets values so you can compute percentiles.
```python
request_duration = Histogram("request_duration_seconds", "Duration", ["endpoint"])
request_duration.labels(endpoint="/chat").observe(0.85)
```
Histograms let you compute p50, p95, p99 — critical because *averages lie*. An average latency of 500ms can hide a p99 of 8 seconds.

---

## The Four Golden Signals (`the_four_golden_signals.py`)

Google's SRE book defines the four signals that matter for any user-facing system:

1. **Latency** — how long requests take. Track p50, p95, p99 separately. Separate successful from failed request latency (a fast failure shouldn't look good).
2. **Traffic** — how much demand. Requests per second, tokens per second.
3. **Errors** — rate of failed requests. Both hard errors (500s) and soft errors (wrong answers — AI-specific).
4. **Saturation** — how full your system is. CPU, memory, queue depth, connection pool usage.

If you track only four things, track these.

---

## The RED Method (`the_red_method.py`)

For request-driven services (like AI APIs), track for every endpoint:
- **R**ate — requests per second
- **E**rrors — failed requests per second
- **D**uration — latency distribution

RED is the golden signals reframed for services. Simple, complete, actionable.

---

## The USE Method (`the_use_method.py`)

For resources (databases, queues, GPUs), track:
- **U**tilization — % of time the resource is busy
- **S**aturation — how much work is queued/waiting
- **E**rrors — error count for the resource

RED for services, USE for resources. Together they cover everything.

---

## Business Metrics (`business_metrics.py`)

Technical metrics tell you the system is healthy. Business metrics tell you it's *valuable*.

- Daily/monthly active users
- Queries per user
- Feature adoption rate
- Conversion / task completion rate
- User retention

These connect engineering to impact. When you tune latency, business metrics tell you if it mattered.

---

## LLM-Specific Metrics (`llm_specific_metrics.py`)

The metrics standard observability never told you to track:

- **Tokens per request** (input and output separately)
- **Cost per request** (derived from tokens × model pricing)
- **Time to first token** (for streaming — perceived latency)
- **Tokens per second** (generation throughput)
- **Model usage distribution** (which models, how often)
- **Cache hit rate** (semantic + exact cache effectiveness)
- **Fallback rate** (how often the primary model fails)
- **Refusal rate** (how often the model declines to answer)
- **Context window utilization** (how full the context gets)
- **Retry rate** (transient failures)

Each of these is a leading indicator of a problem before users notice.

---

## Custom Metrics Design (`custom_metrics_design.py`)

Designing a good metric:
1. **Name it clearly:** `llm_tokens_total` not `tokens`. Include units in the name (`_seconds`, `_bytes`, `_total`).
2. **Label thoughtfully:** Labels let you slice (by model, endpoint, tenant). But every label combination is a separate time series — see cardinality below.
3. **Pick the right type:** Count → Counter. Current value → Gauge. Distribution → Histogram.
4. **Make it actionable:** If a metric moving wouldn't change what you do, don't track it.

---

## Metric Cardinality (`metric_cardinality.py`)

**The trap that blows up your metrics bill.** Cardinality = number of unique label combinations.

```python
# ❌ CATASTROPHE — user_id has millions of values
requests_total.labels(user_id="abc123", endpoint="/chat")
# Millions of users × endpoints = millions of time series = Prometheus dies

# ✅ SAFE — bounded label values
requests_total.labels(user_tier="free", endpoint="/chat")
# 3 tiers × 10 endpoints = 30 time series
```

**Rule:** Never put unbounded values (user IDs, request IDs, prompts) in metric labels. Those belong in logs and traces. Metric labels must be low-cardinality (tiers, models, status codes, endpoints).

---

## Metrics Aggregation (`metrics_aggregation.py`)

How raw measurements become dashboard numbers:
- **rate()** — per-second rate of a counter over a window
- **histogram_quantile()** — compute p99 from histogram buckets
- **sum() by (label)** — aggregate across instances, grouped by a label
- **avg / max / min** — over time windows

Understanding aggregation is what lets you turn "17 million data points" into "p99 latency by model, per minute."

---

## Files in This Directory

| File | What It Covers |
|---|---|
| `prometheus_setup.py` | Exposing and scraping metrics |
| `counters_gauges_histograms.py` | The three types, chosen correctly |
| `the_four_golden_signals.py` | Latency, traffic, errors, saturation |
| `the_red_method.py` | Rate, errors, duration for services |
| `the_use_method.py` | Utilization, saturation, errors for resources |
| `business_metrics.py` | Connecting tech to value |
| `llm_specific_metrics.py` | Tokens, cost, TTFT, cache hit, refusal rate |
| `custom_metrics_design.py` | Designing metrics that matter |
| `metric_cardinality.py` | The label explosion trap |
| `metrics_aggregation.py` | Raw data → dashboard numbers |

---

*Previous: [← Structured Logging](../structured_logging/README.md) · Next: [Distributed Tracing →](../distributed_tracing/README.md)*

*Back to [main README](../../README.md)*
