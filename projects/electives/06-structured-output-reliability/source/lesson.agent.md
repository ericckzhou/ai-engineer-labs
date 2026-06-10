# Lesson (Agent Version): Structured Output & Reliability — Making a Model's Text Trustworthy Data

> **Canonical source of truth.** The human version (`rendered/lesson.html`) is derived from this
> file. If they conflict, this file wins.
> **Elective — Production & Hardening track.** Off the numbered 1–9 spine; strongly recommended
> **after P06 (tool use), before P08 (agent)**. Prerequisite skills: Project 01, Project 06.

---

## Metadata

- **Project:** Elective 06 — Structured Output & Reliability
- **Track:** Production & Hardening (off-spine) — a *reliability* elective the other projects depend on
- **Estimated time:** 7–11 hours
- **Prerequisites:** Project 06 (tool use — tools ARE structured output), Project 01 (model calls).
- **Hardens:** every project that parses a model's output — P06 tool arguments, P07 eval verdicts,
  P08 agent actions, P09 routing.
- **Primary sources:**
  - `sources/official-docs/anthropic-tool-use.md` (tools as structured output; JSON-schema input; `tool_choice` to force structure)
  - `sources/papers/outlines-guided-generation.md` (Willard & Louf 2023 — constrain the decoder so output is valid by construction)

---

## Learning Objectives

By the end of this elective, the learner will be able to:

1. **Name the three failure modes of "just parse the model output"** — format noise (fences/prose),
   syntax errors, and the sneaky one: syntactically-valid JSON that **violates the schema**.
2. **Separate extraction from validation** — extraction fixes *format*; validation catches *contract*
   violations. Conflating them is why "it worked on my example" breaks in production.
3. **Build a validate → repair → retry loop** that feeds the *specific* validation errors back to the
   model, with a **bounded attempt budget**, and **fails closed** (never returns an unvalidated object).
4. **Measure reliability as a number** — success rate per failure kind, and the repair *cost* (extra
   generations) — so a reliability claim is evidence, not a vibe.
5. **Explain constrained decoding** — that the most robust fix prevents invalid output *at generation*
   (guided decoding / a forced tool schema) instead of repairing it after, and the tradeoffs.

---

## 1. Motivation

### Why this exists

Every project after Project 06 quietly assumes the model returns **usable structured data**: P06 reads
tool arguments, P07 parses an LLM judge's verdict, P08 decides the next action from a JSON blob, P09
routes on a classification. None of them taught how to *guarantee* that data. They assumed
`json.loads(response)` works.

