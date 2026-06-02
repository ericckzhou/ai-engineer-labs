"""[provided] Guiding tests for learning_os.py — M3 (LearningOS.handle). OFFLINE.

Uses FAKE recording subsystems (from conftest) so `handle` is tested as pure routing + dispatch +
provenance logic — no store, no graph, no provider. Requires M1 (route_query) since handle routes
with it (milestone order: build the router first). Fails with NotImplementedError until M3 is done.
"""
from learning_os import LearningOS, Response


def test_handle_routes_save_with_provenance(fake_subsystems):
    os_ = LearningOS(fake_subsystems)
    r = os_.handle("remember the demo is June 20")
    assert isinstance(r, Response)
    assert r.route == "SAVE"
    assert r.provenance == [101]            # the SAVE worker's sources, threaded through
    assert fake_subsystems["SAVE"].calls    # the SAVE worker was invoked


def test_handle_routes_recall(fake_subsystems):
    os_ = LearningOS(fake_subsystems)
    r = os_.handle("what did I save about the demo?")
    assert r.route == "RECALL"
    assert r.provenance == [101, 102]


def test_handle_routes_chat_default_with_empty_provenance(fake_subsystems):
    os_ = LearningOS(fake_subsystems)
    r = os_.handle("explain cosine similarity")
    assert r.route == "CHAT"
    assert r.provenance == []


def test_handle_dispatches_to_exactly_one_subsystem(fake_subsystems):
    os_ = LearningOS(fake_subsystems)
    os_.handle("summarize everything I saved")
    called = [name for name, w in fake_subsystems.items() if w.calls]
    assert called == ["TASK"]               # one and only one worker ran


def test_handle_carries_route_reason(fake_subsystems):
    os_ = LearningOS(fake_subsystems)
    r = os_.handle("note: buy milk")
    assert r.route == "SAVE"
    assert r.reason                         # the router's justification is returned, not dropped
