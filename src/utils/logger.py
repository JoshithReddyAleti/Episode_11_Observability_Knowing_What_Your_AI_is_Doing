"""logger.py — Structured JSON logger with context support."""
import logging, sys, os, json
from contextvars import ContextVar
_log_context: ContextVar[dict] = ContextVar("_log_context", default={})
def set_log_context(**kwargs):
    ctx = dict(_log_context.get()); ctx.update(kwargs); _log_context.set(ctx)
class JSONFormatter(logging.Formatter):
    def format(self, record):
        base = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "event": record.getMessage(),
            "logger": record.name,
        }
        base.update(_log_context.get())
        base.update(getattr(record, "extra_fields", {}) or {})
        return json.dumps(base)
def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "INFO"), logging.INFO))
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(JSONFormatter())
        logger.addHandler(h); logger.propagate = False
    return logger
