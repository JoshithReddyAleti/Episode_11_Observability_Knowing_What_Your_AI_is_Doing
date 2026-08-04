# 🕸️ Agent Observability — Watching Autonomous Decisions

> *An agent makes decisions you didn't script. Observability is the only way to know if those decisions were good — or how they went wrong.*

---

## Why Agents Are the Hardest to Observe

A chain does the same steps every time — easy to reason about. An agent (Episode 9) decides its own steps at runtime. That means:
- The execution path is different every time
- Failures are decisions, not exceptions ("it chose the wrong tool")
- Cost and latency are unpredictable (variable number of steps)
- Loops and dead-ends are possible

You can't debug what you can't see, and with agents there's a *lot* to see. Agent observability makes the invisible reasoning visible.

---

## Agent Trajectory Tracking (`agent_trajectory_tracking.py`)

The trajectory is the full sequence of steps an agent took: thought → action → observation → thought → action → ... → answer.

Capture the entire trajectory as a structured trace:
```
Step 1: Thought "I need the user's location"  → Action: get_location() → Obs: "SF"
Step 2: Thought "Now search restaurants"       → Action: search(...)    → Obs: [20 results]
Step 3: Thought "Filter by rating"             → Action: filter(...)    → Obs: [5 results]
Step 4: Thought "I have enough"                → Final Answer
```

This is the single most important agent observability artifact. When an agent misbehaves, the trajectory shows exactly where its reasoning went off track.

---

## Reasoning Step Visibility (`reasoning_step_visibility.py`)

Capture each reasoning step's content, not just that it happened. The model's "thought" at each step reveals *why* it chose an action.

When an agent does something wrong, the reasoning almost always explains it: "I'll use the weather tool" (for a non-weather query) tells you the tool descriptions are ambiguous or the reasoning is flawed. Without visible reasoning, you see the wrong action but not the wrong thinking behind it.

---

## Tool Call Tracing (`tool_call_tracing.py`)

Each tool the agent calls becomes a span with: tool name, arguments generated, argument validity, execution result, execution latency, and whether the result was used.

Nested and parallel tool calls form a tree. The trace shows the full tool-use pattern: which tools, in what order, with what results.

---

## Tool Selection Metrics (`tool_selection_metrics.py`)

Is the agent choosing the right tools? Track:
- **Tool selection distribution** — which tools get used, how often
- **Tool selection accuracy** — when you have ground truth, was the right tool chosen? (Episode 8)
- **Unused tools** — tools that are never selected (candidates for removal)
- **Tool retry rate** — how often a tool call has to be retried

A tool that's never selected is dead weight confusing the model. A tool selected wrongly is a description problem. Metrics surface both.

---

## Loop Detection (`loop_detection.py`)

**The classic agent failure.** The agent repeats the same action, or cycles between a few actions, never terminating.

**Detect:** the same action with the same arguments repeated N times, or a cycle of actions with no progress toward the goal. Track a "same action repeated" counter and alert when it exceeds a threshold. Loop detection is both an observability signal and a safety control (it should trigger termination — see Episode 9).

---

## Step Efficiency (`step_efficiency.py`)

How many steps did the agent take to complete the task, versus how many were necessary?

**Track:** steps per task, and the trend over time. A task that used to take 4 steps now taking 9 signals a regression — maybe a prompt change made the agent less decisive, or a tool got less reliable. Efficiency directly drives cost and latency.

---

## Multi-Agent Coordination Traces (`multi_agent_coordination_traces.py`)

For multi-agent systems (Episode 9), trace the coordination: which agent did what, what they passed to each other, where handoffs happened, and how the final result was assembled.

The trace shows the collaboration as a tree/graph. When a multi-agent system produces a bad result, the coordination trace reveals whether it was one agent's fault or a breakdown in how they communicated.

---

## Agent Cost Tracking (`agent_cost_tracking.py`)

Agents are the most expensive AI pattern — each step is an LLM call, and steps are variable. Track cost *per trajectory*, not just per LLM call.

**Track:** total cost per task, cost breakdown by step, and cost distribution across tasks. A few runaway trajectories (agents that looped or over-explored) can dominate your bill. Per-trajectory cost tracking finds them.

---

## Decision Audit Trails (`decision_audit_trails.py`)

For high-stakes agents, every consequential decision needs an immutable audit record: what the agent decided, why (the reasoning), what data it based the decision on, whether a human approved, and what the outcome was.

This serves debugging, compliance, and trust. When an agent takes an action with real-world consequences, the audit trail answers "why did it do that?" definitively. (Connects to Episode 8's governance and Episode 9's safety.)

---

## Failure Mode Analysis (`failure_mode_analysis.py`)

Categorize how agents fail so you can measure and reduce each:
- **Wrong tool selected** — description/reasoning issue
- **Hallucinated tool** — tried to call a nonexistent tool
- **Ignored observation** — didn't use a tool's result
- **Infinite loop** — never terminated
- **Premature termination** — gave up too early
- **Wrong plan** — the overall approach was flawed
- **Coordination failure** — multi-agent breakdown

Each has a distinct signature in the trajectory. Tracking their rates turns "the agent is unreliable" into "loop rate is 3%, wrong-tool rate is 7% — fix the tool descriptions first."

---

## Files in This Directory

| File | What It Covers |
|---|---|
| `agent_trajectory_tracking.py` | The full step sequence (most important) |
| `reasoning_step_visibility.py` | Why the agent chose each action |
| `tool_call_tracing.py` | Every tool call as a span |
| `tool_selection_metrics.py` | Is it choosing the right tools? |
| `loop_detection.py` | Catching the classic failure |
| `step_efficiency.py` | Steps per task and its trend |
| `multi_agent_coordination_traces.py` | Observing collaboration |
| `agent_cost_tracking.py` | Per-trajectory cost |
| `decision_audit_trails.py` | Immutable records for high-stakes actions |
| `failure_mode_analysis.py` | Categorizing and measuring failures |

---

*Previous: [← RAG Observability](../rag_observability/README.md) · Next: [Cost Observability →](../cost_observability/README.md)*

*Back to [main README](../../README.md)*
