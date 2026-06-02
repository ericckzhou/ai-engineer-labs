"""llm_judge.py — [partial] Milestones M1 + M2 — LLM-as-a-judge: prompt + parse.

The judge is one more LLM call (Project 01) whose job is to output a SCORE, not an answer. A strong
LLM judge agrees with humans ~80% of the time — usable, but biased (position / verbosity /
self-enhancement), so the engineering lives in the prompt (sources/papers/mt-bench.md). Two learner
functions: build_judge_prompt (encode the scale + mitigations) and parse_judge_score (turn the
judge's prose back into an int). The model call itself (`judge`) is provided.

PROVIDED: the JudgeResult dataclass; `judge` (the litellm call wiring the two learner fns together).
LEARNER:  build_judge_prompt (M1), parse_judge_score (M2).

Run:  python -m pytest tests/test_llm_judge.py
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class JudgeResult:
    """[provided] One judged case: the score (1..scale) and the judge's reasoning."""
    case_id: str
    score: int
    reasoning: str


def build_judge_prompt(question: str, answer: str, *, reference: str | None = None,
                       scale: int = 5) -> list[dict]:
    """[learner] Build the chat messages for an LLM judge to score `answer`. (M1)

    The prompt is where you mitigate the judge's biases. Bake in: a fixed 1..scale scale, an
    instruction to give the REASONING FIRST and the score last (chain-of-thought improves agreement),
    a request for a parseable format, and — when a reference is provided — reference-guided grading
    (sources/papers/mt-bench.md).

    Steps:
      1. Build a system message: the judge is impartial; it scores on an integer scale 1..scale;
         it must explain its reasoning BEFORE giving the score; it should reply in a parseable form
         (e.g. JSON {"reasoning": "...", "score": N} or a final 'Score: N' line).
      2. Build a user message containing the QUESTION and the ANSWER (clearly labeled). If
         `reference` is not None, include it as the reference/expected answer to grade against.
      3. Return [system_msg, user_msg] as a list of {"role", "content"} dicts.

    The trap: ask for reasoning THEN score, and pin the scale — a bare "rate 1-5" with the number
    first gives worse, less consistent scores (sources/papers/mt-bench.md).

    Example (mirrors tests/test_llm_judge.py::test_build_judge_prompt_*):
        msgs = build_judge_prompt("What is 2+2?", "4", reference="4", scale=5)
        # -> [{"role":"system", "content": "...scale 1..5...reasoning...then...score..."},
        #     {"role":"user",   "content": "...What is 2+2?...Answer: 4...Reference: 4..."}]
    """
    raise NotImplementedError("M1: build a bias-mitigated judge prompt (scale, reasoning-first, reference)")


def parse_judge_score(text: str, *, scale: int = 5) -> tuple[int, str]:
    """[learner] Extract an integer score in [1, scale] from the judge's free-text reply. (M2)

    The judge replies in prose and the format varies: JSON {"score": 4, "reasoning": "..."},
    a 'Score: 4' line, or '...I'd rate this 4/5.'. Parse robustly, CLAMP to [1, scale], and keep the
    reasoning. Fail LOUD (raise ValueError) when there is no score at all — a silent 0 poisons the mean.

    Steps:
      1. Try json.loads(text); if it yields a dict with a numeric "score", use it (and "reasoning"
         if present). (Be tolerant: the model may wrap JSON in prose — fall through on failure.)
      2. Else search the text for a score: prefer 'score: N' or 'N/scale'; else the first integer
         that falls in [1, scale]. Use the whole text as the reasoning.
      3. Clamp the score to [1, scale]. If no integer score can be found at all, raise ValueError.
      4. Return (score, reasoning).

    The trap: clamp out-of-range ('9' on a 1-5 scale -> 5), and raise (never return 0) on no-score.

    Example (mirrors tests/test_llm_judge.py::test_parse_judge_score_*):
        parse_judge_score('{"reasoning": "good", "score": 4}', scale=5) -> (4, "good")
        parse_judge_score("Reasoning: solid.\\nScore: 5", scale=5)       -> (5, "Reasoning: solid.\\nScore: 5")
        parse_judge_score("I'd rate this 3/5.", scale=5)                 -> (3, "I'd rate this 3/5.")
        parse_judge_score("Score: 9", scale=5)                           -> (5, ...)   # clamped
        parse_judge_score("no number here", scale=5)                     -> raises ValueError
    """
    raise NotImplementedError("M2: parse JSON/text into a clamped int score; raise on no-score")


# ---- PROVIDED orchestrator — wires your two functions to a real model call -------------------
def judge(case_id: str, question: str, answer: str, *, reference: str | None = None) -> JudgeResult:
    """[provided] Score one answer with the configured judge model (temperature 0 for repeatability).

    Calls build_judge_prompt (M1) + parse_judge_score (M2), so it raises NotImplementedError until
    those are done. Uses cfg.judge_model — ideally NOT the model under test (avoid self-enhancement
    bias; sources/papers/mt-bench.md).
    """
    import litellm  # local import so the offline tests never need the dependency at import time

    from config import load_config

    cfg = load_config()
    messages = build_judge_prompt(question, answer, reference=reference, scale=cfg.judge_scale)
    resp = litellm.completion(model=cfg.judge_model, messages=messages, temperature=0)
    score, reasoning = parse_judge_score(resp.choices[0].message.content, scale=cfg.judge_scale)
    return JudgeResult(case_id, score, reasoning)
