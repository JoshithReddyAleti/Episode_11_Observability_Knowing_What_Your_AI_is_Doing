# 🔔 Alerting — Turning Signals Into Action

> *An alert that doesn't lead to action is noise. Noise trains people to ignore alerts. Ignored alerts are how outages become disasters.*

---

## The First Principle of Alerting

Every alert must be **actionable** and **urgent**. If an alert fires and the on-call engineer's correct response is "eh, I'll look at it later" — it should not have been an alert. It should have been a dashboard panel or a daily digest.

Bad alerting is worse than no alerting, because it causes alert fatigue (see below), which makes people miss the alerts that matter.

---

## Symptom-Based Alerts (`symptom_based_alerts.py`)

Alert on what users experience, not on internal causes.

**Symptom-based (good):** "Error rate > 5% for 5 minutes." "p99 latency > 5s." "No successful requests in 5 minutes." These mean users are hurting *right now*.

**Cause-based (noisy):** "CPU > 80%." "Memory > 90%." "A pod restarted." These *might* cause problems — or might be totally fine. Alerting on them generates false pages.

Alert on symptoms; use causes for debugging once a symptom fires.

---

## SLO/SLI Alerts (`slo_sli_alerts.py`)

Alert based on your service level objectives and error budgets (Episode 10).

**SLI** — what you measure (e.g., % of requests succeeding). **SLO** — your target (e.g., 99.9%). **Error budget** — the allowed failure (0.1%).

**Burn-rate alerting:** alert when you're consuming error budget too fast. A slow burn (you'll exhaust the monthly budget in 3 weeks) is a low-urgency alert. A fast burn (you'll exhaust it in an hour) is a page. This is far better than raw threshold alerting — it accounts for both severity and duration.

---

## AI-Specific Alerts (`ai_specific_alerts.py`)

The alerts standard observability never told you to set:
- **Cost spike** — hourly cost exceeds N× baseline
- **Quality drop** — online eval score or thumbs-up rate falls below threshold
- **Refusal spike** — refusal rate jumps (model change or content issue)
- **Fallback spike** — primary model failing, falling back too often
- **Hallucination rate** — grounding/faithfulness score drops
- **Retrieval degradation** — Hit@K or chunk relevance drops
- **Agent loop rate** — agents looping/failing to terminate
- **Drift threshold crossed** — PSI/KL exceeds limit

Each of these catches an AI failure mode invisible to traditional alerts.

---

## Anomaly Detection (`anomaly_detection.py`)

For signals where a fixed threshold doesn't work (traffic and cost vary by time of day/week), detect statistical anomalies instead.

**Approaches:** rolling z-score (how many standard deviations from the recent mean), seasonal decomposition (account for daily/weekly patterns), or simple "N× the same hour last week." Anomaly detection catches "this is weird for right now" without you hand-tuning thresholds for every hour.

---

## Multi-Signal Alerts (`multi_signal_alerts.py`)

Reduce false positives by requiring multiple conditions. A single metric blip is often noise; correlated signals are real.

**Example:** Don't page on latency alone. Page when latency is high AND error rate is elevated AND it's sustained for 5 minutes. Multi-signal alerts fire less often but almost always mean something real — dramatically improving the signal-to-noise ratio.

---

## Alert Fatigue Prevention (`alert_fatigue_prevention.py`)

**The silent killer of on-call teams.** Too many alerts → people stop reading them → they miss the real one.

**Prevent it:**
- Every alert must be actionable (delete the rest)
- Tune thresholds to real incident levels, not theoretical ones
- Group related alerts (one incident shouldn't fire 20 pages)
- Use severity tiers (page vs Slack vs digest)
- Regularly review: which alerts fired and were ignored? Delete or fix them.
- Track alert precision: what fraction of alerts led to action?

An alert that's a false positive more than ~20% of the time needs fixing or deletion.

---

## Alert Routing (`alert_routing.py`)

The right alert to the right person via the right channel:
- **P1 (users down):** page on-call immediately (PagerDuty), 24/7
- **P2 (degraded):** Slack the team, business hours
- **P3 (trends/drift):** dashboard or daily digest, no interrupt

Route by ownership too — cost alerts to the team that owns cost, quality alerts to the ML team. Routing prevents both the "everyone gets paged for everything" and the "nobody owns this alert" failure modes.

---

## PagerDuty Integration (`pagerduty_integration.py`)

For urgent, page-worthy alerts. PagerDuty (or Opsgenie) handles: on-call schedules, escalation (if primary doesn't ack in N minutes, page secondary), and acknowledgment tracking.

Reserve paging for genuine "wake someone up" situations. Every page should be a real incident. Track page precision as a health metric for your alerting.

---

## Slack Alerting (`slack_alerting.py`)

For non-urgent-but-notable signals. Slack alerts inform the team without interrupting sleep: degraded (but functional) performance, cost warnings, drift notices, deploy notifications.

**Good Slack alerts** include context (what fired, current value vs threshold, a link to the dashboard/trace, and a suggested first step) so the reader can act without hunting for information.

---

## Files in This Directory

| File | What It Covers |
|---|---|
| `symptom_based_alerts.py` | Alert on user pain, not internal causes |
| `slo_sli_alerts.py` | Error-budget burn-rate alerting |
| `ai_specific_alerts.py` | Cost, quality, drift, agent alerts |
| `anomaly_detection.py` | When fixed thresholds don't fit |
| `multi_signal_alerts.py` | Requiring correlation to reduce noise |
| `alert_fatigue_prevention.py` | Keeping alerts trustworthy |
| `alert_routing.py` | Right alert, right person, right channel |
| `pagerduty_integration.py` | For genuine pages |
| `slack_alerting.py` | For notable-but-not-urgent |

---

*Previous: [← Drift Detection](../drift_detection/README.md) · Next: [Dashboards →](../dashboards/README.md)*

*Back to [main README](../../README.md)*
