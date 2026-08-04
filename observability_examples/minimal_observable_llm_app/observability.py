"""Observability setup — the reusable core."""
import logging, sys, json
from prometheus_client import Counter, Histogram, make_asgi_app

REQUESTS = Counter("chat_requests_total", "Total chat requests", ["status"])
LATENCY = Histogram("chat_latency_seconds", "Chat latency")
TOKENS = Counter("chat_tokens_total", "Tokens used", ["kind"])
COST = Counter("chat_cost_dollars_total", "Cost in dollars")

log = logging.getLogger("app")

def setup_observability(app):
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(logging.Formatter('{"level":"%(levelname)s","event":"%(message)s"}'))
    log.addHandler(h); log.setLevel(logging.INFO)
    app.mount("/metrics", make_asgi_app())
