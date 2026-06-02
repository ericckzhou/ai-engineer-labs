"""[provided] Guiding tests for llm_judge.py — M1 (build_judge_prompt) and M2 (parse_judge_score). OFFLINE.

No network: prompt construction and score parsing are pure functions. The live `judge` call is not
tested here.
"""
import pytest

from llm_judge import build_judge_prompt, parse_judge_score


# ---- M1: build_judge_prompt --------------------------------------------------
def test_build_judge_prompt_returns_role_messages():
    msgs = build_judge_prompt("What is 2+2?", "4", scale=5)
    assert isinstance(msgs, list) and len(msgs) >= 2
    roles = {m["role"] for m in msgs}
    assert "system" in roles and "user" in roles


def test_build_judge_prompt_includes_question_answer_and_scale():
    msgs = build_judge_prompt("What is the capital of France?", "Paris", scale=5)
    blob = " ".join(m["content"] for m in msgs)
    assert "capital of France" in blob
    assert "Paris" in blob
    assert "5" in blob  # the scale appears somewhere


def test_build_judge_prompt_asks_reasoning_before_score():
    msgs = build_judge_prompt("Q", "A", scale=5)
    blob = " ".join(m["content"] for m in msgs).lower()
    # reasoning-before-score mitigation must be present
    assert "reason" in blob and "score" in blob


def test_build_judge_prompt_includes_reference_when_given():
    with_ref = " ".join(m["content"] for m in build_judge_prompt("Q", "A", reference="GOLD", scale=5))
    without = " ".join(m["content"] for m in build_judge_prompt("Q", "A", scale=5))
    assert "GOLD" in with_ref
    assert "GOLD" not in without


# ---- M2: parse_judge_score ---------------------------------------------------
def test_parse_judge_score_json():
    score, reasoning = parse_judge_score('{"reasoning": "covers it well", "score": 4}', scale=5)
    assert score == 4
    assert "covers it well" in reasoning


def test_parse_judge_score_text_score_line():
    score, _ = parse_judge_score("Reasoning: solid but terse.\nScore: 5", scale=5)
    assert score == 5


def test_parse_judge_score_n_over_scale():
    score, _ = parse_judge_score("I'd rate this 3/5.", scale=5)
    assert score == 3


def test_parse_judge_score_clamps_out_of_range():
    score, _ = parse_judge_score("Score: 9", scale=5)
    assert score == 5  # clamped to the scale, never 9 and never 0


def test_parse_judge_score_raises_on_no_score():
    with pytest.raises(ValueError):
        parse_judge_score("no number here at all", scale=5)
