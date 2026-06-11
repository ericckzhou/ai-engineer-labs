"""[provided] Config drift guard. Passes on the starter."""
import dataclasses

import pytest

from config import load_config


def test_defaults():
    cfg = load_config()
    assert cfg.max_attempts == 3
    assert cfg.allow_repair is True
    assert cfg.strict_enum is True
    assert isinstance(cfg.model, str) and cfg.model


def test_config_is_frozen():
    cfg = load_config()
    with pytest.raises(dataclasses.FrozenInstanceError):
        cfg.max_attempts = 1  # type: ignore[misc]
