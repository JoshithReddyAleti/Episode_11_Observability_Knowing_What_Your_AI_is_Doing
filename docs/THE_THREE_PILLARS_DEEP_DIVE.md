# The Three Pillars — When Each Wins

## Logs
**Strength:** maximum detail about individual events.
**Use when:** you need to know exactly what happened in one request.
**Weakness:** expensive at volume; hard to see trends.

## Metrics
**Strength:** cheap, fast, perfect for trends and alerts.
**Use when:** you need to know rates, percentiles, or aggregate behavior.
**Weakness:** no individual detail; cardinality limits.

## Traces
**Strength:** shows the flow of one request across all components.
**Use when:** you need to know WHERE in a multi-step flow something happened.
**Weakness:** sampling needed at scale; setup complexity.

## The Handoff
Metric (something's wrong) → Trace (where) → Log (exactly what).
Each pillar answers a different question. You need all three.

## For AI: Add a Fourth Dimension
The semantic layer — prompts, responses, retrieval, reasoning — cuts across all three pillars and is captured by LLM-native tools (Langfuse, LangSmith, Phoenix).
