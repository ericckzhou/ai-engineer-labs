"""[provided] Drift guard — passes today. Asserts the tiers/thresholds the cores read."""
from config import Config, load_config


def test_config_has_cost_fields():
    cfg = load_config()
    assert isinstance(cfg, Config)
    assert cfg.cheap_price < cfg.strong_price, "cheap tier must cost less than strong"
    assert 0.0 < cfg.cache_threshold <= 1.0
    assert 0.0 < cfg.cascade_threshold <= 1.0
    assert cfg.budget_ceiling > 0
