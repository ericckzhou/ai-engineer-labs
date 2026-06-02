"""cost_tracker.py — [partial] Turn usage tokens into dollars.

PROVIDED: PRICES table (Anthropic figures filled; add your default Groq price), CostTracker
state + summary(), and the guiding tests.
LEARNER: cost_of() and CostTracker.record(). The provided tests (tests/test_cost_tracker.py)
tell you when you're correct — and the docstring examples mirror them. No network needed.

Run:  python -m pytest tests/test_cost_tracker.py     (from the code/ directory)
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
    """[learner] Return the USD cost of one call.

    Steps:
      1. look up (in_price, out_price) = PRICES[model]  (KeyError on unknown model is CORRECT —
         never silently return 0 for a model you don't have a price for).
      2. cost = input_tokens/1e6 * in_price + output_tokens/1e6 * out_price.
      3. return that float.

    Example (mirrors tests/test_cost_tracker.py — uses claude-sonnet-4-6 at $3/$15 per MTok,
    which IS in PRICES; the default Groq model is left for you to add):
        cost_of("claude-sonnet-4-6", 1_000_000, 0)  -> 3.0     # 1M input @ $3/MTok
        cost_of("claude-sonnet-4-6", 0, 1_000_000)  -> 15.0    # 1M output @ $15/MTok
        cost_of("no-such-model", 100, 100)          -> raises KeyError
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
        """[learner] Add one turn's usage; return THAT turn's cost. Update the running totals.

        Steps:
          1. turn_cost = cost_of(model, input_tokens, output_tokens).
          2. update self.turns (+1), self.total (+turn_cost), self.input_tokens,
             self.output_tokens.
          3. return turn_cost  (the cost of THIS turn, not the running total).

        Example (mirrors tests/test_cost_tracker.py::test_tracker_accumulates):
            t = CostTracker()
            t.record("claude-sonnet-4-6", 1_000_000, 0)  -> 3.0    # returns THIS turn's cost
            t.record("claude-sonnet-4-6", 0, 1_000_000)  -> 15.0
            t.total    # -> 18.0   (running total)
            t.turns    # -> 2
        """
        # TODO(learner): compute this turn's cost via cost_of(), update totals, return it.
        raise NotImplementedError("Implement CostTracker.record()")

    def summary(self) -> str:
        return (
            f"{self.turns} turns | in={self.input_tokens} out={self.output_tokens} tok "
            f"| total=${self.total:.4f}"
        )
