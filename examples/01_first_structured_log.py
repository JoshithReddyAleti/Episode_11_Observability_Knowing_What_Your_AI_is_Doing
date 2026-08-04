"""01 — Your first structured log. Run: python examples/01_first_structured_log.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.utils.logger import get_logger, set_log_context
from src.utils.helpers import request_id

log = get_logger("example01")
set_log_context(request_id=request_id(), user_id="demo_user", environment="dev")
log.info("chat_request_started")
log.info("llm_call_completed")  # both logs auto-include request_id + user_id
print("\n^ Two JSON logs above, both correlated by the same request_id.")
