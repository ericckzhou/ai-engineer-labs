# Resources — Elective 06: Structured Output & Reliability

> Source-backed reading. Tiered by epistemic authority (`catalogs/source-map.md`). Truth lives in
> `sources/`; this is the reading list for the elective.

## Primary (read before coding)

- **Tier 1 — `sources/official-docs/anthropic-tool-use.md`** — Tools as structured output: a tool is a
  name + description + **JSON-schema input**; the model returns `stop_reason: "tool_use"` with
  arguments matching the schema; `tool_choice` (auto/any/tool/none) can **force** a single tool, i.e.
  force schema-shaped output. The provider-native alternative to "please return JSON."
- **Tier 2 — `sources/papers/outlines-guided-generation.md`** — Willard & Louf 2023, *Efficient Guided
  Generation for Large Language Models*. Reframes structured generation as transitions over a
  finite-state machine built from a regex/grammar/JSON-schema: at each step only tokens that keep the
  output schema-valid can be sampled, so invalid output is **impossible by construction**, at near-zero
  overhead. The basis for the constrained-decoding extension.

## Supporting

- **Tier 1 — `sources/official-docs/mcp-tools.md`** — `inputSchema` and optional `outputSchema`,
  structured tool results, and protocol-vs-execution errors: the same "declare the shape, validate
  against it, separate kinds of failure" contract at the protocol layer.
- **Tier 1 — `sources/official-docs/anthropic-messages-api.md`** — stop reasons and the response
  envelope you parse (carried from P01): where `max_tokens` truncation produces an *incomplete* object
  that validation must catch.

## Connects to

- **Project 06 (Tool Use)** — the place this skill is first needed: tool arguments are structured output
  you must trust.
- **Project 07 (Evaluation)** — an LLM judge returns a verdict you parse; an unvalidated verdict
  corrupts the score.
- **Elective 02 (Guardrails)** — a validated object is a smaller, more predictable attack surface than
  free text.
- **Elective 03 (Cost & Latency)** — every repair attempt is a generation; constrained decoding trades
  repair cost for decode constraints.
- **Elective 04 (Observability)** — emit the per-route repair rate as telemetry; a rising repair rate is
  drift.

## Reflection prompts
See `source/reflection.template.md` (copied into the project root as `UNDERSTANDING.md`).
