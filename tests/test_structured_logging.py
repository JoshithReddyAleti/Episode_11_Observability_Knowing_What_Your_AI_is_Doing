"""Tests for structured logging + context propagation."""
from src.utils.logger import get_logger, set_log_context, _log_context

def test_context_propagates():
    set_log_context(request_id="req_1", user_id="u1")
    ctx = _log_context.get()
    assert ctx["request_id"] == "req_1"
    assert ctx["user_id"] == "u1"

def test_logger_creation():
    log = get_logger("test")
    assert log is not None
