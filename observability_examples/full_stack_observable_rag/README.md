# Full-Stack Observable RAG

A complete RAG API instrumented end to end, with the full observability stack running alongside: Prometheus (metrics), Grafana (dashboards), and trace export.

## Run
```bash
docker-compose up
# RAG API: http://localhost:8000
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

## What to Look For
- Retrieval traced with chunk scores (RAG observability)
- LLM call traced with tokens + cost
- Pre-built Grafana dashboard for RAG operations
- Prometheus scraping the app's /metrics
