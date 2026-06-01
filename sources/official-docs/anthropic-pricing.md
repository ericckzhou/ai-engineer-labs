# Anthropic Pricing & Token Cost

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** Anthropic
**Date:** Accessed 2026-06-01
**URL:** https://platform.claude.com/docs/en/docs/about-claude/pricing
**Accessed:** 2026-06-01

## Why This Source Matters

Cost is the constraint that shapes every production LLM decision. This source gives the exact per-token prices and the formula to turn `usage` fields into dollars — the basis for the cost tracker built in Project 1. It also states the rule of thumb for estimating tokens from text.

## Key Claims

### Token estimation
- A token is a piece of text the model processes. Rough estimate: **1 token ≈ 4 characters ≈ 0.75 words** in English. Exact count varies by language and content.
- Note: Opus 4.7+ use a new tokenizer that may use up to ~35% more tokens for the same text than earlier models.

### Pricing is per million tokens (MTok), split input vs. output
Output is consistently ~5× the input price. Selected current rates (USD / MTok):

| Model | Input | Output |
|-------|-------|--------|
| Claude Opus 4.5 / 4.6 / 4.7 | $5 | $25 |
| Claude Opus 4.1 | $15 | $75 |
| Claude Sonnet 4.5 / 4.6 | $3 | $15 |
| Claude Haiku 4.5 | $1 | $5 |

### Cost formula
```
cost = (input_tokens  / 1_000_000) * input_price_per_mtok
     + (output_tokens / 1_000_000) * output_price_per_mtok
```
Worked example (Opus 4.8, one turn): 50,000 input + 15,000 output
- input:  50,000 × $5  / 1,000,000 = $0.25
- output: 15,000 × $25 / 1,000,000 = $0.375
- total ≈ **$0.625**

### Why chatbots get expensive
- The whole conversation history is resent every turn (see `anthropic-messages-api.md`), so `input_tokens` grows each turn. A long conversation pays for the full history repeatedly.
- **Prompt caching** mitigates this: cache reads cost 0.1× the base input price (a 5-minute cache write costs 1.25×, a 1-hour write 2×). Reusing a large system prompt or history across calls pays off after one or two cache reads.

### Volume reference
- ~10,000 support conversations at ~3,700 tokens each on Haiku 4.5 ≈ **$37 total**.

## Relevant To

- concepts: [tokens, token-cost, cost-projection, prompt-caching, model-selection]
- projects: [01-ai-chatbot]

## Notes

- Prices change; always re-verify against claude.com/pricing before quoting absolute numbers. The *structure* (per-MTok, input vs output ~1:5, history-resend cost growth) is the durable lesson.
- Cost-optimization hierarchy from the docs: pick the cheapest adequate model (Haiku→Sonnet→Opus), use prompt caching for repeated context, batch non-urgent work, monitor usage.
