# Anthropic Prompt Caching

**Type:** official-docs
**Tier:** 1 (Official Doc)
**URL:** https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching
**Accessed:** 2026-06-09
**Publisher:** Anthropic
**Link:** https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching
**Related (in repo):** `sources/official-docs/anthropic-pricing.md` (the per-MTok base prices the
multipliers below apply to)

> Primary source for **Elective 03 — Cost & Latency Engineering** (the prompt-caching lever, M1).
> Faithful summary of the mechanics; the canonical doc above governs exact thresholds, which
> change by model — do not hardcode a model's minimum or invent prices.

---

## What it caches

A **stable prompt prefix** reused across requests: tool definitions, the system prompt, long
documents/context, few-shot examples, and prior conversation turns. You mark the end of the
stable region with a `cache_control: {"type": "ephemeral"}` breakpoint (up to 4 explicit
breakpoints; or automatic caching that moves the breakpoint forward as a conversation grows).

## The one rule that makes it work

**The cached prefix must be identical across requests and come BEFORE the variable content.** A
breakpoint placed on a block that changes every request (a timestamp, the incoming user message)
caches nothing useful. Order: stable content first → breakpoint → variable content last.

## Cost mechanics (the reason it's a cost lever)

Multipliers on the model's **base input** price (`anthropic-pricing.md`):

| Operation | Cost vs. base input |
|-----------|---------------------|
| Cache **write**, 5-min TTL | ~1.25× |
| Cache **write**, 1-hour TTL | ~2× |
| Cache **read** (hit) | ~0.1× |
| Uncached input (after breakpoint) | 1× |

So a cache **write** costs slightly *more* than a normal call; the savings come from every
subsequent **read** at ~1/10th the input price. Caching only pays off when the prefix is reused
enough times to amortize the write — a real engineering tradeoff, not a free win.

## TTL

Default **5-minute** ephemeral cache (refreshed free on each hit). Optional **1-hour** TTL at the
higher write multiplier — for prompts reused less than every 5 min, or agentic steps that take
longer than 5 min between calls.

## Minimums and verification

There is a **minimum cacheable prefix length** (on the order of ~1k tokens, model-dependent;
check the doc for the current number per model). Shorter prefixes silently don't cache. Verify
caching actually happened via the response `usage`:
`total_input = cache_read_input_tokens + cache_creation_input_tokens + input_tokens`.

## Why This Source Matters

It is the first, cheapest cost lever: no quality change at all (same model, same output), pure
input-cost reduction on a reused prefix. The learner measures `cache_read_input_tokens` to prove
the saving — and learns that caching a *variable* prefix saves nothing (the common mistake).

## Key Claims

- Caching reuses a stable prompt prefix (tool definitions, system prompt, long documents, few-shot examples, prior turns) marked with a `cache_control` breakpoint.
- The cached prefix must be identical and come *before* variable content; a breakpoint on per-request content (timestamp, incoming message) caches nothing useful.
- Cost mechanics make it a real tradeoff: cache write ~1.25× (5-min) / ~2× (1-hour) base input, cache read ~0.1×; it pays off only once the prefix is reused enough to amortize the write — verify via `usage.cache_read_input_tokens`.

## Relevant To

- Elective 03 — Cost & Latency Engineering (the prompt-caching lever, M1).
- Related: anthropic-pricing.md (the base per-MTok prices the multipliers apply to). Minimums and exact multipliers are model-specific — read the live doc, don't hardcode.

## Known issues / cautions

- Cache writes cost more than uncached input — a prefix reused only once is a net loss.
- Invalidation cascades: changing tools invalidates tools+system+messages; changing the system
  prompt invalidates system+messages. A prefix that changes per request never caches.
- Thresholds and exact multipliers are model/platform-specific and change — read the live doc;
  don't bake a number into code as if permanent.
