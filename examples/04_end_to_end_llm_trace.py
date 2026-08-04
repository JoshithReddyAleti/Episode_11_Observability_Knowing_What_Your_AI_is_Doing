"""04 — End-to-end LLM request with full instrumentation (logs+metrics+trace+cost)."""
import sys, os, time, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.utils.logger import get_logger, set_log_context
from src.utils.helpers import request_id, compute_cost

log = get_logger("example04")
set_log_context(request_id=request_id(), user_id="demo")
t0 = time.time()
in_tok, out_tok = 850, 320
time.sleep(0.05)
cost = compute_cost(in_tok, out_tok, 0.15, 0.60)  # gpt-4o-mini pricing per 1M
log.info("llm_request_complete")
print(f"tokens_in={in_tok} tokens_out={out_tok} cost=${cost:.6f} latency={time.time()-t0:.3f}s")
