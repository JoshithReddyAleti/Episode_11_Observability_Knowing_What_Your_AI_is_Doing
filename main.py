"""Episode 11 — entry point stub tying observability together.
See README.md and observability_examples/ for runnable apps.
"""
from fastapi import FastAPI
app = FastAPI(title="Episode 11 — Observable AI")

@app.get("/health")
async def health():
    return {"status": "ok"}
