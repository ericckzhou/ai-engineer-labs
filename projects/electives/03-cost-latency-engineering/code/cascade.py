"""cascade.py — [learner] The model cascade. This is a learning target (M3).

Answer with the CHEAP model first; ESCALATE to the STRONG model only when the cheap answer isn't
trusted (FrugalGPT, lesson §6). The hard design choice is the escalation signal — here the cheap
model reports a confidence; accept if confidence >= cfg.cascade_threshold, else escalate.

Compose with the cache: a cache hit returns immediately at ~0 cost and calls NO model.
Account for cost via the CostTracker (budget.py) using cfg prices.
"""
from __future__ import annotations

from dataclasses import dataclass

from budget import CostTracker
from cache import SemanticCache
from config import Config, load_config
from feature_backend import cheap_answer, strong_answer


@dataclass
class CascadeResult:
    text: str
    tier: str        # "cache" | "cheap" | "strong"
    cost: float
    cache_hit: bool


def answer(
    query: str,
    *,
    cfg: Config | None = None,
    cache: SemanticCache | None = None,
    tracker: CostTracker | None = None,
) -> CascadeResult:
    """Route a query cheaply, escalating only when needed.

    Order:
      1. If `cache` is given and lookup hits → return (tier="cache", cost=0.0, cache_hit=True),
         and do NOT call a model.
      2. Call cheap_answer(query) -> (text, confidence). Add cfg.cheap_price to the tracker.
         If confidence >= cfg.cascade_threshold → accept (tier="cheap").
      3. Otherwise ESCALATE: call strong_answer(query). Add cfg.strong_price. (tier="strong").
      4. If `cache` is given, store the final answer so a repeat is free next time.

    Examples (default cfg):
        answer("what is 2 + 2")              -> tier="cheap",  cost=0.001, text="4"
        answer("explain the halting problem")-> tier="strong", cost=0.016 (cheap+strong escalation)
        # with a pre-warmed cache:
        answer("what is 2 + 2", cache=warm)  -> tier="cache",  cost=0.0,  cache_hit=True
    """
    cfg = cfg or load_config()
    raise NotImplementedError("M3: implement answer — cache → cheap → escalate on low confidence; track cost.")
