# Observability Taxonomy — What to Observe

## By Pillar
- **Logs** — discrete events (what happened at a moment)
- **Metrics** — aggregated numbers (trends over time)
- **Traces** — request flow (where time/errors occur)

## By AI Layer
- **Infrastructure** — CPU, memory, network, latency, errors
- **LLM** — prompts, responses, tokens, model versions, parameters
- **RAG** — retrieval quality, chunk relevance, embedding drift
- **Agent** — trajectories, tool selection, loops, decisions
- **Cost** — per request/user/tenant/feature/model
- **Quality** — online eval, feedback, regressions
- **Drift** — input/output/embedding/prompt/model

## By Purpose
- **Debugging** — traces + correlated logs
- **Alerting** — symptom-based metrics
- **Capacity** — saturation metrics
- **Cost control** — cost attribution
- **Compliance** — audit logs
- **Security** — access logs, injection detection

## By Audience
- **Executives** — health, growth, cost
- **Engineers** — golden signals, debugging
- **ML engineers** — LLM/RAG/agent operations
- **Finance** — cost breakdown
- **Security** — audit, access, threats
