# Lesson (Agent Version): Cost & Latency Engineering — Making a Working Feature Cheap

> **Canonical source of truth.** The human version (`rendered/lesson.html`) is derived from this
> file. If they conflict, this file wins.
> **Elective — Production & Hardening track.** Off the numbered 1–9 spine; recommended after P09.
> Prerequisite skills: Projects 01, 02, 07.

---

## Metadata

- **Project:** Elective 03 — Cost & Latency Engineering
- **Track:** Production & Hardening (off-spine; after the P09 capstone)
- **Estimated time:** 8–12 hours
- **Prerequisites:** Project 07 (the eval + judge used as the no-regression **gate**), Project 01
  (the feature being optimized), Project 02 (embeddings — the semantic cache is a similarity lookup).
- **Optimized capability:** the Project 01 chatbot / Project 08 agent.
- **Primary sources:**
  - `sources/official-docs/anthropic-prompt-caching.md` (cache a stable prefix; cost mechanics)
  - `sources/official-docs/gptcache-semantic-caching.md` (embedding-similarity cache; the false hit)
  - `sources/papers/frugalgpt.md` (Chen/Zaharia/Zou 2023 — the model cascade)
  - `sources/official-docs/anthropic-pricing.md` (the real per-MTok base prices)

---

## Learning Objectives

By the end of this elective, the learner will be able to:

1. **Separate cost from quality as independent axes** — and explain why you can only optimize cost
   *safely* once you have an eval that proves quality didn't drop (why this follows Project 07).
2. **Apply prompt caching** — identify the stable prefix, place the breakpoint before variable
   content, and explain the cache-write-costs-more / cache-read-costs-less tradeoff.
3. **Build a semantic cache** — embed → nearest-neighbor → threshold gate → store; and explain the
   **false hit** (a too-loose threshold returns a stored answer for a different question).
4. **Build a model cascade** — answer with a cheap model, define a confidence/escalation signal,
   and escalate to a stronger model only when the cheap answer isn't trusted (FrugalGPT).
5. **Account for cost honestly** — accumulate real per-call cost from the published price table
   (no invented prices) and enforce a budget ceiling.
6. **Prove the optimization** — run the frozen eval and report that **quality held while cost/
   latency dropped**; report the frontier, not a one-sided "10× cheaper".

---

## 1. Motivation

### Why this exists

Your Project 01 chatbot and Project 08 agent are *correct*. They are also, in production, **slow
and expensive**: every turn hits your biggest model, re-sends the same long system prompt, and
re-answers questions you've already answered for someone else. At one user, you don't notice. At
ten thousand, the bill and the latency are the product.

The instinct is to "just use a cheaper model." But that can quietly break correctness — and how
would you know? You wouldn't, *unless you had an eval.* You built one in Project 07. That is the
key that unlocks this whole elective: **with a frozen eval and a judge, you can change the
engine — cache, downgrade, cascade — and prove the answers are no worse before you ship the
savings.** Cost optimization without an eval is just gambling with quality.

### What breaks without it

Without these levers: you pay 1× for every token of a system prompt that never changes; you pay
full price to re-answer "what is X" for the thousandth time; and you send trivial queries to a
model built for hard ones. Without the *eval*, the obvious fixes are landmines — a cheaper model
or a loose cache silently regresses quality and you find out from users, not tests.

> **Startup lens (StarcallOS).** A personal OS runs constantly in the background — summarizing,
> classifying, routing. Most of that is repetitive and easy; a fraction is hard. Paying top-model
> prices for all of it is how a useful product becomes an unaffordable one. Caching + cascading
> is the difference between a demo and a thing you can actually leave running.

---

## 2. ELI12

Imagine you run a help desk. Three habits save you a fortune without giving worse help:

1. **Keep the rulebook open on the desk** instead of re-reading it from the vault every single
   time a question comes in. The rulebook never changes — read it once, keep it handy. That's
   **prompt caching**: the unchanging part of the prompt is kept "open" so you don't pay to
   re-read it.
