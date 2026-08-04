# Minimal Observable LLM App

The smallest possible fully-instrumented LLM application: structured logs + Prometheus metrics + OpenTelemetry traces + cost tracking, in one file.

## Run
```bash
docker-compose up
# App: http://localhost:8000  Metrics: http://localhost:8000/metrics
```

## What to Look For
- Every request emits a structured JSON log with request_id
- `/metrics` exposes request count, latency histogram, token/cost counters
- Each request creates a trace with spans for each step
