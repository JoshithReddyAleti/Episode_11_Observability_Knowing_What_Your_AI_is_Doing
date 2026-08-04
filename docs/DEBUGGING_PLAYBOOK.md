# Production Debugging Playbook

## Universal Path
Metric (scope) → Trace (locate) → Log (detail)

## By Symptom

### Slow requests
Check latency percentiles → pull slow trace → find long-pole span → usually LLM provider, retrieval, or serial calls.

### Wrong answers (hallucination)
Pull trace → check retrieval (was right info retrieved?) → check context (did it make it into prompt?) → check generation (did model use it?) → check source (was data correct?).

### Cost spikes
Segment by user/tenant/feature/model → common causes: prompt change, verbosity, cache drop, loops, abuse → correlate with deploys.

### Quality regression
When did it start? → what changed then (prompt/model/retrieval/data)? → segment → compare good vs bad examples → check model version drift.

### System down
Check dependency health → recent deploys → provider status → rollback if deploy-related.

See src/production_debugging/README.md for full workflows.
