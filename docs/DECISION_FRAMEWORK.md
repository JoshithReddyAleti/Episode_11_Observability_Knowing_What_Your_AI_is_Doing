# Decision Framework — Observability Choices

## Which pillar for this question?
- What happened in one request? → Logs
- What's the trend/rate? → Metrics
- Where in the flow? → Traces

## Which tool?
See docs/TOOL_COMPARISON_HONEST.md and src/observability_tools/README.md.

## What to alert on?
- User-visible symptom, actionable, urgent → alert (page/Slack by severity)
- Trend, gradual, investigate → dashboard/digest, not a page

## Which dashboard for whom?
- Leadership → executive
- On-call → engineering
- ML eng → LLM operations / agent operations
- Finance → cost
- Product → quality

## How much to sample?
- Always keep: errors, high-cost, low-quality, flagged
- Sample: fast, cheap, correct successes

## Ready for production observability?
Level 4 on the maturity model (src/foundations). Online eval + drift + cost + full tracing.
