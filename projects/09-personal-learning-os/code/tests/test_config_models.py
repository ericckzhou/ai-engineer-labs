"""[provided] Tests that pin the CURRENT config.py provider/model resolution. Fully OFFLINE.

Keeps the suite in sync with the canonical config.py models (local Ollama default:
ollama/qwen3.5:4b chat + ollama/nomic-embed-text 768-dim embeddings; Groq preferred cloud) and with
this project's Config knobs (top_k, route_threshold, link_min_shared_tags). If those defaults change,
update both config.py and this test together. No NotImplementedError here — config.py is provided, so
these pass today and guard against silent drift.
"""
import importlib

import pytest

_ENV_KEYS = [
    "LLM_MODEL", "CHATBOT_MODEL", "EMBEDDING_MODEL", "OLLAMA_MODEL", "OLLAMA_EMBEDDING_MODEL",
    "USE_OLLAMA", "GROQ_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY",
    "CHATBOT_TEMPERATURE", "CHATBOT_MAX_TOKENS",
    "OS_TOP_K", "OS_ROUTE_THRESHOLD", "OS_LINK_MIN_SHARED_TAGS",
]


@pytest.fixture
def clean_env(monkeypatch):
    for k in _ENV_KEYS:
        monkeypatch.delenv(k, raising=False)
    import config
    importlib.reload(config)
    return config


def test_embedding_default_is_local_nomic_when_no_keys(clean_env):
    # No OPENAI key and no USE_OLLAMA -> keyless local embedder.
    assert clean_env.default_embedding_model() == "ollama/nomic-embed-text"


def test_embedding_uses_ollama_when_use_ollama_set(clean_env, monkeypatch):
    monkeypatch.setenv("USE_OLLAMA", "1")
    assert clean_env.default_embedding_model() == "ollama/nomic-embed-text"


def test_embedding_explicit_override_wins(clean_env, monkeypatch):
    monkeypatch.setenv("EMBEDDING_MODEL", "text-embedding-3-small")
    assert clean_env.default_embedding_model() == "text-embedding-3-small"


def test_chat_default_is_ollama_when_use_ollama(clean_env, monkeypatch):
    monkeypatch.setenv("USE_OLLAMA", "1")
    assert clean_env.default_model() == "ollama/qwen3.5:4b"


def test_chat_prefers_groq_cloud_when_key_present(clean_env, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    assert clean_env.default_model() == "groq/llama-3.3-70b-versatile"


def test_config_exposes_os_knobs(clean_env):
    # The per-project Config carries the OS's routing/retrieval/graph knobs with documented defaults.
    cfg = clean_env.load_config()
    assert cfg.top_k == 5
    assert cfg.route_threshold == 0.0
    assert cfg.link_min_shared_tags == 1
    assert cfg.temperature == 0.2
