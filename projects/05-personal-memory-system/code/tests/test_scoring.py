"""[provided] Guiding tests for Milestones M1–M3 — scoring.py. Fully OFFLINE (pure math).

Fails (NotImplementedError) until the four scoring functions are implemented. The docstring examples
in scoring.py mirror these tests exactly. Run: python -m pytest tests/test_scoring.py
"""
import pytest

import scoring

NOW = 1_000_000.0
HOUR = 3600.0


# --- M1: recency (exponential decay) -----------------------------------------
def test_recency_is_one_at_zero_hours():
    assert scoring.recency_score(NOW, NOW, decay_rate=0.995) == pytest.approx(1.0)


def test_recency_decays_by_the_hour():
    assert scoring.recency_score(NOW, NOW - HOUR, decay_rate=0.995) == pytest.approx(0.995)
    assert scoring.recency_score(NOW, NOW - 2 * HOUR, decay_rate=0.995) == pytest.approx(0.995 ** 2)


def test_recency_smaller_decay_forgets_faster():
    slow = scoring.recency_score(NOW, NOW - 24 * HOUR, decay_rate=0.995)
    fast = scoring.recency_score(NOW, NOW - 24 * HOUR, decay_rate=0.9)
    assert fast < slow  # a smaller decay_rate => lower recency for the same age


def test_recency_never_exceeds_one_for_future_skew():
    # Clock skew (last_accessed in the "future") must not produce recency > 1.0.
    assert scoring.recency_score(NOW, NOW + HOUR, decay_rate=0.995) <= 1.0


# --- M2: importance + relevance ----------------------------------------------
def test_importance_normalizes_1_to_10():
    assert scoring.importance_score(10) == pytest.approx(1.0)
    assert scoring.importance_score(5) == pytest.approx(0.5)
    assert scoring.importance_score(1) == pytest.approx(0.1)


def test_relevance_is_cosine():
    assert scoring.relevance_score([1.0, 0.0, 0.0], [1.0, 0.0, 0.0]) == pytest.approx(1.0)
    assert scoring.relevance_score([1.0, 0.0, 0.0], [0.0, 1.0, 0.0]) == pytest.approx(0.0)


def test_relevance_guards_zero_vector():
    # A zero-norm vector has no direction; defined as 0.0 relevance (no divide-by-zero).
    assert scoring.relevance_score([0.0, 0.0, 0.0], [1.0, 0.0, 0.0]) == pytest.approx(0.0)


# --- M3: the combined three-signal score -------------------------------------
def test_combined_score_is_weighted_sum():
    assert scoring.retrieval_score(0.8, 0.9, 0.7, weights=(1.0, 1.0, 1.0)) == pytest.approx(2.4)


def test_combined_score_needs_all_three():
    w = (1.0, 1.0, 1.0)
    relevant_and_fresh = scoring.retrieval_score(0.8, 0.9, 0.7, weights=w)   # 2.4
    relevant_but_old = scoring.retrieval_score(0.9, 0.1, 0.3, weights=w)     # 1.3
    fresh_but_off_topic = scoring.retrieval_score(0.1, 1.0, 0.2, weights=w)  # 1.3
    assert relevant_and_fresh > relevant_but_old
    assert relevant_and_fresh > fresh_but_off_topic


def test_weights_can_reprioritize():
    # Cranking the recency weight makes a fresh-but-off-topic memory outrank a relevant-but-old one.
    relevant_but_old = scoring.retrieval_score(0.9, 0.1, 0.3, weights=(1.0, 5.0, 1.0))   # 1.7
    fresh_but_off_topic = scoring.retrieval_score(0.1, 1.0, 0.2, weights=(1.0, 5.0, 1.0))  # 5.3
    assert fresh_but_off_topic > relevant_but_old
