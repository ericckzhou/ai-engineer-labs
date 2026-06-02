"""[provided] Guiding tests for the context guard — context.py.

These run with NO network: estimate_tokens / within_budget / trim_to_budget are pure list logic.
They FAIL (NotImplementedError) until you implement context.py, and the docstring examples in
context.py mirror them exactly. trim_to_budget is asserted by PROPERTY (system kept, within budget,
newest turns survive, input not mutated) rather than one exact output, so your dropping strategy has
room — it just has to honor the contract. Run from code/:  python -m pytest tests/test_context.py
"""
from context import estimate_tokens, trim_to_budget, within_budget

# 40-char contents → exactly 10 tokens each at ~4 chars/token, so the arithmetic is clean.
SYS = {"role": "system", "content": "s" * 4}        # 4 chars  → 1 token
U1 = {"role": "user", "content": "1" * 40}          # 40 chars → 10 tokens
A1 = {"role": "assistant", "content": "A" * 40}     # 10 tokens
U2 = {"role": "user", "content": "2" * 40}          # 10 tokens
A2 = {"role": "assistant", "content": "B" * 40}     # 10 tokens


def test_estimate_tokens_counts_chars_over_four():
    assert estimate_tokens([U1]) == 10                      # 40 chars // 4
    assert estimate_tokens([U1], system="y" * 8) == 12      # (40 + 8) // 4


def test_within_budget_is_inclusive():
    assert within_budget([U1], 10) is True                  # 10 <= 10
    assert within_budget([U1], 9) is False                  # 10 > 9


def test_trim_keeps_system_and_newest_within_budget():
    msgs = [SYS, U1, A1, U2, A2]                            # total = 1 + 40 = 41 tokens
    result = trim_to_budget(msgs, 25)

    assert result[0] == SYS                                 # system message is never dropped
    assert estimate_tokens(result) <= 25                    # actually within budget now
    assert U2 in result and A2 in result                   # newest turns survive
    assert U1 not in result                                 # oldest turn dropped first


def test_trim_does_not_mutate_input_and_is_noop_when_under_budget():
    msgs = [SYS, U1, A1, U2, A2]
    result = trim_to_budget(msgs, 10_000)                  # already within budget

    assert estimate_tokens(result) <= 10_000
    assert len(result) == 5                                 # nothing dropped
    assert msgs == [SYS, U1, A1, U2, A2]                    # caller's list untouched
