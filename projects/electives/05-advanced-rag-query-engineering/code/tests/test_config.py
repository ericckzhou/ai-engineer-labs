"""[provided] Drift guard — passes today. Asserts the retrieval params the pipeline reads."""
from config import Config, load_config


def test_config_has_retrieval_params():
    cfg = load_config()
    assert isinstance(cfg, Config)
    assert cfg.retrieve_k >= 1
    assert cfg.rerank_top_n >= 1
    assert 0.0 < cfg.faithfulness_threshold <= 1.0
