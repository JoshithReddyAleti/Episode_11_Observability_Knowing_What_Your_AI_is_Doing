"""helpers.py — Shared observability utilities."""
import uuid, time
def request_id(): return f"req_{uuid.uuid4().hex[:16]}"
def now_ms(): return int(time.time() * 1000)
def compute_cost(input_tokens, output_tokens, in_price, out_price):
    return (input_tokens * in_price + output_tokens * out_price) / 1_000_000
