"""cost_tracker.py — [partial] Turn usage tokens into dollars.

LEARNER TODO: implement cost_of() and CostTracker.record().
The provided tests (tests/test_cost_tracker.py) tell you when you're correct —
run `python -m pytest` from this directory. No network needed.
"""
from __future__ import annotations

# ($/MTok input, $/MTok output)
PRICES: dict[str, tuple[float, float]] = {
    # Default provider is Groq. Add your default model's real price from Groq's official
    # pricing page (https://groq.com/pricing) — do NOT guess. Looking it up from the source
    # IS the first step of the cost milestone. Until you add it, cost_of() correctly raises
    # KeyError for the default model rather than inventing a number.
    # "groq/llama-3.3-70b-versatile": (<in>, <out>),  # TODO(learner): fill from source
    #
    # Anthropic figures (source: sources/official-docs/anthropic-pricing.md) — kept for the
    # lesson's worked cost example and for provider switching:
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5": (1.0, 5.0),
}


def cost_of(model: str, input_tokens: int, output_tokens: int) -> float:
    """Return the USD cost of one call.

    cost = input_tokens/1e6 * in_price + output_tokens/1e6 * out_price
    Raise KeyError on an unknown model — never silently return 0.
    """
    # TODO(learner): look up the price tuple in PRICES and apply the formula above.
    raise NotImplementedError("Implement cost_of() — see source/lesson.agent.md §3 'The Math'")


class CostTracker:
    """Accumulates spend across a session."""

    def __init__(self) -> None:
        self.turns = 0
        self.total = 0.0
        self.input_tokens = 0
        self.output_tokens = 0

    def record(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Add one turn's usage; return THAT turn's cost. Update the running totals."""
        # TODO(learner): compute this turn's cost via cost_of(), update totals, return it.
        raise NotImplementedError("Implement CostTracker.record()")

    def summary(self) -> str:
        return (
            f"{self.turns} turns | in={self.input_tokens} out={self.output_tokens} tok "
            f"| total=${self.total:.4f}"
        )
