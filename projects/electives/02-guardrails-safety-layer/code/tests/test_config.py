"""[provided] Drift guard — passes today. Asserts config.py exposes the bounds/policy that
guards.py reads. If this fails, config.py was edited away from the lesson contract."""
from config import Config, load_config


def test_config_has_guard_policy_fields():
    cfg = load_config()
    assert isinstance(cfg, Config)
    # PII policy
    assert cfg.pii_entities == ("EMAIL", "PHONE", "CREDIT_CARD", "SSN")
    assert cfg.pii_operator in {"mask", "replace", "redact"}
    # Output policy
    assert cfg.output_max_chars > 0
    assert "answer" in cfg.allowed_output_keys
    assert any("SYSTEM" in s for s in cfg.forbidden_output_substrings)
    # Fail-closed default
    assert isinstance(cfg.refusal_text, str) and cfg.refusal_text
    # Input bound
    assert cfg.max_input_chars > 0
