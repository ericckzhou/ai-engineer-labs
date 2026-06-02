"""regression_runner.py — [partial] Milestone M4 — detect regressions between two eval runs.

"Did my prompt change help or hurt?" A flat mean can hide a real per-case regression (a 5→2 drop
and a 3→5 rise nearly cancel in the average). `compare_runs` is the learner core: match cases by id
and flag the ones that got WORSE. The run-a-dataset harness + CLI is provided.

PROVIDED: the RegressionReport dataclass; run_eval (dataset -> judge -> results); main() CLI.
LEARNER:  compare_runs (M4).

Run:  python -m pytest tests/test_regression.py
      python regression_runner.py            # live demo (needs a provider)
"""
from __future__ import annotations

from dataclasses import dataclass

from llm_judge import JudgeResult, judge
from metrics import summarize


@dataclass(frozen=True)
class RegressionReport:
    """[provided] Per-case comparison of a candidate run against a baseline."""
    regressions: list[str]      # case_ids whose score dropped beyond tolerance
    improvements: list[str]     # case_ids whose score rose beyond tolerance
    baseline_mean: float
    candidate_mean: float
    mean_delta: float           # candidate_mean - baseline_mean


def compare_runs(baseline: list[JudgeResult], candidate: list[JudgeResult], *,
                 tolerance: int = 0) -> RegressionReport:
    """[learner] Compare two runs case-by-case and flag regressions / improvements. (M4)

    Match results by case_id (only cases present in BOTH runs are comparable). For each common case,
    delta = candidate.score - baseline.score: a regression is delta < -tolerance, an improvement is
    delta > +tolerance.

    Steps:
      1. Index each run by case_id (e.g. {r.case_id: r.score}).
      2. For every case_id present in BOTH: compute delta = cand - base.
         - delta < -tolerance  -> regression (collect case_id)
         - delta >  tolerance  -> improvement (collect case_id)
      3. baseline_mean / candidate_mean: mean score over the COMMON cases (compare like-for-like).
         If there are no common cases, use 0.0 for both.
      4. mean_delta = candidate_mean - baseline_mean.
      5. Return RegressionReport(regressions, improvements, baseline_mean, candidate_mean, mean_delta).

    The trap: compare like-for-like (same case_ids) — a regression test over different cases measures
    nothing. The point of per-case comparison is to surface a drop the mean would hide.

    Example (mirrors tests/test_regression.py::test_compare_runs_*):
        base = [JudgeResult("a",4,""), JudgeResult("b",5,""), JudgeResult("c",3,"")]
        cand = [JudgeResult("a",4,""), JudgeResult("b",2,""), JudgeResult("c",5,"")]
        r = compare_runs(base, cand, tolerance=0)
        r.regressions   -> ["b"]      # 5 -> 2
        r.improvements  -> ["c"]      # 3 -> 5
        round(r.baseline_mean,2), round(r.candidate_mean,2) -> (4.0, 3.67)
    """
    base_by_id = {r.case_id: r.score for r in baseline}
    cand_by_id = {r.case_id: r.score for r in candidate}
    common = [cid for cid in base_by_id if cid in cand_by_id]

    regressions: list[str] = []
    improvements: list[str] = []
    for cid in common:
        delta = cand_by_id[cid] - base_by_id[cid]
        if delta < -tolerance:
            regressions.append(cid)
        elif delta > tolerance:
            improvements.append(cid)

    if common:
        baseline_mean = sum(base_by_id[cid] for cid in common) / len(common)
        candidate_mean = sum(cand_by_id[cid] for cid in common) / len(common)
    else:
        baseline_mean = candidate_mean = 0.0

    return RegressionReport(
        regressions=regressions,
        improvements=improvements,
        baseline_mean=baseline_mean,
        candidate_mean=candidate_mean,
        mean_delta=candidate_mean - baseline_mean,
    )


# ---- PROVIDED harness — run a dataset through a system-under-test, then judge -----------------
def run_eval(cases, answer_fn) -> list[JudgeResult]:
    """[provided] For each TestCase, produce an answer via answer_fn(question) and judge it.

    `cases` is an iterable of TestCase (see dataset.py); `answer_fn` is the system under test
    (any callable str->str). Returns a list of JudgeResult. Needs a provider (the judge call).
    """
    results = []
    for case in cases:
        answer = answer_fn(case.question)
        results.append(judge(case.id, case.question, answer, reference=case.reference))
    return results


def main() -> None:
    """[provided] Tiny live demo: judge a trivial echo 'system' over the sample dataset."""
    from dataset import load_sample_cases
    from report import format_summary

    cases = load_sample_cases()
    # A throwaway "system under test": replace with a real project's answer function.
    results = run_eval(cases, answer_fn=lambda q: f"(demo answer to: {q})")
    from config import load_config
    cfg = load_config()
    print(format_summary(summarize(results, pass_threshold=cfg.pass_threshold)))


if __name__ == "__main__":
    main()
