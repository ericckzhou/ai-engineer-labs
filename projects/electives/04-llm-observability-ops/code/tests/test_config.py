"""[provided] Drift guard — passes today. Asserts the thresholds monitor.py reads."""
from config import Config, load_config


def test_config_has_drift_thresholds():
    cfg = load_config()
    assert isinstance(cfg, Config)
    assert 0.0 < cfg.error_rate_delta < 1.0
    assert cfg.latency_ratio > 1.0
    assert cfg.cost_ratio > 1.0
    assert 0.0 < cfg.sample_rate <= 1.0
