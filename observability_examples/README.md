# Observability Examples — Run Them Yourself

Not diagrams. Actual `docker-compose up` and watch it work.

| Example | What It Shows | How to Run |
|---|---|---|
| `minimal_observable_llm_app/` | Smallest fully-instrumented LLM app | `docker-compose up` |
| `full_stack_observable_rag/` | RAG + Grafana + Prometheus + traces | `docker-compose up` |
| `observable_agent_system/` | Agent with full trajectory visibility | `python app/main.py` |
| `langsmith_end_to_end/` | LangSmith integration | set key, `python example.py` |
| `langfuse_self_hosted/` | Self-hosted Langfuse | `docker-compose up` |
| `phoenix_local_setup/` | Arize Phoenix local | `python example.py` |
| `grafana_prometheus_stack/` | Full Grafana + Prometheus | `docker-compose up` |
| `multi_tenant_observability/` | Per-tenant isolation | `python app/main.py` |

Start with `minimal_observable_llm_app`, then `full_stack_observable_rag`.
