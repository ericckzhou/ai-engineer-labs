"""[provided] Guiding tests for M1–M4. Fail with NotImplementedError until implemented.

Run from code/:  python -m pytest
"""
import json

import pytest

import fake_backend
from structured_output import (
    StructuredOutputError,
    build_repair_prompt,
    coerce,
    extract_json,
    parse_strict,
    validate,
)

VALID = '{"category": "billing", "priority": 4, "needs_human": true, "summary": "x"}'


# ---- M1: strict parse --------------------------------------------------------
def test_parse_strict_accepts_bare_json():
    assert parse_strict(VALID)["category"] == "billing"


def test_parse_strict_rejects_fenced():
    with pytest.raises(json.JSONDecodeError):
        parse_strict("```json\n" + VALID + "\n```")


# ---- M2: tolerant extraction (format noise) ----------------------------------
def test_extract_strips_code_fence():
    assert extract_json("```json\n" + VALID + "\n```")["priority"] == 4


def test_extract_from_prose():
    assert extract_json("Sure! Here you go: " + VALID + " Hope that helps!")["category"] == "billing"


def test_extract_raises_without_json():
    with pytest.raises(ValueError):
        extract_json("there is absolutely no json here")


# ---- M3: schema validation ---------------------------------------------------
def test_validate_accepts_valid():
    assert validate({"category": "billing", "priority": 4, "needs_human": True, "summary": "x"}) == []


def test_validate_flags_bad_enum_and_type():
    errs = validate({"category": "payments", "priority": "high", "needs_human": True, "summary": "x"})
    assert any("category" in e for e in errs)
    assert any("priority" in e for e in errs)


def test_validate_flags_missing_field_and_out_of_range():
    errs = validate({"category": "technical", "priority": 9, "summary": "x"})
    assert any("needs_human" in e for e in errs)
    assert any("priority" in e for e in errs)


def test_validate_rejects_bool_where_int_required():
    # bool is a subclass of int in Python — priority=True must still be rejected.
    errs = validate({"category": "billing", "priority": True, "needs_human": True, "summary": "x"})
    assert any("priority" in e for e in errs)


# ---- M4a: repair prompt ------------------------------------------------------
def test_repair_prompt_includes_message_and_errors():
    p = build_repair_prompt("change my email", '{"oops": 1}', ["needs_human: required field missing"])
    assert "change my email" in p
    assert "needs_human: required field missing" in p


# ---- M4: the coerce loop -----------------------------------------------------
def test_coerce_clean_first_try():
    out = coerce("My invoice charged me twice this month and I want a refund.")
    assert out["category"] == "billing"
    assert validate(out) == []


def test_coerce_extracts_fenced_without_repair():
    out = coerce("The mobile app crashes every time I open the settings screen.")
    assert validate(out) == []
    assert out["category"] == "technical"


def test_coerce_repairs_schema_violation():
    out = coerce("I was charged a late fee but I paid on time, please review.")
    assert validate(out) == []
    assert out["category"] == "billing"  # 'payments' was repaired into a valid enum value


def test_coerce_fails_closed_on_unfixable():
    with pytest.raises(StructuredOutputError):
        coerce("asdkfj this is not really a support request lorem ipsum 12345")


def test_coerce_no_repair_when_disabled():
    from config import Config

    cfg = Config(allow_repair=False)
    # schema-violating case can't be repaired when repair is off -> fail closed
    with pytest.raises(StructuredOutputError):
        coerce("I was charged a late fee but I paid on time, please review.", cfg=cfg)
