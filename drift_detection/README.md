# 📉 Drift Detection — Catching the World Changing Underneath You

> *Your model was trained on yesterday's world. It serves today's. The gap between them grows silently — until it doesn't.*

---

## What Drift Is

Drift is when the statistical properties of your system's inputs or outputs change over time, degrading performance without any code change. The model didn't break — the world moved. Drift is uniquely dangerous because it's gradual and invisible to per-request observability. Only by comparing distributions *over time* can you see it.

---

## Input Drift (`input_drift.py`)

The distribution of incoming queries changes. Users start asking about new topics, in new styles, in new languages, at new lengths.

**Detect:** track features of incoming requests (length, topic distribution, language, embedding distribution) and compare current windows to a baseline. When users start asking things your system wasn't built for, input drift catches it before quality visibly craters.

---

## Output Drift (`output_drift.py`)

The distribution of your system's responses changes — even for similar inputs. Responses get longer, shorter, more/less confident, more/less likely to refuse.

**Detect:** track output features (length, sentiment, refusal rate, structure) over time. Output drift with stable input drift usually means something changed on the model side — a version update, a prompt edit, a parameter change.

---

## Embedding Drift (`embedding_drift.py`)

**Critical for RAG.** The distribution of query or document embeddings shifts. This degrades retrieval silently because the embedding space your vectors live in no longer matches incoming queries well.

**Detect:** monitor the distribution of query embeddings (via dimensionality-reduced statistics or distance-to-centroid metrics) against a baseline. Also catches the catastrophic case: an embedding model change that requires re-indexing. (See also [`src/rag_observability/`](../rag_observability/README.md).)

---

## Prompt Drift (`prompt_drift.py`)

Your *own* prompts change over time — often accidentally. A template edit, a new few-shot example, a reordered instruction. Prompt drift tracks the versions and correlates them with quality/cost/behavior changes.

**Track:** prompt template versions as a dimension on all metrics. When quality shifts, "which prompt version was live?" is answerable instantly. Prompt drift is the most controllable form of drift — you just have to observe it.

---

## Model Drift (`model_drift.py`)

The model itself changes behavior — usually a provider updating a model behind a stable name, or you migrating versions. Model drift tracks model version as a dimension and watches for behavior changes across versions.

**Track:** exact model version on every request; compare quality/cost/latency/length distributions across versions. This is how you catch "gpt-4o got worse at our task last Tuesday" — a real, common, otherwise-invisible event.

---

## PSI and KL Divergence (`psi_kl_divergence.py`)

The math of drift detection. Two standard measures of "how different are these two distributions?":

**Population Stability Index (PSI):** compares a current distribution to a baseline across bins. Rule of thumb: PSI < 0.1 = no significant drift; 0.1–0.25 = moderate drift, investigate; > 0.25 = significant drift, act. Simple, interpretable, widely used.

**KL Divergence:** measures how much one distribution differs from a reference. More sensitive, less symmetric, common in ML monitoring.

Both turn "the data feels different" into a number you can threshold and alert on.

---

## Statistical Tests (`statistical_tests.py`)

Beyond PSI/KL, tests for detecting distribution change:
- **Kolmogorov-Smirnov (KS)** — for continuous distributions (latency, length, scores)
- **Chi-square** — for categorical distributions (topic, language, model)
- **Wasserstein distance** — "earth mover's distance," robust for embeddings

Choosing the right test depends on the data type. The README covers which test for which signal.

---

## Drift Alerting (`drift_alerting.py`)

Turn drift measurements into action. Set thresholds (PSI > 0.25, KS p-value < 0.05) and alert when crossed.

**Key practice:** drift alerts are *investigate* signals, not *page-someone* signals — drift is gradual, not an outage. Route them to a dashboard/daily digest, not to PagerDuty at 3 AM. When a drift alert fires, the response is analysis (what changed, does it matter?), possibly leading to re-evaluation, re-indexing, or retraining.

---

## Files in This Directory

| File | What It Covers |
|---|---|
| `input_drift.py` | Incoming query distribution shifts |
| `output_drift.py` | Response distribution shifts |
| `embedding_drift.py` | The RAG-critical drift |
| `prompt_drift.py` | Your own prompts changing |
| `model_drift.py` | Provider model behavior changes |
| `psi_kl_divergence.py` | The core drift math |
| `statistical_tests.py` | KS, chi-square, Wasserstein |
| `drift_alerting.py` | Investigate signals, not pages |

---

*Previous: [← Quality Monitoring](../quality_monitoring/README.md) · Next: [Alerting →](../alerting/README.md)*

*Back to [main README](../../README.md)*
