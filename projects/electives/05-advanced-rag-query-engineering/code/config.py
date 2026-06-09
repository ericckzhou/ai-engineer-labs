"""config.py — [provided] Settings & provider/environment loading. NOT the learning target.

CANONICAL TEMPLATE — keep the PROVIDER-RESOLUTION BLOCK identical across projects.
The `Config` dataclass is PER-PROJECT.

For THIS elective the core runs OFFLINE on a provided corpus with canned transforms. The retrieval
params in `Config` ARE used by advanced_rag.py — read them from here, do not hardcode.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()

# ---- CANONICAL: provider resolution (do not edit per project) ----------------
PROVIDER_DEFAULTS: list[tuple[str, str]] = [
    ("GROQ_API_KEY", "groq/llama-3.3-70b-versatile"),
    ("ANTHROPIC_API_KEY", "claude-sonnet-4-6"),
    ("OPENAI_API_KEY", "gpt-4o-mini"),
]
OLLAMA_CHAT_DEFAULT = "ollama/qwen3.5:4b"
OLLAMA_EMBED_DEFAULT = "ollama/nomic-embed-text"


def _use_ollama() -> bool:
    return os.getenv("USE_OLLAMA", "").strip().lower() in {"1", "true", "yes", "on"}


def default_model() -> str:
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
    explicit = os.getenv("EMBEDDING_MODEL")
    if explicit:
        return explicit
    if _use_ollama() or not os.getenv("OPENAI_API_KEY"):
        return os.getenv("OLLAMA_EMBEDDING_MODEL", OLLAMA_EMBED_DEFAULT)
    return "text-embedding-3-small"
# ---- end canonical block -----------------------------------------------------


@dataclass(frozen=True)
class Config:
    # PER-PROJECT: retrieval params for the query-engineering pipeline.
    model: str = field(default_factory=default_model)

    retrieve_k: int = 4            # chunks retrieved PER (sub-)query
    rerank_top_n: int = 3          # chunks kept after fusion re-ranking
    faithfulness_threshold: float = 0.66   # the eval gate (RAGAS-style)


def load_config() -> Config:
    return Config()