It doesn't — reliably. A model is a text generator, not a serializer. Ask it for JSON and a meaningful
fraction of the time you get JSON wrapped in a ```json fence, or with a "Sure! Here you go:" preamble,
or with a trailing "Hope that helps!", or — worst — perfectly-valid JSON whose `priority` is `"high"`
instead of `4`, or that's missing `needs_human` entirely. The first three are *format* problems. The
last is a *contract* problem, and it's the dangerous one: it **parses**, so your code happily proceeds
with a wrong object.

This elective makes the model→object boundary a thing you **engineer**: extract, validate against a
schema, and on failure send the model its own errors and ask it to fix them — within a budget, failing
closed when it can't. Then you **measure** the lift.

### What breaks without it

Without this layer, your reliability ceiling is "the model happened to format it right." One stray
fence crashes a tool call; one out-of-range enum silently mis-routes a request; one missing field
throws three calls deep with a `KeyError` and no idea which model response caused it. And the trap on
the *other* side: blindly retrying on failure with no error feedback (the model repeats the same
mistake) or, worse, "fixing" the parse by accepting whatever came back — returning an object you never
validated. Reliability is the loop **plus** the discipline to fail closed.

> **Startup lens (StarcallOS).** A personal OS chains models: classify an input, pick a tool, fill its
> arguments, judge the result. Each hop hands structured data to the next. One unreliable hop poisons
> the chain — a mis-parsed action runs the wrong tool on your real files. The coerce loop is the
> shock-absorber between a probabilistic generator and deterministic code that *acts*.

---

## 2. ELI12

You ask a brilliant but rambling friend to write you a shopping list as a neat table. Sometimes you get
the table. Sometimes you get "Sure! Here's your list:" and *then* the table. Sometimes the table is
wrapped in decorative borders. And sometimes it looks perfect but they wrote "a bunch" in the quantity
column instead of a number.

A careless person grabs whatever and goes shopping — and comes home with "a bunch" of milk. A careful
person does two different things:

1. **Unwraps** the table from the chatter and borders. (That's *extraction* — a format problem.)
2. **Checks the table follows the rules**: every row has a number in the quantity column, every item is
   one you actually buy. (That's *validation* — a contract problem.)

And if a rule is broken, the careful person doesn't guess — they hand it back: "quantity must be a
number; you wrote 'a bunch' for milk — fix just that." Usually the friend fixes it. If after a couple
tries it's still broken, the careful person **stops** rather than shop on bad data. Unwrap, check,
hand-back-with-the-specific-error, and know when to stop — that's the whole elective.

---

## 3. The Three Failure Modes of "Just Parse It"

`json.loads(model_output)` fails three structurally different ways. Naming them is half the battle,
because each has a *different* fix:

- **Format noise.** Valid JSON wrapped in ```json fences or buried in prose ("Here you go: {…}. Hope
  that helps!"). Fix: **extraction** — strip the wrapper, find the object. Cheap, deterministic, no
  model needed.
- **Syntax errors.** Single quotes, trailing commas, unquoted keys — not valid JSON. Sometimes
  recoverable by a tolerant parser; often needs a **repair** round.
- **Schema violations.** The output parses fine but breaks your *contract*: wrong type
  (`"priority": "high"`), out-of-range, bad enum, missing required field. This is the dangerous one
  because **parsing succeeds** — your program proceeds with a wrong object. Fix: **validation** then
  **repair**.

The mistake nearly everyone makes is treating all three as "the JSON was bad" and throwing a bigger
regex at it. Extraction will never fix a schema violation; validation will never fix a fence. Keep them
separate.

---

## 4. Extraction — Fix the Format, Nothing Else

`extract_json(text)` strips code fences, ignores surrounding prose, and pulls out the first **balanced**
`{…}` object. Scan from the first `{`, track brace depth (respecting strings), stop at the matching `}`.

That's *all* it does. It does not validate, coerce types, or fill defaults. Keeping extraction narrow is
what lets you reason about reliability: after extraction you either have a JSON object or you don't, and
the next stage decides whether that object is *acceptable*. A 'clean' or 'fenced' output is usable after
extraction with **zero** model calls — the cheapest possible fix, and you should always try it first.

---

## 5. Validation — Enforce the Contract, Return the Errors

`validate(obj, schema)` walks the schema and returns a **list of human-readable errors** ( `[]` means
valid): required-but-missing, wrong type, out-of-enum, out-of-range. Two things make this more than an
`if`-soup:

- **Return the errors, don't just say "invalid."** `coerce` feeds these exact strings back to the model
  ("priority: 9 exceeds max 5") so it can fix *that specific thing*. Error specificity is what makes
  repair converge instead of flailing.
- **The `bool`/`int` trap.** In Python `bool` is a subclass of `int`, so `isinstance(True, int)` is
  `True`. A model that returns `"priority": true` would sail through a naive int check. Check `bool`
  fields *before* int fields, and reject a bool where an int is required. This is exactly the kind of
  silent-wrong-object bug the whole elective exists to stop.

Validation is the gate. Nothing reaches your downstream code without passing it.

---

## 6. The Repair Loop — Hand Back the Errors, With a Budget, Fail Closed

`coerce(message)` is the core:

```
prompt = task(message)
for attempt in range(max_attempts):
    raw = backend.generate(prompt)
    obj = extract_json(raw)          # format
    errors = validate(obj)           # contract
    if not errors: return obj        # success
    if no budget left or repair disabled: break
    prompt = build_repair_prompt(message, raw, errors)   # hand back the SPECIFIC errors
raise StructuredOutputError(...)     # FAIL CLOSED — never return an unvalidated object
```

Three non-negotiables:

- **Repair with the errors, not a blind retry.** "Try again" makes the model repeat its mistake.
  "Your `priority` was 9; the max is 5 — return only valid JSON" fixes it. The repair prompt carries the
  validation errors.
- **A bounded budget.** Each attempt costs a generation (latency + tokens). Cap it (`max_attempts`).
  Unbounded "keep trying until valid" is how a flaky model turns one request into a runaway bill.
- **Fail closed.** When the budget is exhausted, **raise** — do not return the least-bad object. A
  caller that gets an exception can fall back safely; a caller handed an unvalidated object acts on
  garbage. The whole point of the layer is that *what comes out is valid, or nothing does.*

---

## 7. Measure It — Reliability Is a Number (M5)

"It seems more reliable now" is not engineering. `evaluate.py` runs a frozen set across the failure
kinds and reports, **per kind**, the naive baseline (raw output that parses *and* validates) vs the
robust loop, plus the repair cost. Expected honest findings:

- **clean** ~100% either way (the loop costs nothing here).
- **fenced / prose** 0% naive → ~100% robust, fixed by extraction alone (no repair).
- **schema** 0% naive → ~100% robust, but **only via a repair round** — and naive "parse success" is a
  lie here: it parsed and was still wrong.
- **unfixable** 0% and **stays 0%** under the robust loop — failing closed is *correct*, not a bug; a
  layer that "succeeds" on garbage is broken.

The gap between the columns is the value you added; the repair attempts are the price (this is where
this elective hands off to **Elective 03 — Cost & Latency**: every repair is a generation).

---

## 8. Constrained Decoding — Prevent the Error Instead of Repairing It (Extension)

Repair fixes invalid output *after* the fact. The more robust move prevents it *at generation*:

- **Forced tool schema.** `anthropic-tool-use.md`: a tool is a name + description + **JSON-schema**
  input, and `tool_choice` can **force** the model to emit exactly one tool's arguments. Asking for a
  tool call rather than "please return JSON" gives you schema-shaped output from the provider — fewer
  repairs.
- **Guided decoding.** `outlines-guided-generation.md` (Willard & Louf 2023) reframes structured
  generation as walking a **finite-state machine** built from a regex/grammar/JSON-schema: at each step
  the decoder is only allowed to sample tokens that keep the output matching the schema, so invalid
  output is **impossible by construction**, at near-zero overhead.

The tradeoff: constrained decoding needs provider/library support and can over-constrain (the model
can't express "I don't know" if the grammar forbids it). The mature design often uses *both*: constrain
where you can, and keep the validate-repair loop as the backstop for everything else. The lesson the
eval teaches still holds — measure whether constraining actually cut the repair rate.

---

## Milestones

1. **M1 — `parse_strict`:** strict `json.loads`; establishes the baseline failure rate.
2. **M2 — `extract_json`:** strip fences/prose, pull the first balanced object (format noise).
3. **M3 — `validate`:** schema errors as a list; handle the `bool`/`int` trap.
4. **M4 — `build_repair_prompt` + `coerce`:** the validate→repair→retry loop, bounded, fail closed.
5. **M5 — measure:** run `evaluate.py`; report success per failure kind and the repair cost, honestly.
6. **Extension:** swap the fake backend for a live model; force a tool schema (`tool_choice`) and/or
   guided decoding; compare repair rate.

---

## Common Misconceptions

- **"`json.loads` is enough."** It handles neither format noise nor schema violations — and on a schema
  violation it *succeeds*, handing you a wrong object.
- **"Extraction and validation are the same step."** Extraction fixes format; validation enforces the
  contract. A bigger regex never fixes a missing field.
- **"If it parsed, it's valid."** The most dangerous output is valid JSON that breaks your schema.
- **"Just retry until it works."** Blind retry repeats the mistake and is unbounded cost. Repair with
  the *specific* errors, and cap attempts.
- **"Return the best object we got."** Never return an unvalidated object. Fail closed.
- **"`isinstance(priority, int)` checks the type."** `True` passes it — `bool` is an `int`. Check bool
  first.
- **"Reliability is a feeling."** It's a number: success rate per failure kind, and the repair cost.

---

## Instructor Notes

- The **non-negotiable assessable idea** is **fail closed**: `coerce` must raise (never return an
  unvalidated object) when the budget is exhausted. A learner who returns the least-bad object has
  inverted the entire point.
- The **second** is **separation**: extraction (format) vs validation (contract) are distinct stages.
  Watch for learners who try to validate inside `extract_json` or repair inside `validate`.
- The **third** is **repair-with-errors**: the repair prompt must carry the specific validation errors,
  and `EVALUATION.md` must report success **per failure kind** plus the repair cost — including that
  the unfixable case correctly stays failed.
- Keep it offline/deterministic: a provided `fake_backend` emits the five failure shapes and converges
  on a repair attempt for fixable cases, so the whole loop is gradeable without a provider. Live model +
  constrained decoding is the extension.
- The `bool`/`int` trap is a deliberate teaching moment — most learners miss it until a test catches it.

---

## Sources

- `sources/official-docs/anthropic-tool-use.md` — tool = name + description + JSON-schema input;
  `stop_reason: "tool_use"`; `tool_choice` (auto/any/tool/none) to **force** structured output; tools as
  the provider-native structured-output mechanism.
- `sources/papers/outlines-guided-generation.md` — Willard & Louf 2023: guided generation as FSM
  transitions over the vocabulary; only schema-preserving tokens are sampled, making invalid output
  impossible by construction at near-zero overhead (the constrained-decoding extension).
- `sources/official-docs/mcp-tools.md` — `inputSchema`/optional `outputSchema` and structured tool
  results: the same "declare the shape, validate against it" contract at the protocol layer.
