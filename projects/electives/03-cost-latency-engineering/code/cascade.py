"""cascade.py — [REFERENCE SOLUTION] verified copy (solns branch). Starter (NotImplementedError) on main."""
from __future__ import annotations

from dataclasses import dataclass

from budget import CostTracker
from cache import SemanticCache
from config import Config, load_config
from feature_backend import cheap_answer, strong_answer


@dataclass
class CascadeResult:
    text: str
    tier: str
    cost: float
    cache_hit: bool


def answer(query, *, cfg: Config | None = None, cache: SemanticCache | None = None,
           tracker: CostTracker | None = None) -> CascadeResult:
    cfg = cfg or load_config()
    if cache is not None:
        hit = cache.lookup(query, cfg=cfg)
        if hit is not None:
            return CascadeResult(hit, "cache", 0.0, True)

    text, confidence = cheap_answer(query)
    cost = cfg.cheap_price
    if tracker is not None:
        tracker.add(cfg.cheap_price)
    tier = "cheap"

    if confidence < cfg.cascade_threshold:
        text = strong_answer(query)
        cost += cfg.strong_price
        if tracker is not None:
            tracker.add(cfg.strong_price)
        tier = "strong"

    if cache is not None:
        cache.store(query, text, cfg=cfg)
    return CascadeResult(text, tier, cost, False)
