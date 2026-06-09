"""[provided] Guiding tests for M2 redact_output. Fail with NotImplementedError until implemented.

Asserts detect→transform: structured PII is removed and reported; clean text is untouched.
"""
import re

from guards import redact_output


def test_email_redacted():
    clean, hits = redact_output("contact me at alice@example.com please")
    assert "alice@example.com" not in clean
    assert "EMAIL" in hits


def test_valid_credit_card_redacted():
    clean, hits = redact_output("card 4242 4242 4242 4242 on file")  # passes Luhn
    assert "4242 4242 4242 4242" not in clean
    assert "CREDIT_CARD" in hits


def test_ssn_redacted():
    clean, hits = redact_output("ssn 078-05-1120")
    assert not re.search(r"\b\d{3}-\d{2}-\d{4}\b", clean)
    assert "SSN" in hits


def test_clean_text_untouched():
    clean, hits = redact_output("The meeting is on Tuesday at noon.")
    assert clean == "The meeting is on Tuesday at noon."
    assert hits == []
