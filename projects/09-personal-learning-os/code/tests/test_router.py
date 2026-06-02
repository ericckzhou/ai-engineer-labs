"""[provided] Guiding tests for router.py — M1 (route_query). OFFLINE, pure logic.

These fail with NotImplementedError until you implement route_query. They pin the routing CONTRACT:
classify by precedence (SAVE ▸ RECALL ▸ TASK), fall back to CHAT as the safe default, and respect the
confidence threshold. Queries are deliberately unambiguous — the hard, ambiguous cases are for your
FAILURE_ANALYSIS and the per-route evaluation, not for the contract.
"""
from router import route_query


# ---- SAVE ---------------------------------------------------------------------
def test_route_save():
    assert route_query("remember the demo is June 20").name == "SAVE"
    assert route_query("note: buy milk").name == "SAVE"
    assert route_query("don't forget to email Sam").name == "SAVE"


# ---- RECALL -------------------------------------------------------------------
def test_route_recall():
    assert route_query("what did I save about the demo?").name == "RECALL"
    assert route_query("find my notes on France").name == "RECALL"


# ---- TASK ---------------------------------------------------------------------
def test_route_task():
    assert route_query("summarize everything I saved this week").name == "TASK"
    assert route_query("compare my notes on A and B").name == "TASK"


# ---- CHAT (the safe default) --------------------------------------------------
def test_route_chat_is_safe_default():
    assert route_query("explain cosine similarity").name == "CHAT"
    assert route_query("hello there").name == "CHAT"


# ---- contract details ---------------------------------------------------------
def test_route_returns_reason_and_confidence():
    r = route_query("note: buy milk")
    assert r.name == "SAVE"
    assert r.reason  # a non-empty justification
    assert 0.0 <= r.confidence <= 1.0


def test_precedence_save_not_swallowed_as_chat():
    # A conversational save phrasing must route to SAVE, not be lost as small talk.
    assert route_query("remember that I like tea").name == "SAVE"


def test_threshold_forces_safe_default():
    # One marker -> confidence 0.5; a threshold above that demands stronger evidence -> CHAT.
    assert route_query("note: buy milk", threshold=0.9).name == "CHAT"
