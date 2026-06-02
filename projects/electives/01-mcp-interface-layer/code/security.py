"""security.py — [learner] The TRUST BOUNDARY. Milestones M1–M3.

Across a protocol boundary, every argument and URI comes from a model running inside someone
else's host — it is UNTRUSTED. The JSON inputSchema you write in memory_tools.py is only
ADVISORY: a model can ignore it. This module is where you ENFORCE the contract — bound every
input and contain every resource URI, and FAIL CLOSED (raise SecurityError) on anything off.

This is Project 06's tool-sandboxing lesson, now across a *process* boundary: validate after
parsing, never trust a raw string, and reject rather than guess.

PROVIDED: SecurityError, the function signatures + contracts, and the bounds (from config.py).
LEARNER: the checks inside each function (M1–M3).

Run:  python -m pytest tests/test_security.py
"""
from __future__ import annotations

from config import load_config

cfg = load_config()


class SecurityError(ValueError):
    """Raised when an untrusted argument or URI violates the contract. Fail closed."""


def validate_search_args(args: dict) -> tuple[str, int]:
    """[learner] Validate memory_search arguments → return (query, k). (M1)

    Steps:
      1. Read args["query"]; require a non-empty str (reject missing/None/empty/non-str
         with SecurityError) — strip surrounding whitespace.
      2. Read args.get("k"); default to cfg.default_k when absent. Coerce to int; reject a
         non-integer / <= 0 with SecurityError.
      3. CLAMP k to the ceiling cfg.max_k (a model asking for k=10_000_000 must not reach the
         backend). Clamping (not rejecting) a too-large k is friendlier than failing.
      4. Return (query, k).

    Example (mirrors tests/test_security.py::test_validate_search_args):
      validate_search_args({"query": "demo"})              -> ("demo", 5)     # default_k
      validate_search_args({"query": "demo", "k": 999})    -> ("demo", 50)    # clamped to max_k
      validate_search_args({"query": ""})                  -> raises SecurityError
      validate_search_args({"k": 3})                       -> raises SecurityError  # no query
    """
    raise NotImplementedError("M1: validate and clamp the search arguments")


def validate_save_args(args: dict) -> tuple[str, str, float]:
    """[learner] Validate memory_save arguments → return (text, kind, importance). (M2)

    Steps:
      1. Read args["text"]; require a non-empty str. Reject text longer than
         cfg.max_text_chars with SecurityError (an unbounded write is a memory/latency risk).
      2. Read args.get("kind"); default to "episodic". Reject anything not in
         cfg.allowed_kinds with SecurityError (whitelist, don't sanitize).
      3. Read args.get("importance"); default 5.0. Coerce to float; reject out of
         [cfg.min_importance, cfg.max_importance] with SecurityError.
      4. Return (text, kind, importance).

    Example (mirrors tests/test_security.py::test_validate_save_args):
      validate_save_args({"text": "demo June 20"})                  -> ("demo June 20", "episodic", 5.0)
      validate_save_args({"text": "x", "kind": "semantic", "importance": 8}) -> ("x", "semantic", 8.0)
      validate_save_args({"text": "x", "kind": "rumor"})            -> raises SecurityError
      validate_save_args({"text": "z"*5000})                        -> raises SecurityError  # too long
    """
    raise NotImplementedError("M2: validate and bound the save arguments")


def validate_resource_uri(uri: str) -> str:
    """[learner] Validate a resource URI and return the entry id. (M3)

    Contain the namespace exactly like a path sandbox (Project 06), but for URIs: only the
    project's own scheme, only the entries path, only a well-formed id. Reject everything else.

    Steps:
      1. Require a str beginning with f"{cfg.resource_scheme}://entries/" (e.g.
         "memory://entries/"). Reject any other scheme ("file://", "http://") with SecurityError.
      2. Take the remainder as the id. Reject ids containing "/", "..", whitespace, or that are
         empty — i.e. reject path traversal and nested paths. Fail closed.
      3. (Optional, stricter) require the id to match the backend's id shape, e.g. r"^m\\d+$".
      4. Return the id (e.g. "m3").

    Example (mirrors tests/test_security.py::test_validate_resource_uri):
      validate_resource_uri("memory://entries/m3")           -> "m3"
      validate_resource_uri("memory://entries/../secret")    -> raises SecurityError  # traversal
      validate_resource_uri("file:///etc/passwd")            -> raises SecurityError  # foreign scheme
      validate_resource_uri("memory://entries/")             -> raises SecurityError  # empty id
    """
    raise NotImplementedError("M3: parse and contain the resource URI")
