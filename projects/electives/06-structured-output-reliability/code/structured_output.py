"""structured_output.py — [learner] The reliability core. Learning target (M1–M4).

An LLM emits TEXT, not data. To use it programmatically you need a schema-valid object. Naive
`json.loads(response)` fails constantly: markdown fences, chatty prose, bad syntax, and — the sneaky
one — syntactically-valid JSON that violates your schema. This module turns flaky text into a
trustworthy object with a **parse → extract → validate → repair → retry** loop, failing CLOSED when
the budget is exhausted. See source/lesson.agent.md §3–§7.

You implement five functions. They run OFFLINE against fake_backend.generate (which emits the
realistic malformed outputs) — no API key. The live-LLM backend is the extension.
"""
from __future__ import annotations

import json

from config import Config, load_config
from schema import TICKET_SCHEMA


class StructuredOutputError(Exception):
    """Raised when coerce() cannot produce a schema-valid object within the attempt budget."""


def parse_strict(text: str) -> dict:
    """M1 — Strictly parse `text` as a JSON object. NO cleanup. This is the baseline failure rate.

    Use json.loads. Raise (let json.JSONDecodeError propagate) if `text` is not bare JSON — that's
    the point: it shows how often a raw model response is directly usable.

    Example:
        parse_strict('{"category": "billing", "priority": 4, "needs_human": true, "summary": "x"}')
            -> {"category": "billing", "priority": 4, "needs_human": True, "summary": "x"}
        parse_strict('```json\\n{"a": 1}\\n```')   -> raises json.JSONDecodeError (fenced, not bare JSON)
    """
    raise NotImplementedError("M1: return json.loads(text); do not strip or repair anything here.")


def extract_json(text: str) -> dict:
    """M2 — Tolerantly extract the first JSON object from `text` (handles FORMAT NOISE only).

    Strip ```json ... ``` / ``` ... ``` fences, ignore any prose before/after, find the first
    balanced {...} object, and json.loads it. This fixes 'fenced' and 'prose' outputs. It does NOT
    fix schema violations — that's validate()/coerce()'s job.

    Hint: locate the first '{', then scan forward tracking brace depth (respecting strings) to the
    matching '}'. Raise ValueError if no JSON object is found.

    Example:
        extract_json('```json\\n{"priority": 3}\\n```')                 -> {"priority": 3}
        extract_json('Sure! Here you go: {"priority": 2}. Thanks!')    -> {"priority": 2}
        extract_json('no json here')                                   -> raises ValueError
    """
    raise NotImplementedError("M2: strip fences, find the first balanced {...}, json.loads it.")


def validate(obj: dict, schema: dict = TICKET_SCHEMA, *, cfg: Config | None = None) -> list[str]:
    """M3 — Return a list of human-readable validation errors ([] means valid).

    For each field in `schema`, check, in order: required-but-missing, wrong type, enum, min/max.
    The classic trap: in Python `bool` is a subclass of `int`, so `isinstance(True, int)` is True —
    check `bool` fields BEFORE int-typed fields, and reject a bool where an int is required.
    Return MESSAGES (e.g. "priority: 9 exceeds max 5"), because coerce() feeds them into the repair
    prompt so the model knows exactly what to fix.

    Example:
        validate({"category":"billing","priority":4,"needs_human":True,"summary":"x"})  -> []
        validate({"category":"payments","priority":"high","needs_human":True,"summary":"x"})
            -> ["category: 'payments' not in ['billing','technical','account','other']",
                "priority: expected int, got str"]
        validate({"category":"technical","priority":9,"summary":"x"})
            -> ["needs_human: required field missing", "priority: 9 exceeds max 5"]
    """
    cfg = cfg or load_config()
    raise NotImplementedError("M3: walk the schema; return a list of error strings ([] if valid).")


def build_repair_prompt(message: str, bad_output: str, errors: list[str]) -> str:
    """M4a — Build the prompt that asks the model to FIX an invalid output.

    A good repair prompt includes: the original task/message, the model's previous (bad) output, and
    the SPECIFIC validation errors, and instructs it to return ONLY valid JSON. Including the errors
    is the whole reason repair works better than blind retry — the model is told what was wrong.

    Must contain each error string and the original `message` (a test checks this).
    """
    raise NotImplementedError("M4a: compose a repair prompt that includes `message`, `bad_output`, and `errors`.")


def coerce(message: str, *, backend=None, schema: dict = TICKET_SCHEMA, cfg: Config | None = None) -> dict:
    """M4 — The reliability loop: turn a free-text support `message` into a schema-valid dict.

    Steps (use the provided fake_backend by default):
      1. Build a task prompt from `message` and call backend.generate(prompt) for the first attempt.
      2. extract_json the response, then validate it.
      3. If valid -> return the dict (success).
      4. If invalid and cfg.allow_repair and attempts remain -> build_repair_prompt and generate again.
      5. If the budget (cfg.max_attempts) is exhausted without a valid object -> raise
         StructuredOutputError (FAIL CLOSED — never return an unvalidated object).

    Edge cases to handle: extract_json itself can raise (treat as an error and repair/continue);
    a 'clean' output validates on attempt 0 (no repair); an 'unfixable' case exhausts the budget.

    Example (offline, fake backend):
        coerce("My invoice charged me twice this month and I want a refund.")
            -> {"category": "billing", "priority": 4, "needs_human": True, "summary": ...}   # 1 attempt
        coerce("asdkfj this is not really a support request lorem ipsum 12345")
            -> raises StructuredOutputError                                                  # fail closed
    """
    cfg = cfg or load_config()
    if backend is None:
        import fake_backend
        backend = fake_backend
    raise NotImplementedError(
        "M4: implement the extract->validate->repair->retry loop; fail closed via StructuredOutputError."
    )
