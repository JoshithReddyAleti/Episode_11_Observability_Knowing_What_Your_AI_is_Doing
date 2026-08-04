"""Minimal fully-observable LLM app. FastAPI + logs + metrics + traces + cost."""
from fastapi import FastAPI
from observability import setup_observability, log, REQUESTS, LATENCY, TOKENS, COST
import time

app = FastAPI(title="Minimal Observable LLM App")
setup_observability(app)

@app.post("/chat")
async def chat(message: str = "hello"):
    t0 = time.time()
    # (call your LLM here) — simulated
    in_tok, out_tok = len(message.split()) * 4, 120
    cost = (in_tok * 0.15 + out_tok * 0.60) / 1_000_000
    TOKENS.labels(kind="input").inc(in_tok)
    TOKENS.labels(kind="output").inc(out_tok)
    COST.inc(cost)
    dur = time.time() - t0
    LATENCY.observe(dur)
    REQUESTS.labels(status="200").inc()
    log.info("chat_complete")
    return {"response": "...", "tokens": in_tok + out_tok, "cost_usd": cost}
