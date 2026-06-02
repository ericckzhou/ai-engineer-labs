"""report.py — [provided] Format eval results as readable text.

Turns a Summary / RegressionReport into something you can print or paste into a PR. Not the learning
target — formatting only.
"""
from __future__ import annotations

from metrics import Summary
from regression_runner import RegressionReport


def format_summary(s: Summary) -> str:
    return (f"Eval summary: n={s.n}  mean_score={s.mean_score:.2f}  "
            f"pass_rate={s.pass_rate:.0%}")


def format_regression(r: RegressionReport) -> str:
    arrow = "▲" if r.mean_delta > 0 else ("▼" if r.mean_delta < 0 else "=")
    lines = [
        f"Regression report: baseline={r.baseline_mean:.2f} -> candidate={r.candidate_mean:.2f} "
        f"({arrow} {r.mean_delta:+.2f})",
        f"  regressions ({len(r.regressions)}): {', '.join(r.regressions) or 'none'}",
        f"  improvements ({len(r.improvements)}): {', '.join(r.improvements) or 'none'}",
    ]
    if r.regressions:
        lines.append("  ⚠ regressions present — do not ship without review.")
    return "\n".join(lines)
