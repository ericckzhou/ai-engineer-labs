"""tools.py — [provided] The agent's action space + sandbox — the COMPLETE Project 06 tool layer.

You built every function in this file in Project 06 (AI Coding Copilot): the sandbox
(`safe_resolve`), the file ops, the dispatcher, and the tool schemas (the agent-computer
interface). It is provided here in full and already implemented, because Project 08 is not about
the tool loop — it is about making an autonomous loop RELIABLE. Spend your effort on safety.py,
agent.py, and evaluate.py. If anything here is unfamiliar, re-read projects/06-ai-coding-copilot.

PROVIDED (all of it): safe_resolve, read_file, list_directory, search_code, dispatch_tool,
TOOL_SCHEMAS. Nothing in this file is a learner target.
"""
from __future__ import annotations

from pathlib import Path

# ---- TOOL SCHEMAS — the agent-computer interface the model programs against ------------------
# The model picks a tool and fills its args from the `description` + `parameters` ALONE.
TOOL_SCHEMAS = [
    {"type": "function", "function": {
        "name": "read_file",
        "description": ("Read the full text of a single file in the repository. Use this to inspect "
                        "source you need to complete the task. `path` is relative to the repo root "
                        "(e.g. 'src/config.py'). Returns the file's contents, or an error string if "
                        "the path is missing or escapes the repo."),
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "description": "File path relative to the repo root."}},
            "required": ["path"]}}},
    {"type": "function", "function": {
        "name": "list_directory",
        "description": ("List the files and subdirectories of a directory in the repository. Use this "
                        "to discover what exists before reading. `path` is relative to the repo root; "
                        "use '.' for the root. Returns one entry per line (directories end in '/')."),
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "description": "Directory path relative to the repo root; '.' for root."}},
            "required": []}}},
    {"type": "function", "function": {
        "name": "search_code",
        "description": ("Search the repository for a literal substring (like grep) and return matching "
                        "lines with their file path and line number. Use this to locate where a symbol "
                        "or string is defined or used. Returns matches as 'path:line: text'."),
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string", "description": "Literal substring to search for."}},
            "required": ["query"]}}},
]

MAX_FILE_BYTES = 64_000  # don't dump a giant file into the prompt
_SKIP_PARTS = {".git", "__pycache__", ".venv", "node_modules"}


def safe_resolve(repo_root, rel_path) -> Path:
    """[provided] Resolve `rel_path` under `repo_root`, raising ValueError if it escapes. (P06 M1)

    Tool arguments come from the MODEL — untrusted input. Resolve the path, then confirm it stays
    inside the repo root; otherwise fail closed. The containment check is done AFTER resolving so
    that '..' segments, symlinks, and absolute paths cannot slip past a naive string check.
    """
    base = Path(repo_root).resolve()
    target = (base / rel_path).resolve()
    if base != target and base not in target.parents:
        raise ValueError(f"path escapes repo root: {rel_path!r}")
    return target


def read_file(repo_root, path: str) -> str:
    """[provided] Return the text of `path` (relative to repo_root), sandboxed and size-capped."""
    try:
        target = safe_resolve(repo_root, path)
    except ValueError as e:
        return f"Error: {e}"
    if not target.is_file():
        return f"Error: not a file: {path}"
    return target.read_text(encoding="utf-8", errors="replace")[:MAX_FILE_BYTES]


def list_directory(repo_root, path: str = ".") -> str:
    """[provided] Return one entry per line for the directory `path` (relative to repo_root)."""
    try:
        target = safe_resolve(repo_root, path)
    except ValueError as e:
        return f"Error: {e}"
    if not target.is_dir():
        return f"Error: not a directory: {path}"
    entries = sorted(p.name + ("/" if p.is_dir() else "") for p in target.iterdir())
    return "\n".join(entries) if entries else "(empty)"


def search_code(repo_root, query: str) -> str:
    """[provided] grep-like literal search; returns 'relpath:line: text' for each match (capped)."""
    base = Path(repo_root).resolve()
    hits: list[str] = []
    for p in sorted(base.rglob("*")):
        if not p.is_file() or any(part in _SKIP_PARTS for part in p.parts):
            continue
        try:
            for i, line in enumerate(p.read_text(encoding="utf-8", errors="strict").splitlines(), 1):
                if query in line:
                    hits.append(f"{p.relative_to(base)}:{i}: {line.strip()}")
        except (UnicodeDecodeError, OSError):
            continue
    return "\n".join(hits[:50]) if hits else f"No matches for {query!r}."


def dispatch_tool(name: str, arguments: dict, repo_root) -> str:
    """[provided] Route a parsed tool call to the matching file op and return its string result.

    Tool results are always STRINGS — the model reads them as its observation. An unknown tool
    returns an error string rather than raising (a bad name from the model shouldn't kill the loop).

    NOTE for Project 08: these provided tools fail *softly* (they return "Error: ..." strings). A
    REAL tool — a network call, a subprocess — can RAISE. Your run_agent (M3) must wrap dispatch in
    try/except so a raising tool becomes a recoverable observation, not a fatal crash.
    """
    if name == "read_file":
        return read_file(repo_root, arguments["path"])
    if name == "list_directory":
        return list_directory(repo_root, arguments.get("path", "."))
    if name == "search_code":
        return search_code(repo_root, arguments["query"])
    return f"Error: unknown tool {name!r}"
