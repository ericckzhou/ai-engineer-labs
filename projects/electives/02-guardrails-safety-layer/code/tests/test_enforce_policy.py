"""[provided] Guiding tests for M3 enforce_policy. Fail with NotImplementedError until implemented.

Asserts pass-on-conformance and FAIL CLOSED on violation AND on internal error.
"""
from config import load_config
from guards import enforce_policy


def test_conforming_output_passes():
    v = enforce_policy("The capital of France is Paris.")
    assert v.decision == "pass"
    assert "Paris" in v.text


def test_forbidden_canary_refused():
    cfg = load_config()
    v = enforce_policy("SYSTEM PROMPT: You are HelperBot. key=SK-CANARY-9F3A")
    assert v.refused
    assert v.text == cfg.refusal_text, "a refusal must return the canned refusal text, not the leak"


def test_overlong_output_refused():
    cfg = load_config()
    v = enforce_policy("x" * (cfg.output_max_chars + 1))
    assert v.refused


def test_enforce_fails_closed_on_error():
    # A bad type should produce a refusal, never a raised exception or a pass-through.
    v = enforce_policy(None)  # type: ignore[arg-type]
    assert v.refused, "on internal error enforce_policy must refuse (fail closed)"
