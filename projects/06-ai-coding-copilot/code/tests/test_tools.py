"""[provided] Guiding tests for tools.py — M1 (safe_resolve) and M3 (dispatch_tool). OFFLINE.

These fail with NotImplementedError until you implement the learner cores. read_file /
list_directory / search_code and TOOL_SCHEMAS are provided; the only gaps are safe_resolve and
dispatch_tool. (dispatch of read_file also exercises safe_resolve, so do M1 before M3.)
"""
import pytest

import tools


# ---- M1: safe_resolve --------------------------------------------------------
def test_safe_resolve_accepts_valid_path(fixture_repo):
    p = tools.safe_resolve(fixture_repo, "config.py")
    assert p.is_file()
    assert p.name == "config.py"


def test_safe_resolve_accepts_nested_path(fixture_repo):
    p = tools.safe_resolve(fixture_repo, "src/util.py")
    assert p.read_text(encoding="utf-8").startswith("def add")


def test_safe_resolve_rejects_traversal(fixture_repo):
    with pytest.raises(ValueError):
        tools.safe_resolve(fixture_repo, "../../etc/passwd")


# ---- M3: dispatch_tool -------------------------------------------------------
def test_dispatch_read_file_returns_contents(fixture_repo):
    out = tools.dispatch_tool("read_file", {"path": "config.py"}, fixture_repo)
    assert "DEFAULT_MODEL" in out


def test_dispatch_search_code_finds_symbol(fixture_repo):
    out = tools.dispatch_tool("search_code", {"query": "DEFAULT_MODEL"}, fixture_repo)
    assert "config.py" in out


def test_dispatch_list_directory_lists_entries(fixture_repo):
    out = tools.dispatch_tool("list_directory", {"path": "."}, fixture_repo)
    assert "config.py" in out
    assert "src/" in out


def test_dispatch_unknown_tool_returns_error(fixture_repo):
    out = tools.dispatch_tool("frobnicate", {}, fixture_repo)
    assert "unknown tool" in out.lower()
