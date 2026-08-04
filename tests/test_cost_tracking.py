"""Tests for per-request cost computation."""
from src.utils.helpers import compute_cost

def test_cost_computation():
    # 850 in @ $0.15/1M, 320 out @ $0.60/1M
    cost = compute_cost(850, 320, 0.15, 0.60)
    expected = (850 * 0.15 + 320 * 0.60) / 1_000_000
    assert abs(cost - expected) < 1e-9

def test_zero_cost():
    assert compute_cost(0, 0, 0.15, 0.60) == 0
