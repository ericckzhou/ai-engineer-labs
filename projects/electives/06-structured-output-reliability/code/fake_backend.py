"""fake_backend.py — [reference] A deterministic offline 'LLM' that emits realistic malformed output.

No provider, no network — this is what makes M1–M5 gradeable. `generate(prompt)` figures out which
CASE the prompt is about (the support message text appears in the prompt) and returns that case's
response for the current attempt:

  attempt 0 (the original prompt)      -> the RAW, often-malformed first response
  attempt >=1 (a repair prompt)        -> the case's REPAIRED (valid) response — UNLESS the case is
                                          marked unfixable, which stays malformed forever so coerce()
                                          must fail closed.

Attempt counting is per-case and internal (decoupled from your repair-prompt wording), so you can't
fail grading on phrasing. Call `reset()` between runs — the test suite does this automatically
(see tests/conftest.py). The live-LLM backend (call a real model) is the extension.

The five failure shapes mirror what real models actually do:
  clean    — valid JSON, first try (the happy path; ~1 attempt)
  fenced   — valid JSON wrapped in a ```json ... ``` markdown block (format noise; extract fixes it)
  prose    — valid JSON with a chatty preamble/trailer ("Sure! Here you go: { ... }. Hope that helps!")
  schema   — syntactically valid JSON that VIOLATES the schema (bad enum / out-of-range / missing) →
             needs a repair round
  unfixable — never returns valid output → coerce must exhaust its budget and fail closed
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class _Case:
    cid: str
    text: str           # the support message; appears verbatim in every prompt about this case
    kind: str           # clean | fenced | prose | schema | unfixable
    raw: str            # the malformed (or clean) first response
    fixed: str          # the valid response returned on a repair attempt (ignored if unfixable)
    fixable: bool


# Keep these texts UNIQUE — generate() identifies the case by substring match on `text`.
CASES: list[_Case] = [
    _Case(
        cid="clean-1",
        text="My invoice charged me twice this month and I want a refund.",
        kind="clean",
        raw='{"category": "billing", "priority": 4, "needs_human": true, "summary": "Double charge; wants refund."}',
        fixed='{"category": "billing", "priority": 4, "needs_human": true, "summary": "Double charge; wants refund."}',
        fixable=True,
    ),
    _Case(
        cid="fenced-1",
        text="The mobile app crashes every time I open the settings screen.",
        kind="fenced",
        raw='```json\n{"category": "technical", "priority": 3, "needs_human": false, "summary": "App crashes opening settings."}\n```',
        fixed='{"category": "technical", "priority": 3, "needs_human": false, "summary": "App crashes opening settings."}',
        fixable=True,
    ),
    _Case(
        cid="prose-1",
        text="How do I change the email address on my account?",
        kind="prose",
        raw='Sure! Here is the structured ticket:\n{"category": "account", "priority": 2, "needs_human": false, "summary": "Wants to change account email."}\nLet me know if you need anything else.',
        fixed='{"category": "account", "priority": 2, "needs_human": false, "summary": "Wants to change account email."}',
        fixable=True,
    ),
    _Case(
        cid="schema-enum-1",
        text="I was charged a late fee but I paid on time, please review.",
        kind="schema",
        # valid JSON, but category is not in the enum and priority is a string -> validation fails -> repair
        raw='{"category": "payments", "priority": "high", "needs_human": true, "summary": "Disputes a late fee."}',
        fixed='{"category": "billing", "priority": 4, "needs_human": true, "summary": "Disputes a late fee; paid on time."}',
        fixable=True,
    ),
    _Case(
        cid="schema-missing-1",
        text="Nothing loads after I log in, just a blank white page.",
        kind="schema",
        # valid JSON, but 'needs_human' is missing and priority is out of range -> validation fails -> repair
        raw='{"category": "technical", "priority": 9, "summary": "Blank page after login."}',
        fixed='{"category": "technical", "priority": 5, "needs_human": true, "summary": "Blank page after login (outage)."}',
        fixable=True,
    ),
    _Case(
        cid="unfixable-1",
        text="asdkfj this is not really a support request lorem ipsum 12345",
        kind="unfixable",
        # never valid: not JSON at all, and the 'repair' stays broken -> coerce must fail closed
        raw="I'm not sure how to categorize this one, sorry!",
        fixed="I still can't produce that, sorry!",
        fixable=False,
    ),
]

_BY_TEXT = {c.text: c for c in CASES}
_calls: dict[str, int] = {}


def reset() -> None:
    """Clear per-case attempt counters. Call between evaluation runs / tests."""
    _calls.clear()


def _match(prompt: str) -> _Case | None:
    for c in CASES:
        if c.text in prompt:
            return c
    return None


def generate(prompt: str) -> str:
    """Return the fake model's response for `prompt`.

    Deterministic: first call for a case returns its raw output; later calls (your repair prompts)
    return the fixed output, unless the case is unfixable. Raises if the prompt mentions no known case.
    """
    case = _match(prompt)
    if case is None:
        raise ValueError("fake_backend: prompt does not reference any known support message")
    n = _calls.get(case.cid, 0)
    _calls[case.cid] = n + 1
    if n == 0:
        return case.raw
    return case.fixed if case.fixable else case.raw
