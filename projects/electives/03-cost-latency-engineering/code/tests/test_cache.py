"""[provided] Guiding tests for M2 SemanticCache. Fail with NotImplementedError until implemented.

Asserts the threshold gate: exact + near-duplicate hit; unrelated + lexically-close-but-different
miss (the latter is the correct miss that a too-loose threshold would turn into a false hit).
"""
from cache import SemanticCache


def test_exact_hit():
    c = SemanticCache()
    c.store("what is the capital of france", "Paris")
    assert c.lookup("what is the capital of france") == "Paris"


def test_near_duplicate_hit():
    c = SemanticCache()
    c.store("what is the capital of france", "Paris")
    # ~0.93 similarity — a re-asked question, same answer.
    assert c.lookup("what is the capital of france please") == "Paris"


def test_unrelated_miss():
    c = SemanticCache()
    c.store("what is the capital of france", "Paris")
    assert c.lookup("who wrote pride and prejudice") is None


def test_close_but_different_is_a_correct_miss():
    # ~0.83 similarity (different country) — must MISS at the default 0.90 threshold.
    # A looser threshold would return "Paris" here: the false hit (see FAILURE_ANALYSIS).
    c = SemanticCache()
    c.store("what is the capital of france", "Paris")
    assert c.lookup("what is the capital of austria") is None


def test_empty_cache_miss():
    assert SemanticCache().lookup("anything") is None
