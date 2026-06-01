"""[provided] Guiding tests for Milestone M4 — cosine_similarity from scratch.

These run with NO network: they assert the mathematical invariants on hand-built vectors. They will
FAIL (NotImplementedError) until you implement cosine_similarity(). When they pass, your cosine is
correct on the cases that matter. Run:  python -m pytest tests/test_similarity.py
"""
import numpy as np
import pytest

from similarity_calculator import cosine_similarity


def test_identical_vectors_score_one():
    v = np.array([1.0, 2.0, 3.0, 4.0])
    assert cosine_similarity(v, v) == pytest.approx(1.0)


def test_opposite_vectors_score_minus_one():
    v = np.array([1.0, 2.0, 3.0])
    assert cosine_similarity(v, -v) == pytest.approx(-1.0)


def test_orthogonal_vectors_score_zero():
    a = np.array([1.0, 0.0])
    b = np.array([0.0, 1.0])
    assert cosine_similarity(a, b) == pytest.approx(0.0)


def test_known_angle_3_4_5():
    # (1,0) vs (3,4): cos = 3 / (1 * 5) = 0.6
    a = np.array([1.0, 0.0])
    b = np.array([3.0, 4.0])
    assert cosine_similarity(a, b) == pytest.approx(0.6)


def test_ignores_magnitude_only_direction():
    a = np.array([1.0, 1.0])
    b = np.array([10.0, 10.0])  # same direction, far larger magnitude
    assert cosine_similarity(a, b) == pytest.approx(1.0)


def test_result_within_bounds():
    rng = np.random.default_rng(0)
    for _ in range(20):
        a = rng.standard_normal(16)
        b = rng.standard_normal(16)
        s = cosine_similarity(a, b)
        assert -1.0 - 1e-9 <= s <= 1.0 + 1e-9
