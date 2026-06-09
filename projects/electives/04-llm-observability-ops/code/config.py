"""config.py — [provided] Settings & provider/environment loading. NOT the learning target.

CANONICAL TEMPLATE — keep the PROVIDER-RESOLUTION BLOCK identical across projects.
The `Config` dataclass is PER-PROJECT.

For THIS elective the core runs OFFLINE on replayable trace fixtures. The DRIFT THRESHOLDS and
sample rate in `Config` ARE used by monitor.py — read them from here, do not hardcode.
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
    # PER-PROJECT: telemetry + drift-detection thresholds.
    model: str = field(default_factory=default_model)

    service_name: str = "ai-agent"

    # Drift thresholds (monitor.detect_drift reads these).
    error_rate_delta: float = 0.20   # flag if a route's error-rate rises by more than this (abs)
    latency_ratio: float = 1.5       # flag if avg latency rises beyond baseline x this
    cost_ratio: float = 1.5          # flag if total cost rises beyond baseline x this

    # Online eval: fraction of traffic an async judge would sample (extension).
    sample_rate: float = 0.10


def load_config() -> Config:
    return Config()
