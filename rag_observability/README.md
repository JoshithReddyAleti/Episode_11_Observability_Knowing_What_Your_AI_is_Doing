# 🔍 RAG Observability — Watching Retrieval Quality

> *Most RAG failures aren't LLM failures — they're retrieval failures. If you can't see what was retrieved, you can't fix why the answer was wrong.*

---

## The Central Insight

When a RAG system gives a bad answer, there are two possible causes:
1. **Retrieval failed** — the right information wasn't retrieved
2. **Generation failed** — the right information was retrieved but the LLM ignored or misused it

These need completely different fixes. Without RAG-specific observability, you can't tell which one happened — so you guess, and usually guess wrong.

---

## Retrieval Tracing (`retrieval_tracing.py`)

Trace every retrieval as a span with full detail:

**Capture:** the query (and any query transformation like HyDE), the embedding model used, the number of chunks retrieved, each chunk's content (or ID), each chunk's similarity score, and which chunks made it into the final context.

This turns "the answer was wrong" into "here are the 5 chunks that were retrieved, with scores — and the relevant one wasn't among them." Now you know it's a retrieval problem, and you can see whether it's an embedding, chunking, or indexing issue.

---

## Chunk Relevance Scoring (`chunk_relevance_scoring.py`)

Log the relevance score of each retrieved chunk and monitor the distribution over time.

**What healthy looks like:** top chunks score high (relevant), scores drop off after the useful ones.

**Warning signs:** all chunks scoring uniformly low (nothing relevant exists / embedding mismatch), or scores all clustered together (poor discrimination — embeddings can't tell relevant from irrelevant).

Track the top-1 score, top-k mean score, and score gap (difference between best and worst retrieved). A collapsing score gap is an early warning of retrieval degradation.

---

## Retrieval Latency Breakdown (`retrieval_latency_breakdown.py`)

Retrieval has multiple stages, each a latency source:
- **Query embedding** — encoding the query (model call)
- **Vector search** — the ANN lookup in the vector DB
- **Reranking** — the cross-encoder pass (if used)
- **Context assembly** — building the final prompt context

Break these out. A slow retrieval is usually one stage — often vector search as the index grows, or reranking if the candidate set is too large.

---

## Reranker Observability (`reranker_observability.py`)

If you use a reranker (Episode 5), observe how much it changes the ordering.

**Track:** the pre-rerank order vs post-rerank order, how many top results the reranker promoted/demoted, and reranker latency.

**Why:** If the reranker rarely changes the order, it's adding latency and cost for no benefit — remove it. If it dramatically reorders, it's earning its place. You only know by observing.

---

## Hit@K Monitoring (`hit_at_k_monitoring.py`)

The core retrieval quality metric, monitored in production. Hit@K = did the relevant chunk appear in the top K retrieved?

**Offline:** you have labeled data, compute Hit@K directly.

**Online:** you don't have labels, so approximate — use the chunk the LLM actually cited, or user feedback, or an LLM-as-judge relevance rating, as a proxy for "was the right thing retrieved."

A dropping Hit@K (even approximated) is the clearest signal that retrieval quality is regressing.

---

## Context Utilization (`context_utilization.py`)

You retrieved 5 chunks and stuffed them into the prompt. Did the model actually *use* them?

**Track:** which retrieved chunks the response actually drew from (via citation, or attribution analysis). If you consistently retrieve 5 chunks but the model only ever uses 1, you're paying for 4 chunks of context tokens for nothing — retrieve fewer. If the model uses information not in any chunk, that's a hallucination signal.

---

## Retrieval Failures (`retrieval_failures.py`)

Categorize the ways retrieval fails:
- **Empty retrieval** — nothing matched (query out of domain, or index issue)
- **Low-relevance retrieval** — results returned but all scored low
- **Wrong retrieval** — confident but wrong chunks (embedding mismatch)
- **Stale retrieval** — the index is out of date, missing recent data
- **Timeout** — vector DB too slow

Each failure mode has its own metric and its own fix. Tracking them separately turns a vague "retrieval is bad" into a specific, fixable problem.

---

## Embedding Drift Detection (`embedding_drift_detection.py`)

**The silent RAG killer.** Over time, the distribution of your queries (or documents) can drift away from what your embedding model handles well.

**Track:** the distribution of query embeddings over time. A statistical shift (measured with PSI or KL divergence — see drift_detection) signals that incoming queries look different than before. Also critical: if you *change* the embedding model, all existing vectors must be re-embedded — mismatched embedding spaces silently destroy retrieval. Observability catches the mismatch.

---

## RAG Debugging Workflow (`rag_debugging_workflow.py`)

The systematic process when a RAG answer is wrong:
1. **Look at the trace** — what was retrieved, with what scores?
2. **Was the right info retrieved?** No → retrieval problem (embedding/chunking/index). Yes → continue.
3. **Was the right info in the final context?** No → reranking/context-assembly dropped it. Yes → continue.
4. **Did the model use it?** No → generation problem (prompt/model). Yes → the info itself may be wrong (data quality).

Each branch points to a different fix. This workflow, backed by retrieval tracing, resolves RAG issues in minutes instead of hours.

---

## Files in This Directory

| File | What It Covers |
|---|---|
| `retrieval_tracing.py` | Full visibility into what was retrieved |
| `chunk_relevance_scoring.py` | Monitoring score distributions |
| `retrieval_latency_breakdown.py` | Where retrieval time goes |
| `reranker_observability.py` | Is the reranker earning its keep? |
| `hit_at_k_monitoring.py` | Retrieval quality in production |
| `context_utilization.py` | Did the model use what you retrieved? |
| `retrieval_failures.py` | Categorizing retrieval failure modes |
| `embedding_drift_detection.py` | The silent RAG killer |
| `rag_debugging_workflow.py` | Retrieval problem or generation problem? |

---

*Previous: [← LLM Observability](../llm_observability/README.md) · Next: [Agent Observability →](../agent_observability/README.md)*

*Back to [main README](../../README.md)*
