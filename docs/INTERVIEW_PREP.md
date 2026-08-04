# Interview Prep — Episode 11

## "What's the difference between monitoring and observability?"
> "Monitoring answers questions you already know to ask — is it up, is CPU high, is the error rate over 5%. You build those dashboards in advance. Observability lets you answer questions you didn't know to ask — why are German users slow only on Tuesdays, why did this specific user get a hallucination. Monitoring tells you THAT something is wrong; observability tells you WHY. For AI especially you need the second, because AI failure modes are impossible to fully anticipate."

## "How is observing an AI system different from a normal web app?"
> "Normal apps fail loudly — 500 errors, stack traces. AI systems fail silently — a confident, well-formatted, completely wrong answer with a 200 status. So beyond the standard three pillars, I instrument a semantic layer: every prompt, response, and token count; retrieval quality and chunk relevance for RAG; agent trajectories and tool selection for agents; per-request cost; and quality via online evaluation. Plus drift detection, because AI degrades as the world moves away from its training distribution — something no per-request observability catches."

## "A user says answers got worse but nothing was deployed. How do you debug it?"
> "First, confirm with the quality dashboard — when did it start, is it all traffic or one segment? Since nothing was deployed, my prime suspect is model version drift — the provider may have updated the model behind a stable name, so I check the model version dimension on my metrics. I also check embedding drift (did the input distribution shift?) and data freshness (did the index go stale?). I compare good-period vs bad-period examples using my golden set, which is stable enough to compare over time. The whole investigation is possible because I track model version, drift, and quality as first-class signals."

## "How do you debug a RAG system that hallucinates?"
> "I pull the trace and walk four checkpoints. One: was the correct info retrieved? If not, it's a retrieval problem — embedding, chunking, or index. Two: did the correct info make it into the final prompt? If not, reranking or context assembly dropped it. Three: was the info in context but the model contradicted it? That's a generation problem. Four: was the retrieved info itself wrong? That's data quality. Each branch has a different fix, and I can only distinguish them because retrieval tracing shows me exactly what was retrieved with what scores."

## "How do you prevent surprise LLM bills?"
> "Cost observability. Every request gets per-request cost computed from tokens and model pricing, attributed to user, tenant, feature, and model. That rolls up into real-time dashboards and anomaly detection — if hourly cost exceeds a multiple of baseline, or one tenant spikes, it alerts immediately. Plus forecasting to project the month, and budget alerts at 50/80/100%. The whole point is turning cost from a lagging invoice surprise into a leading signal I can act on."

## "What's an observability anti-pattern you've seen?"
> "High-cardinality metric labels. Someone puts user_id or request_id as a Prometheus label, and every unique value becomes a separate time series — millions of them — and Prometheus falls over. Unbounded values belong in logs and traces, not metric labels. Metric labels must be low-cardinality — tier, model, status code, endpoint. It's a classic mistake that turns your metrics system into an outage."

## Resume Bullet
> Built end-to-end observability for production AI — structured logging with PII redaction, Prometheus metrics, OpenTelemetry tracing, plus LLM/RAG/agent-specific instrumentation (prompt/token/cost tracking, retrieval quality, agent trajectories), online quality evaluation, and PSI-based drift detection across LangSmith, Langfuse, Phoenix, and Grafana.
