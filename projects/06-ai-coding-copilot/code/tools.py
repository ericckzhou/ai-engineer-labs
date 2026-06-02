"""tools.py — [partial] Milestones M1 + M3 — the copilot's action space (file tools) + sandbox/dispatch.

A "tool" is just a function the MODEL is allowed to call. The model never sees these bodies — only
TOOL_SCHEMAS below (name + description + params). That schema IS the interface: "the description is
the API" (sources/articles/building-effective-agents.md). Two pieces are PROVIDED plumbing (the file
ops + the schemas); two are the learning target: safe_resolve (the security boundary) and
dispatch_tool (the router that turns a model request into an action).

PROVIDED: read_file / list_directory / search_code (sandboxed file ops), TOOL_SCHEMAS.
LEARNER:  safe_resolve (M1 — reject path escapes), dispatch_tool (M3 — route a call to a tool).

Run:  python -m pytest tests/test_tools.py
"""
from __future__ import annotations

from pathlib import Path

# ---- TOOL SCHEMAS [provided] — the agent-computer interface the model programs against --------
# The model picks a tool and fills its args from the `description` + `parameters` ALONE. Be specific.
TOOL_SCHEMAS = [
    {"type": "function", "function": {
        "name": "read_file",
        "description": ("Read the full text of a single file in the repository. Use this to inspect "
                        "source you need to answer a question. `path` is relative to the repo root "
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
    """[learner] Resolve `rel_path` under `repo_root`, raising ValueError if it escapes. (M1)

    Tool arguments come from the MODEL — treat them as untrusted input. A `read_file` that will
    happily open '../../etc/passwd' is a directory-traversal hole. Resolve the path and confirm it
    stays inside the repo root; otherwise FAIL CLOSED with a ValueError.

    Steps:
      1. base = Path(repo_root).resolve()  — the absolute, symlink-free repo root.
      2. target = (base / rel_path).resolve()  — joining then resolving collapses any '..' segments
         (and absolutizes an absolute rel_path) so the check below is sound.
      3. Containment check: target must BE base, or have base among its parents
         (i.e. `base == target or base in target.parents`). If not, raise ValueError.
      4. Return target.

    The trap: do the containment check AFTER resolving. Scanning the raw string for '..' is not
    enough — symlinks and absolute paths slip past a string check; resolving first is what makes it
    sound.

    Example (mirrors tests/test_tools.py::test_safe_resolve_*):
        safe_resolve("/work/repo", "src/config.py")    -> Path("/work/repo/src/config.py")
        safe_resolve("/work/repo", "../../etc/passwd")  -> raises ValueError
    """
    base = Path(repo_root).resolve()
    target = (base / rel_path).resolve()
    if base != target and base not in target.parents:
        raise ValueError(f"path escapes repo root: {rel_path!r}")
    return target


# ---- PROVIDED file ops — each path-taking op routes through safe_resolve (your M1) ------------
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


# ---- DISPATCH [learner] ----------------------------------------------------------------------
def dispatch_tool(name: str, arguments: dict, repo_root) -> str:
    """[learner] Route a parsed tool call to the matching file op and return its string result. (M3)

    The loop hands you the tool `name` the model asked for and the parsed `arguments` dict
    (parse_tool_calls already json.loads'd them). Call the right provided function. Tool results are
    always STRINGS — the model reads them as its observation. On an unknown tool, return an error
    string (don't raise — a bad tool name from the model shouldn't kill the loop).

    Steps:
      1. name == "read_file":      return read_file(repo_root, arguments["path"]).
      2. name == "list_directory": return list_directory(repo_root, arguments.get("path", ".")).
      3. name == "search_code":    return search_code(repo_root, arguments["query"]).
      4. otherwise:                return f"Error: unknown tool {name!r}".

    Example (mirrors tests/test_tools.py::test_dispatch_*):
        dispatch_tool("read_file", {"path": "config.py"}, repo)  -> "<contents of config.py>"
        dispatch_tool("frobnicate", {}, repo)                    -> "Error: unknown tool 'frobnicate'"
    """
    if name == "read_file":
        return read_file(repo_root, arguments["path"])
    if name == "list_directory":
        return list_directory(repo_root, arguments.get("path", "."))
    if name == "search_code":
        return search_code(repo_root, arguments["query"])
    return f"Error: unknown tool {name!r}"