2. **Remember answers to questions you've already been asked.** If someone asks "how do I reset my
   password" and you answered that an hour ago — even phrased slightly differently — you just
   repeat your answer instead of researching it again. That's a **semantic cache**: it matches on
   *meaning*, not exact words. (Danger: if you're too loose about "that's basically the same
   question," you'll give the password answer to someone asking about billing.)
3. **Send easy questions to the junior, hard ones to the expert.** Most questions are easy; the
   junior handles them fine and cheap. Only when the junior isn't sure do you escalate to the
   expensive expert. That's a **cascade**.

And the golden rule: before you trust the junior or your memory, **check against the answer key**
(your eval) — cheaper help is only good if it's still *right*.

---

## 3. Cost and Quality Are Separate Axes

A change can move cost, quality, or both. The trap is optimizing cost and *assuming* quality held.
"We made it 10× cheaper" is not a result — it's half of one. The other half is "and the eval
pass-rate is unchanged." A cheaper config that drops pass-rate from 92% to 78% is a **regression**
wearing a cost-savings costume.

So every lever in this elective is measured the same way: run Project 07's **frozen eval set**
through the optimized pipeline and the baseline, and compare **two** numbers — quality (judge
pass-rate) and cost (and latency). Ship the change only if quality is within tolerance. The eval
is the gate; the levers are negotiable; correctness is not.

---

## 4. Prompt Caching — Free Savings on a Stable Prefix

Most of your prompt doesn't change between calls: the system prompt, the tool definitions, a long
document. Prompt caching stores that **stable prefix** so you pay full input price for it **once**
and ~1/10th on every reuse (`anthropic-prompt-caching.md`).

Two facts make this an *engineering* decision, not a free button:

- A cache **write** costs *more* than a normal call (~1.25×). The saving is in the **reads** (~0.1×).
  So caching pays off only when the prefix is reused enough to amortize the write.
- The cached prefix must be **identical and come before the variable content.** Put the breakpoint
  after something that changes every request (a timestamp, the user's message) and you cache
  nothing. Stable first → breakpoint → variable last.

This is the purest lever: **same model, same output, lower input cost** — zero quality risk. The
learner proves it by reading `cache_read_input_tokens` from the response usage.

---

## 5. Semantic Caching — Don't Re-Answer the Same Question

Exact-match caching only helps if the *string* repeats. A **semantic cache** helps when the
*meaning* repeats: "how do I reset my password" and "I forgot my password, what now?" should hit
the same stored answer (`gptcache-semantic-caching.md`). The design reuses what you already built:

- **embed** the query (Project 02 — same embedder for store and lookup),
- **nearest-neighbor** search over stored queries (Project 03's ANN),
- a **similarity threshold**: above ⇒ return the cached answer (hit); below ⇒ miss → call the
  model → store.

The lesson's failure mode is the **false hit**: set the threshold too loose and the cache returns
a stored answer for a *different* question — a confident, cached, wrong answer. So the threshold is
a precision/recall dial (echoing Elective 02's guard), and **hit-rate alone is a vanity metric** —
the real one is correctness *under* hits, which only the eval reveals.

---

## 6. Model Cascade — Cheap First, Escalate on Doubt

You don't need your best model for "what's 2+2." FrugalGPT's **cascade** (`frugalgpt.md`) answers
with a **cheap model first**, then **escalates** to a stronger one only when the cheap answer
isn't trusted:

```
query ─▶ cheap model ─▶ [confident?] ──yes──▶ accept (cheap)
                              │ no
                              ▼
                         strong model ─▶ accept (strong)
```

The hard part — the whole design decision — is the **escalation signal**: *how do you know the
cheap model wasn't sure?* Options: a self-reported confidence, a logprob, a cheap self-check, or a
judge. There is no free correct answer; the learner picks a signal and the eval shows whether it
escalated the *right* queries. Unlike caching, a cascade carries **quality risk** (a wrong cheap
answer ships), which is again why the eval gate is mandatory.

---

## 7. Budget Accounting

Optimizing cost requires *measuring* cost. Reusing Project 08's budget pattern, a `CostTracker`
accumulates the real per-call cost — tier price × tokens, from the **published price table**
(`anthropic-pricing.md`; do **not** invent prices) — and enforces a ceiling. A cache hit costs ~0;
a cheap-tier call costs little; an escalation costs the strong-tier price. The tracker turns "feels
cheaper" into a number you can put next to the quality number.

---

## 8. Measuring the Optimization — Report the Frontier

The deliverable is a **frontier**, not a slogan. Run the frozen eval through:

- **baseline** (always the strong model, no cache), and
- **optimized** (cache + cascade),

and report, for each: **quality** (judge pass-rate), **cost** (total $), **latency** (or calls),
and **cache-hit rate**. A good result is "quality 92% → 91% (within tolerance), cost −74%,
latency −40%." A loud cost win next to a quiet quality drop is the metric trap this project exists
to teach you to refuse.

---

## Milestones

1. **M1 — Prompt caching:** mark the stable prefix; measure cache-read savings on repeat calls.
2. **M2 — Semantic cache:** embed → nearest → threshold gate → store; tune the threshold and show
   a false hit at a loose setting.
3. **M3 — Model cascade:** cheap-first; define the escalation signal; escalate only on low
   confidence.
4. **M4 — Budget:** accumulate real per-call cost; enforce a ceiling.
5. **M5 — Prove it:** run the frozen eval baseline vs optimized; quality holds while cost/latency
   drop; report the frontier.
6. **Extension:** batch API for offline workloads; per-route tiering; cache invalidation strategy.

---

## Common Misconceptions

- **"Caching is a free button."** A cache *write* costs more than a normal call; it only pays off on
  reuse. Caching a variable prefix saves nothing.
- **"High cache-hit rate = good cache."** Not if the hits are wrong. A loose semantic threshold
  serves a stored answer to a different question. Measure correctness under hits.
- **"Just use the cheap model."** That's a cascade with the escalation removed — it ships the cheap
  model's wrong answers. The signal is the point.
- **"10× cheaper" is the result.** Half of one. Without "and quality held on the eval," it's a
  possible regression.
- **"I'll estimate the prices."** Use the real per-MTok table. Invented prices invalidate the whole
  cost claim.

---

## Instructor Notes

- The **non-negotiable assessable idea** is *cost and quality are separate axes, and the eval is the
  gate*. If `EVALUATION.md` reports a cost win without the paired quality number, it's incomplete.
- The **second** is the *semantic false hit*: the learner must demonstrate a wrong answer from a
  too-loose threshold, not just a hit-rate.
- The **third** is the *escalation signal*: a cascade that never escalates (or always does) misses
  the design decision.
- Keep it offline/deterministic: a provided cheap/strong "model" pair + a deterministic embedder +
  a cost model make the whole thing gradeable without a provider; real caching/latency numbers are
  the live extension.
- Don't accept invented prices. The cost number must trace to `anthropic-pricing.md`.

---

## Sources

- `sources/official-docs/anthropic-prompt-caching.md` — stable-prefix caching; write ~1.25× / read
  ~0.1× / base 1×; 5-min/1-hour TTL; stable-before-variable; verify via usage.
- `sources/official-docs/gptcache-semantic-caching.md` — embedding-similarity cache; embed → ANN →
  threshold = hit; the false hit from a loose threshold; eviction.
- `sources/papers/frugalgpt.md` — Chen/Zaharia/Zou 2023: prompt adaptation / approximation /
  cascade; cheap-first, escalate on low reliability score; up to ~98% cost cut.
- `sources/official-docs/anthropic-pricing.md` — the real per-MTok base prices the multipliers and
  savings are computed against.
