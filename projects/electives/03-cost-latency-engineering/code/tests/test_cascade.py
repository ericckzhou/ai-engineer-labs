"""[provided] Guiding tests for M3 cascade.answer. Fail with NotImplementedError until implemented.

Asserts cheap-first acceptance, escalation on low confidence, and the cache-hit short-circuit.
"""
import cascade
from cache import SemanticCache
from config import load_config


def test_easy_query_accepts_cheap():
    cfg = load_config()
    res = cascade.answer("what is 2 + 2", cfg=cfg)
    assert res.tier == "cheap"
    assert res.text == "4"
    assert abs(res.cost - cfg.cheap_price) < 1e-9
    assert res.cache_hit is False


def test_hard_query_escalates_to_strong():
    cfg = load_config()
    res = cascade.answer("explain the halting problem", cfg=cfg)
    assert res.tier == "strong"
    assert res.text == "Whether an arbitrary program halts is undecidable."
    # cost reflects BOTH calls (cheap then strong)
    assert abs(res.cost - (cfg.cheap_price + cfg.strong_price)) < 1e-9


def test_cache_hit_short_circuits():
    cfg = load_config()
    warm = SemanticCache()
    warm.store("what is 2 + 2", "4")
    res = cascade.answer("what is 2 + 2", cfg=cfg, cache=warm)
    assert res.tier == "cache"
    assert res.cost == 0.0
    assert res.cache_hit is True
