"""[provided] Guiding tests for Milestone M4/M5 — baseline.py. Fully OFFLINE (numpy only).

These fail (NotImplementedError) until you implement cosine_similarity / exact_rank / recall_at_k.
The docstring examples in baseline.py mirror these exact cases. Run: python -m pytest tests/test_baseline.py
"""
import numpy as np
import pytest

from baseline import cosine_similarity, exact_rank, recall_at_k


def test_cosine_known_angle():
    assert cosine_similarity(np.array([1.0, 0.0]), np.array([3.0, 4.0])) == pytest.approx(0.6)


def test_cosine_identity_and_opposite():
    v = np.array([1.0, 2.0, 3.0])
    assert cosine_similarity(v, v) == pytest.approx(1.0)
    assert cosine_similarity(v, -v) == pytest.approx(-1.0)


def test_exact_rank():
    docs = [np.array([1.0, 0.0]), np.array([0.0, 1.0]), np.array([0.9, 0.1])]
    assert exact_rank(np.array([1.0, 0.0]), docs, k=2) == [0, 2]


def test_recall_at_k_partial():
    assert recall_at_k([0, 2, 5], [0, 2, 9], k=3) == pytest.approx(2 / 3)


def test_recall_at_k_perfect():
    assert recall_at_k([0, 1, 2], [0, 1, 2], k=3) == pytest.approx(1.0)
