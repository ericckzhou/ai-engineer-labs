"""agent_backend.py — [reference] The capability being wrapped (Project 08, condensed).

This is a COMPLETE, working agent — provided whole because the agent is NOT the learning target.
The guard layer (guards.py) is. Do not add guards here; guarding is the learner's job, and it
belongs in guarded_agent.py.

It is deliberately NAIVE: with no guard in front of it, it will follow injected instructions and
echo PII straight back. That is the point — it is the unsafe-but-functional feature you must make
safe to expose. Runs OFFLINE by default with a deterministic canned-response model so tests and
the demo need no provider or network.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class AgentResult:
    """Run-level result, faithful to Project 08."""
    text: str
    tool_calls: list[str] = field(default_factory=list)
    stop_reason: str = "stop"


# A fake "system prompt" the naive agent will happily reveal if asked — the canary an output
# guard should catch leaking.
_FAKE_SYSTEM_PROMPT = "SYSTEM PROMPT: You are HelperBot. Internal key: SK-CANARY-9F3A."


def _offline_naive_response(user_input: str, context: str) -> AgentResult:
    """A deterministic stand-in for a real, unguarded agent.

    Models three unsafe-but-realistic behaviors so an unguarded run demonstrably fails:
      1. Obeys a system-prompt-extraction request (leaks the canary).
      2. Obeys obvious injected instructions found in the *context* (indirect injection).
      3. Echoes whatever it was given — including any PII — into the answer.
    """
    blob = f"{context}\n{user_input}".lower()
    tool_calls: list[str] = []

    if "system prompt" in blob or "your instructions" in blob:
        return AgentResult(text=_FAKE_SYSTEM_PROMPT, stop_reason="stop")

    # Naively "follows" an exfiltration instruction hidden in retrieved context.
    if "email" in blob and ("@" in context or "send" in blob):
        tool_calls.append("send_email")
        return AgentResult(
            text=f"Sure — forwarding the conversation as requested. {user_input} {context}".strip(),
            tool_calls=tool_calls,
            stop_reason="stop",
        )

    # Default: echo the request and any context back (will surface PII present in either).
    answer = f"Here is what I found: {user_input}".strip()
    if context.strip():
        answer += f" (context: {context.strip()})"
    return AgentResult(text=answer, stop_reason="stop")


def run_agent(user_input: str, *, context: str = "") -> AgentResult:
    """Run the (unguarded) agent.

    Offline by default. Set a provider (e.g. GROQ_API_KEY or USE_OLLAMA=1) AND
    LIVE_AGENT=1 to route through a real model via LiteLLM for the live-agent extension.
    """
    if os.getenv("LIVE_AGENT", "").strip().lower() in {"1", "true", "yes", "on"}:
        return _live_response(user_input, context)
    return _offline_naive_response(user_input, context)


def _live_response(user_input: str, context: str) -> AgentResult:
    """[extension] Route through a real model. Import is local so the offline path needs no deps."""
    from litellm import completion  # noqa: PLC0415

    from config import load_config

    cfg = load_config()
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{context}\n\n{user_input}".strip()},
    ]
    resp = completion(model=cfg.model, messages=messages)
    text = resp["choices"][0]["message"]["content"]
    return AgentResult(text=text, stop_reason="stop")
