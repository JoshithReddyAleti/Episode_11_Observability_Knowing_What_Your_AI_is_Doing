# Core Concepts — Episode 11

1. **Observability = understanding internal state from outside.** Without shipping new code to investigate.

2. **Monitoring ≠ observability.** Monitoring answers known questions; observability answers unknown ones.

3. **Three pillars: logs, metrics, traces.** Each answers a different question; you need all three.

4. **AI needs a fourth dimension.** The semantic layer — prompts, responses, retrieval, reasoning.

5. **AI fails silently.** A 200 status with a wrong answer. Quality must be observed, not assumed.

6. **Request IDs correlate everything.** The single most important field.

7. **Low-cardinality metric labels.** Never put user IDs in metric labels.

8. **Trace-first debugging.** For AI, start from the trace, not the log.

9. **Cost is a first-class signal.** Per-request cost tracking prevents surprise bills.

10. **Retrieval failures ≠ generation failures.** RAG observability distinguishes them.

11. **Agent trajectories are the key artifact.** The full reasoning sequence.

12. **Drift is silent and gradual.** Only visible by comparing distributions over time.

13. **Alerts must be actionable.** Non-actionable alerts cause fatigue, which causes missed incidents.

14. **Symptom-based alerting.** Alert on user pain, not internal causes.

15. **One tool doesn't do it all.** LLM-native + general, via OpenTelemetry.

16. **Observability is evidence.** For debugging, compliance, and forensics.

17. **Instrument before you need it.** During an incident, you can only use what exists.

18. **Every incident improves observability.** Find what was missing, add it.

19. **Observability as code.** Version-controlled dashboards and alerts.

20. **The invisible is where AI fails.** Observability makes it visible.
