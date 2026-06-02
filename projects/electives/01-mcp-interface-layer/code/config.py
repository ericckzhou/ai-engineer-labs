"""config.py — [provided] Settings & provider/environment loading. NOT the learning target.

CANONICAL TEMPLATE — source of truth: skills/lesson-generator/templates/config.py
Stamped into each project's code/ by the lesson-generator skill.

The PROVIDER-RESOLUTION BLOCK below is canonical: keep it identical across every project so
it never drifts. It makes the LLM provider swappable by key/string. Order of preference:
explicit model > local Ollama (USE_OLLAMA, free, no key) > cloud key (Groq > Anthropic > OpenAI).
The `Config` dataclass is PER-PROJECT — add or remove fields for this project's needs.

For THIS elective the live LLM is optional: the memory backend runs offline with a
deterministic local embedder, so the provider block matters only if you flip the backend to
real embeddings (an extension) or point a host's model at the server. The bounds in `Config`
ARE used by `security.py` — read them from here, don't hardcode them.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()  # reads code/.env into the environment (API keys + optional overrides)

# ---- CANONICAL: provider resolution (do not edit per project) ----------------
# Cloud provider preference order → (env key, default model via LiteLLM).
# Groq is the preferred cloud provider: it has a free tier. First key present wins.
PROVIDER_DEFAULTS: list[tuple[str, str]] = [
    ("GROQ_API_KEY", "groq/llama-3.3-70b-versatile"),
    ("ANTHROPIC_API_KEY", "claude-sonnet-4-6"),
    ("OPENAI_API_KEY", "gpt-4o-mini"),
]

# Local Ollama defaults (no API key, $0). Opt in with USE_OLLAMA=1. Requires a running
# Ollama server (localhost:11434) with these models pulled. LiteLLM routes "ollama/..."
# (use "ollama_chat/<model>" for higher-quality chat output if you prefer).
OLLAMA_CHAT_DEFAULT = "ollama/qwen3.5:4b"
OLLAMA_EMBED_DEFAULT = "ollama/nomic-embed-text"  # 768-dim


def _use_ollama() -> bool:
    return os.getenv("USE_OLLAMA", "").strip().lower() in {"1", "true", "yes", "on"}


def default_model() -> str:
    """Pick a default chat model. Explicit LLM_MODEL/CHATBOT_MODEL always wins.

    Then: local Ollama if USE_OLLAMA is set; else the first cloud provider whose key is
    present (Groq preferred). If nothing is configured, fall back to the Groq default so
    the resulting error clearly points at the intended provider.
    """
    explicit = os.getenv("LLM_MODEL") or os.getenv("CHATBOT_MODEL")
    if explicit:
        return explicit
    if _use_ollama():
        return os.getenv("OLLAMA_MODEL", OLLAMA_CHAT_DEFAULT)
    for env_key, model in PROVIDER_DEFAULTS:
        if os.getenv(env_key):
            return model
    return PROVIDER_DEFAULTS[0][1]


def default_embedding_model() -> str:
    """Pick a default embedding model. Explicit EMBEDDING_MODEL always wins.

    Groq/Anthropic have no embedding endpoint, so local Ollama is the natural keyless
    default: used when USE_OLLAMA is set or when no OPENAI_API_KEY is present. With an
    OpenAI key (and no USE_OLLAMA), default to OpenAI's small embedding model.
    """
    explicit = os.getenv("EMBEDDING_MODEL")
    if explicit:
        return explicit
    if _use_ollama() or not os.getenv("OPENAI_API_KEY"):
        return os.getenv("OLLAMA_EMBEDDING_MODEL", OLLAMA_EMBED_DEFAULT)
    return "text-embedding-3-small"
# ---- end canonical block -----------------------------------------------------


@dataclass(frozen=True)
class Config:
    # PER-PROJECT: the MCP server identity + the trust-boundary bounds.
    # security.py reads the bounds from here so there is one source of truth.
    model: str = field(default_factory=default_model)

    # Server identity (sent during MCP capability negotiation / `serverInfo`).
    server_name: str = "personal-memory"
    server_version: str = "0.1.0"
    resource_scheme: str = "memory"          # memory://entries/{id}

    # Tool input bounds (enforced in security.py — the schema is only advisory).
    default_k: int = 5                       # memory_search default top-k
    max_k: int = 50                          # clamp ceiling for k
    max_text_chars: int = 4000               # cap on a saved memory's text
    min_importance: float = 1.0
    max_importance: float = 10.0
    allowed_kinds: tuple[str, ...] = ("episodic", "semantic", "procedural")


def load_config() -> Config:
    """Return a frozen Config. API keys are loaded into the environment by load_dotenv()."""
    return Config()
