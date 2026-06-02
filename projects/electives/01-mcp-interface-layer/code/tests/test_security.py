"""[provided] Guiding tests for the TRUST BOUNDARY (security.py). OFFLINE. M1–M3.

Fail with NotImplementedError until you implement the validators, then pass. They assert the
contract: valid input is parsed/clamped; hostile input fails closed with SecurityError.
"""
import pytest

from security import (
    SecurityError,
    validate_resource_uri,
    validate_save_args,
    validate_search_args,
)


# ---- M1: search args -------------------------------------------------------------
def test_validate_search_args_defaults_and_clamp():
    assert validate_search_args({"query": "demo"}) == ("demo", 5)        # default_k
    assert validate_search_args({"query": "demo", "k": 999}) == ("demo", 50)  # clamped to max_k


def test_validate_search_args_rejects_bad_input():
    with pytest.raises(SecurityError):
        validate_search_args({"query": ""})        # empty query
    with pytest.raises(SecurityError):
        validate_search_args({"k": 3})             # missing query


# ---- M2: save args ---------------------------------------------------------------
def test_validate_save_args_valid():
    assert validate_save_args({"text": "demo June 20"}) == ("demo June 20", "episodic", 5.0)
    assert validate_save_args(
        {"text": "x", "kind": "semantic", "importance": 8}) == ("x", "semantic", 8.0)


def test_validate_save_args_rejects_bad_input():
    with pytest.raises(SecurityError):
        validate_save_args({"text": "x", "kind": "rumor"})   # kind not whitelisted
    with pytest.raises(SecurityError):
        validate_save_args({"text": "z" * 5000})             # over max_text_chars (4000)
    with pytest.raises(SecurityError):
        validate_save_args({"text": "x", "importance": 99})  # out of range


# ---- M3: resource URI containment ------------------------------------------------
def test_validate_resource_uri_valid():
    assert validate_resource_uri("memory://entries/m3") == "m3"


def test_validate_resource_uri_rejects_escape_and_foreign_scheme():
    with pytest.raises(SecurityError):
        validate_resource_uri("memory://entries/../secret")   # traversal
    with pytest.raises(SecurityError):
        validate_resource_uri("file:///etc/passwd")           # foreign scheme
    with pytest.raises(SecurityError):
        validate_resource_uri("memory://entries/")            # empty id
