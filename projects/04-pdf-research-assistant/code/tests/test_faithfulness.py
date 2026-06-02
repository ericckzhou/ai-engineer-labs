"""[provided] Guiding test for Milestone M5 — faithfulness.faithfulness_score(). Fully OFFLINE (pure math).

Fails (NotImplementedError) until faithfulness_score is implemented. check_faithfulness() needs a
provider (it asks the model to verify each claim) and is exercised via the pipeline, not here. The
docstring example in faithfulness.py mirrors test_faithfulness_score.
Run: python -m pytest tests/test_faithfulness.py
"""
import pytest

import faithfulness


def test_faithfulness_score():
    assert faithfulness.faithfulness_score([True, True, False]) == pytest.approx(2 / 3)
    assert faithfulness.faithfulness_score([True, True, True]) == pytest.approx(1.0)
    assert faithfulness.faithfulness_score([False, False]) == pytest.approx(0.0)


def test_faithfulness_empty_is_vacuously_faithful():
    # No claims -> nothing to contradict the context -> defined as 1.0 (documented choice).
    assert faithfulness.faithfulness_score([]) == pytest.approx(1.0)


def test_faithfulness_in_unit_range():
    score = faithfulness.faithfulness_score([True, False, True, False, True])
    assert 0.0 <= score <= 1.0
    assert score == pytest.approx(0.6)
