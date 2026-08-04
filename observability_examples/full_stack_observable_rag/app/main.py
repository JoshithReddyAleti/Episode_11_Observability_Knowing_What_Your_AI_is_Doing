"""Full-stack observable RAG API (skeleton). See README for the full stack."""
from fastapi import FastAPI
app = FastAPI(title="Observable RAG")

@app.post("/query")
async def query(q: str):
    # retrieve (traced, chunk scores logged) → llm call (traced, cost logged)
    return {"answer": "...", "sources": []}
