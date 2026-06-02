"""[provided] Tests that pin the CURRENT config.py provider/model resolution. Fully OFFLINE.

Keeps the suite in sync with the canonical config.py models (local Ollama default:
ollama/qwen3.5:4b chat + ollama/nomic-embed-text 768-dim embeddings; Groq preferred cloud). If those
defaults change, update both config.py and this test together. No NotImplementedError here — config.py
is provided, so these pass today and guard against silent model drift.
"""
import importlib

import pytest

_ENV_KEYS = [
    "LLM_MODEL", "CHATBOT_MODEL", "EMBEDDING_MODEL", "OLLAMA_MODEL", "OLLAMA_EMBEDDING_MODEL",
    "USE_OLLAMA", "GROQ_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY",
    "JUDGE_MODEL", "JUDGE_SCALE", "EVAL_PASS_THRESHOLD", "EVAL_REGRESSION_TOLERANCE",
]


@pytest.fixture
def clean_env(monkeypatch):
    for k in _ENV_KEYS:
        monkeypatch.delenv(k, raising=False)
    import config
    importlib.reload(config)
    return config


def test_embedding_default_is_local_nomic_when_no_keys(clean_env):
    assert clean_env.default_embedding_model() == "ollama/nomic-embed-text"


def test_chat_default_is_ollama_when_use_ollama(clean_env, monkeypatch):
    monkeypatch.setenv("USE_OLLAMA", "1")
    assert clean_env.default_model() == "ollama/qwen3.5:4b"


def test_chat_prefers_groq_cloud_when_key_present(clean_env, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    assert clean_env.default_model() == "groq/llama-3.3-70b-versatile"


def test_config_exposes_eval_knobs(clean_env):
    # The per-project Config carries the eval-harness knobs with the documented defaults.
    cfg = clean_env.load_config()
    assert cfg.judge_scale == 5
    assert cfg.pass_threshold == 4
    assert cfg.regression_tolerance == 0
    # judge_model defaults to the same provider resolution as the model under test
    assert cfg.judge_model == clean_env.default_model()
