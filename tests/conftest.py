"""Shared pytest fixtures for Episode 11 observability tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pytest

@pytest.fixture
def sample_request():
    return {"request_id": "req_test123", "user_id": "u1", "tenant_id": "acme",
            "model": "gpt-4o-mini", "input_tokens": 850, "output_tokens": 320}
