"""prompts.py — [learner] The PROMPT layer (user-controlled templates). Milestone M4.

Prompts are the primitive a USER invokes (`prompts/list`, `prompts/get`): reusable, parameterized
message templates the host surfaces (e.g. as a slash-command). They are NOT actions the model
takes (that's a tool) and NOT raw context the app reads (that's a resource). One prompt here:
`reflect_on`, which pulls recalled memories about a topic into a ready-to-send message.

SDK-agnostic: no `mcp` import; plain dicts only.

PROVIDED: nothing beyond the function; the backend recall is reused.
LEARNER: PROMPT_DEFINITIONS + get_prompt (M4).

Run:  python -m pytest tests/test_prompts.py
"""
from __future__ import annotations

from config import load_config

cfg = load_config()

# [learner] M4 — the prompt contracts the host surfaces. Fill with one dict per prompt:
#   {"name": "reflect_on", "description": <what it does>,
#    "arguments": [{"name": "topic", "description": "...", "required": True}]}
PROMPT_DEFINITIONS: list[dict] = [
    {
        "name": "reflect_on",
        "description": "Pull recalled memories about a topic into a ready-to-send reflection prompt.",
        "arguments": [
            {"name": "topic", "description": "The topic to reflect on.", "required": True},
        ],
    },
]


def get_prompt(name: str, args: dict, backend) -> dict:
    """[learner] Render a prompt template → {"description": str, "text": str}. (M4)

    Steps:
      1. Reject an unknown `name` (only "reflect_on" is defined) — raise KeyError/ValueError.
      2. Read args["topic"]; require a non-empty str (raise if missing — reuse a guard or
         security check).
      3. Recall context: backend.search(topic, k=cfg.default_k) → the relevant entries.
      4. Build a message `text` that (a) names the topic and (b) includes the recalled entries
         (e.g. one bullet per entry), then asks the model to reflect / summarize what is known.
      5. Return {"description": f"Reflect on {topic}", "text": <the assembled message>}.

    Example (mirrors tests/test_prompts.py::test_reflect_on_injects_memories):
      # backend has m0 "the StarcallOS demo is on June 20"
      get_prompt("reflect_on", {"topic": "StarcallOS"}, backend)
        -> {"description": "Reflect on StarcallOS",
            "text": "...StarcallOS... the StarcallOS demo is on June 20 ..."}  # topic + recalled text present
    """
    if name != "reflect_on":
        raise KeyError(f"unknown prompt: {name!r}")
    topic = args.get("topic")
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("topic must be a non-empty string")
    topic = topic.strip()

    hits = backend.search(topic, k=cfg.default_k)
    if hits:
        recalled = "\n".join(f"- {m.text}" for m in hits)
    else:
        recalled = "(no saved memories found)"
    text = (
        f"Reflect on what I know about {topic}.\n\n"
        f"Recalled memories:\n{recalled}\n\n"
        f"Summarize what is known about {topic} and note any gaps."
    )
    return {"description": f"Reflect on {topic}", "text": text}
