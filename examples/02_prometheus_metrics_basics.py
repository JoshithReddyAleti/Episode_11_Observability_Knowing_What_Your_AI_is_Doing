"""02 — Prometheus metric types. Requires: pip install prometheus-client"""
try:
    from prometheus_client import Counter, Gauge, Histogram, generate_latest
    requests_total = Counter("demo_requests_total", "Total", ["status"])
    active = Gauge("demo_active", "In flight")
    latency = Histogram("demo_latency_seconds", "Latency")
    requests_total.labels(status="200").inc()
    active.inc(); latency.observe(0.42)
    print(generate_latest().decode()[:400])
except ImportError:
    print("pip install prometheus-client to run this example")
