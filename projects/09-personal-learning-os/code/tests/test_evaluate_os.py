"""[provided] Guiding tests for evaluate_os.py — M4 (evaluate_routing). OFFLINE, pure logic.

Uses a controllable FAKE route function so this milestone is independent of M1: we pin the metric
contract (overall accuracy, per-route accuracy, misroutes) regardless of how the real router behaves.
Fails with NotImplementedError until evaluate_routing is implemented.
"""
from evaluate_os import evaluate_routing
from router import Route


def fake_route_fn(mapping: dict):
    """Return a route_fn that maps a query to a fixed route name (default CHAT)."""
    def route(query: str) -> Route:
        return Route(mapping.get(query, "CHAT"), reason="fake", confidence=1.0)
    return route


def test_evaluate_all_correct():
    cases = [{"query": "a", "expected_route": "SAVE"},
             {"query": "b", "expected_route": "RECALL"}]
    rep = evaluate_routing(cases, fake_route_fn({"a": "SAVE", "b": "RECALL"}))
    assert rep["accuracy"] == 1.0
    assert rep["per_route"] == {"SAVE": 1.0, "RECALL": 1.0}
    assert rep["misroutes"] == []


def test_evaluate_per_route_exposes_a_silently_broken_route():
    cases = [{"query": "a", "expected_route": "SAVE"},
             {"query": "b", "expected_route": "SAVE"},
             {"query": "c", "expected_route": "TASK"}]
    # SAVE perfect, but every TASK is mis-routed to RECALL — a mean would hide it.
    rep = evaluate_routing(cases, fake_route_fn({"a": "SAVE", "b": "SAVE", "c": "RECALL"}))
    assert rep["per_route"]["SAVE"] == 1.0
    assert rep["per_route"]["TASK"] == 0.0
    assert abs(rep["accuracy"] - 2 / 3) < 1e-9
    assert rep["misroutes"] == [{"query": "c", "expected": "TASK", "got": "RECALL"}]


def test_evaluate_empty_cases():
    rep = evaluate_routing([], fake_route_fn({}))
    assert rep["accuracy"] == 0.0
    assert rep["per_route"] == {}
    assert rep["misroutes"] == []
