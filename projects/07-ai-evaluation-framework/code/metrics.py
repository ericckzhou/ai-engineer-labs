"""metrics.py — [partial] Milestone M3 — turn per-case scores into a decision.

A list of 200 scores is not an answer; a mean and a pass-rate are. `summarize` is the learner core:
aggregate JudgeResults into the numbers you actually ship on. The simple reference-based metrics
(exact_match / contains) are provided as examples of *non-judge* scoring you can mix in.

PROVIDED: exact_match, contains (cheap deterministic metrics), the Summary dataclass.
LEARNER:  summarize (M3).

Run:  python -m pytest tests/test_metrics.py
"""
from __future__ import annotations

from dataclasses import dataclass

from llm_judge import JudgeResult


@dataclass(frozen=True)
class Summary:
    """[provided] Aggregate result of one eval run."""
    n: int
    mean_score: float
    pass_rate: float


# ---- PROVIDED simple metrics (reference-based, no LLM) ----------------------------------------
def exact_match(answer: str, reference: str) -> bool:
    """[provided] True iff answer equals reference after stripping/lowercasing."""
    return answer.strip().lower() == reference.strip().lower()


def contains(answer: str, reference: str) -> bool:
    """[provided] True iff the reference text appears in the answer (case-insensitive)."""
    return reference.strip().lower() in answer.lower()


# ---- LEARNER core ----------------------------------------------------------------------------
def summarize(results: list[JudgeResult], *, pass_threshold: int = 4) -> Summary:
    """[learner] Aggregate JudgeResults into (n, mean_score, pass_rate). (M3)

    The mean answers "how good on average"; the pass-rate (fraction scoring >= threshold) is the
    ship/no-ship number.

    Steps:
      1. n = number of results. If n == 0, return Summary(0, 0.0, 0.0) (don't divide by zero).
      2. mean_score = average of r.score over results.
      3. pass_rate = (count of results with r.score >= pass_threshold) / n.
      4. Return Summary(n, mean_score, pass_rate).

    Example (mirrors tests/test_metrics.py::test_summarize_*):
        rs = [JudgeResult("c1",5,""), JudgeResult("c2",4,""),
              JudgeResult("c3",3,""), JudgeResult("c4",2,"")]
        summarize(rs, pass_threshold=4)  -> Summary(n=4, mean_score=3.5, pass_rate=0.5)
        summarize([], pass_threshold=4)  -> Summary(n=0, mean_score=0.0, pass_rate=0.0)
    """
    raise NotImplementedError("M3: aggregate into n, mean_score, pass_rate (guard empty)")
