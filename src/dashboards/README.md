# 📈 Dashboards — Making the Invisible Visible

> *A dashboard is a question answered at a glance. Design each one around the question its viewer actually asks.*

---

## The Golden Rule of Dashboards

Every dashboard has an **audience** and a **question**. An executive asking "is the product healthy and what does it cost?" needs a completely different dashboard than an engineer asking "why is p99 latency spiking right now?" A dashboard that tries to serve everyone serves no one.

Design per-audience. That's why this section has six distinct dashboards.

---

## Executive Dashboard (`executive_dashboard.md`)

**Audience:** leadership. **Question:** is the AI product healthy, growing, and cost-effective?

**Panels:** daily active users, request volume trend, total cost (with trend and forecast), overall quality score (thumbs-up rate), uptime/availability, cost per active user. High-level, business-oriented, no technical jargon. Green/yellow/red at a glance.

---

## Engineering Dashboard (`engineering_dashboard.md`)

**Audience:** engineers on-call. **Question:** is the system healthy, and if not, where's the problem?

**Panels:** the four golden signals (latency percentiles, traffic, error rate by category, saturation), request rate by endpoint, error breakdown, dependency health (DB, Redis, vector DB, LLM providers), recent deploys marked on the timeline. Built for fast debugging.

---

## LLM Operations Dashboard (`llm_operations_dashboard.md`)

**Audience:** AI/ML engineers. **Question:** are the model calls healthy?

**Panels:** tokens/sec (in/out), model usage distribution, TTFT and total latency percentiles, cache hit rate, fallback rate, refusal rate, error categories, cost per request. The LLM-specific counterpart to the engineering dashboard.

---

## Cost Dashboard (`cost_dashboard.md`)

**Audience:** engineering + finance. **Question:** where is the money going and is it under control?

**Panels:** cost over time (hourly/daily), cost by model, cost by feature, cost by tenant (top N), cost per user distribution, cache savings, budget consumption vs forecast, cost anomalies flagged. This dashboard prevents the surprise invoice.

---

## Quality Dashboard (`quality_dashboard.md`)

**Audience:** ML/product. **Question:** are answers actually good, and is quality holding?

**Panels:** online eval scores over time, thumbs-up/down rate (segmented by feature/model/prompt version), golden set score, refusal rate, regeneration rate, quality by model version (to catch regressions), drift indicators. The dashboard that catches silent degradation.

---

## Agent Operations Dashboard (`agent_operations_dashboard.md`)

**Audience:** engineers running agents. **Question:** are agents behaving efficiently and safely?

**Panels:** steps per task (with trend), tool selection distribution, loop/failure rates by type, cost per trajectory, task completion rate, tool error rate, approval-gate activity, kill-switch activations. Purpose-built for the unpredictability of agents.

---

## Grafana Setup (`grafana_setup.py`)

How to wire it up. Grafana is the standard open-source visualization layer:
- **Data sources:** Prometheus (metrics), Loki (logs), Tempo/Jaeger (traces)
- **Provisioning:** dashboards as code (JSON), version-controlled, deployed automatically
- **Variables:** template variables (environment, model, tenant) to make one dashboard reusable across dimensions
- **Linking:** click a metric spike → jump to the relevant traces (exemplars)

Example provisioned dashboards live in [`example_grafana_json/`](example_grafana_json/) and [`../../infrastructure/grafana/`](../../infrastructure/grafana/).

---

## Dashboard Design Principles (`dashboard_design_principles.md`)

1. **One question per dashboard.** Know what it answers before building it.
2. **Most important panel top-left.** Eyes go there first.
3. **Consistent time ranges.** All panels show the same window unless intentional.
4. **Show thresholds visually.** Draw the SLO line so "bad" is obvious.
5. **Red/yellow/green sparingly and meaningfully.** Color should mean action.
6. **Link to detail.** Every summary panel should let you drill into traces/logs.
7. **Annotate deploys and incidents.** Correlate changes with metric movements.
8. **Avoid vanity metrics.** If a panel never changes what anyone does, remove it.

---

## Files in This Directory

| File | What It Covers |
|---|---|
| `executive_dashboard.md` | Leadership: health, growth, cost |
| `engineering_dashboard.md` | On-call: golden signals, debugging |
| `llm_operations_dashboard.md` | ML eng: model call health |
| `cost_dashboard.md` | Finance + eng: where money goes |
| `quality_dashboard.md` | Product: is quality holding? |
| `agent_operations_dashboard.md` | Agent efficiency and safety |
| `grafana_setup.py` | Wiring up the visualization layer |
| `dashboard_design_principles.md` | The 8 rules |
| `example_grafana_json/` | Provisioned dashboard examples |

---

*Previous: [← Alerting](../alerting/README.md) · Next: [Production Debugging →](../production_debugging/README.md)*

*Back to [main README](../../README.md)*
