# Observability Anti-Patterns

## 1. Logging everything unstructured
print() statements you can't query. Fix: structured JSON logs.

## 2. High-cardinality metric labels
user_id in Prometheus labels → explosion. Fix: labels are low-cardinality only.

## 3. Alerting on causes, not symptoms
"CPU > 80%" pages that don't matter. Fix: alert on user-visible symptoms.

## 4. No request ID correlation
Logs from concurrent requests interleave into noise. Fix: request IDs everywhere.

## 5. Ignoring the semantic layer
Perfect infra observability, zero prompt/response visibility. Fix: LLM-native tools.

## 6. No cost observability
Discovering cost problems on the invoice. Fix: per-request cost tracking.

## 7. Assuming 200 = success
An HTTP 200 with a hallucinated answer is a failure. Fix: quality monitoring.

## 8. Alert fatigue
So many alerts people ignore them all. Fix: every alert actionable, tiered severity.

## 9. Logging PII
Prompts/responses with PII in plaintext logs. Fix: redaction at logging layer.

## 10. Observability as afterthought
Adding it during the incident. Fix: instrument before you need it.
