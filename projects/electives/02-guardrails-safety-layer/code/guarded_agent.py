"""guarded_agent.py — [partial] Compose the guards around the (provided) agent.

PROVIDED: the result type, the entry-point signature, and the call into the provided agent.
LEARNER (TODOs): wire the guards in the correct order and fail closed at every step:

    scan_input  →  run_agent  →  redact_output  →  enforce_policy

A BLOCKED input must NEVER reach run_agent (don't spend tokens on an attack; don't let it touch
tools). See source/lesson.agent.md §4.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from agent_backend import run_agent
from config import Config, load_config
from guards import enforce_policy, redact_output, scan_input


@dataclass
class GuardedResult:
    text: str                       # what to actually return to the user
    blocked: bool                   # was the request refused at any stage?
    stage: str | None = None        # which stage blocked: "input" | "output_policy" | None
    evidence: dict = field(default_factory=dict)  # reason/rule/pii-hits for logging


def run_guarded(
    user_input: str,
    *,
    retrieved: str = "",
    cfg: Config | None = None,
) -> GuardedResult:
    cfg = cfg or load_config()

    # TODO(M4): 1. Scan the input (user_input AND retrieved). If blocked, return a refusal
    #              carrying cfg.refusal_text and DO NOT call run_agent.
    # TODO(M4): 2. Run the agent on the allowed input.
    # TODO(M4): 3. Redact PII from the agent's output.
    # TODO(M4): 4. Enforce the output policy on the redacted text. If refused, return the refusal.
    # TODO(M4): 5. Return a GuardedResult with blocked=False and the clean text.
    #
    # Fail closed: if any step raises, return a refusal (blocked=True), not the raw output.
    raise NotImplementedError("M4: compose scan -> run -> redact -> enforce; fail closed; agent never sees a blocked input.")
