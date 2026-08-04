"""Tests for metric helpers + request ID generation."""
from src.utils.helpers import request_id, now_ms

def test_request_id_unique():
    assert request_id() != request_id()

def test_request_id_prefix():
    assert request_id().startswith("req_")

def test_now_ms():
    assert now_ms() > 0
