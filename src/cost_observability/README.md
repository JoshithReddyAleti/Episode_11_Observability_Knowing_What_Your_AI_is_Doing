# 💰 Cost Observability — Never Be Surprised by a Bill Again

> *The most common way AI projects die isn't bad quality. It's a bill nobody saw coming.*

---

## Why Cost Is a First-Class Signal

In traditional software, compute cost is roughly fixed and predictable. In AI systems, cost is per-token, per-request, and wildly variable. A single prompt template change can double token usage. One malicious user can burn thousands. A retry loop can 10x a request's cost.

None of this shows up in standard observability. Cost observability makes spending visible in real time, attributable to its source, and predictable enough to act on before the invoice arrives.

---

## Per-Request Cost (`per_request_cost.py`)

The atomic unit. For every LLM call, compute and record cost:

```
cost = (input_tokens × input_price_per_token)
     + (output_tokens × output_price_per_token)
```

Attach cost to the request's trace and log. This is the foundation everything else aggregates from. Without per-request cost, you can only see the monthly total — useless for finding *what* is expensive.

---

## Per-User Cost (`per_user_cost.py`)

Aggregate cost by user. Answers: who is expensive, and is anyone abusing the system?

**Track:** cost per user per day/month, and the distribution. Usually a small fraction of users drive most cost (power users or abusers). Per-user cost lets you set fair limits (Episode 10's cost-based rate limiting), identify accounts to upsell, and catch abuse early.

---

## Per-Feature Cost (`per_feature_cost.py`)

Which features cost the most? Tag every LLM call with the feature that triggered it (chat, summarization, agent, search).

**Why:** A feature that costs more than it's worth is a product decision. Maybe the fancy agent feature costs $2/use and drives no retention — kill it. Per-feature cost turns spending into product intelligence.

---

## Per-Tenant Cost (`per_tenant_cost.py`)

For B2B/multi-tenant systems, cost per tenant (customer organization) is essential for:
- **Billing:** usage-based pricing requires accurate per-tenant cost
- **Margin analysis:** which customers are profitable?
- **Abuse detection:** which tenant is driving unexpected cost?

Tag every request with tenant_id and aggregate. Enterprise contracts often depend on this being accurate.

---

## Model Cost Comparison (`model_cost_comparison.py`)

Track cost broken down by model. Reveals optimization opportunities:
- Are you using an expensive model where a cheap one would do?
- What's the cost difference between your model tiers?
- Would a routing change (Episode 10) save money?

Seeing that 80% of cost comes from using gpt-4o for queries gpt-4o-mini could handle is a direct, actionable saving.

---

## Cost Anomaly Detection (`cost_anomaly_detection.py`)

Automatically detect abnormal spending *as it happens*, not at month-end.

**Detect:** hourly cost exceeding N× the recent average, a single user/tenant's cost spiking, or a sudden jump in cost-per-request (usually a prompt change). Alert immediately. Cost anomaly detection is what stands between a bug and a $50,000 surprise.

---

## Cost Forecasting (`cost_forecasting.py`)

Project future spending from current trends. Answers "at this growth rate, what's next month's bill?" and "when will we exceed budget?"

Simple linear projection from recent daily cost catches most surprises. More sophisticated forecasting accounts for growth trends and seasonality. Either way, forecasting turns cost from a lagging surprise into a leading indicator you can plan around.

---

## Cache Hit Savings (`cache_hit_savings.py`)

Quantify what your caching (Episode 10) actually saves. Track cache hit rate and the cost avoided by cache hits.

**Why:** This justifies the caching investment and reveals when it degrades. If semantic cache hit rate drops from 40% to 15% after a change, your costs just jumped 25% of your LLM spend — you want to know immediately.

---

## Cost Attribution (`cost_attribution.py`)

The unifying practice: every dollar traceable to its source dimensions — user, tenant, feature, model, endpoint. Attribution is what makes all the above possible.

Implement by tagging every LLM call with all relevant dimensions, then aggregating along any axis. Good attribution means you can answer any cost question ("how much did feature X cost tenant Y last week using model Z?") without guessing.

---

## Budget Alerts (`budget_alerts.py`)

Turn cost visibility into action. Set budgets at multiple levels and alert as they're approached:
- Per-user daily budget (with hard cutoff — Episode 10)
- Per-tenant monthly budget (contractual)
- Total system budget (with escalating alerts at 50%, 80%, 100%)

Alerts should fire *before* the budget is blown, with enough lead time to act. A budget alert at 80% on the 20th of the month lets you respond; an invoice on the 1st does not.

---

## Files in This Directory

| File | What It Covers |
|---|---|
| `per_request_cost.py` | The atomic cost unit |
| `per_user_cost.py` | Who is expensive |
| `per_feature_cost.py` | Which features cost the most |
| `per_tenant_cost.py` | Billing and margin (B2B) |
| `model_cost_comparison.py` | Optimization opportunities |
| `cost_anomaly_detection.py` | Catching spikes in real time |
| `cost_forecasting.py` | Projecting future spend |
| `cache_hit_savings.py` | Quantifying caching value |
| `cost_attribution.py` | Every dollar traceable |
| `budget_alerts.py` | Acting before the surprise |

---

*Previous: [← Agent Observability](../agent_observability/README.md) · Next: [Quality Monitoring →](../quality_monitoring/README.md)*

*Back to [main README](../../README.md)*
