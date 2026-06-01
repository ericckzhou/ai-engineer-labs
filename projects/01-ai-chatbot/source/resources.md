# Resources & Sources

> All sources used for this lesson, organized by tier.
> Every claim in lesson.agent.md traces back to one of these.
> Local copies live in `sources/` — those are the truth layer; the URLs below are provenance.

---

## Tier 1: Official Documentation

> Primary sources. Check these first.

- **Anthropic Messages API Reference** — `sources/official-docs/anthropic-messages-api.md`
  - URL: https://platform.claude.com/docs/en/api/messages
  - What to read: request/response contract, the `messages` array, `system`, `stop_reason`, `usage`.
  - Key sections: required request fields; stateless multi-turn model; stop reasons; token usage.
  - Anchors objectives: 1, 2, 3, 6 (and the statelessness mental model).

- **Anthropic Messages API — Streaming** — `sources/official-docs/anthropic-streaming.md`
  - URL: https://platform.claude.com/docs/en/docs/build-with-claude/streaming
  - What to read: how to enable `stream: true` and the SSE event order.
  - Key sections: event flow (`message_start` → `content_block_delta`* → `message_stop`); where final `usage` arrives.
  - Anchors objective: 4. Source of difficulty spike #1 (streaming + usage).

- **Anthropic Pricing & Token Cost** — `sources/official-docs/anthropic-pricing.md`
  - URL: https://platform.claude.com/docs/en/docs/about-claude/pricing
  - What to read: per-MTok pricing, the cost formula, the ~4 chars/token rule, prompt caching.
  - Key sections: token estimation; input vs output pricing; cache/batch discounts.
  - Anchors objective: 5. Basis for `cost_tracker.py` and the quadratic-cost math.

- **LiteLLM — completion() Unified Interface** — `sources/official-docs/litellm-completion.md`
  - URL: https://docs.litellm.ai/docs/completion/input
  - What to read: the unified function signature; "switch providers by changing the model string."
  - Key sections: OpenAI-shaped params; system message at index 0 of `messages`.
  - Anchors objective: 7. Basis for the provider-abstraction extended requirement.

---

## Tier 2: Foundational Papers

> None required for Project 1. The chat-completions abstraction is an engineering contract, not a research result; the underlying Transformer paper is deferred to Project 2 (Tokens & Embeddings), where it becomes load-bearing.

- _Deferred to P2:_ Vaswani et al., "Attention Is All You Need" (2017).

---

## Tier 3: Engineering Blogs

> None gathered for Project 1. Production patterns (sliding window, summarization, prompt caching) are covered by the Tier 1 pricing/Messages docs above; dedicated engineering write-ups are deferred until a specific production claim needs one.

---

## Tier 4: Educational Sources

> Tutorials and courses useful for framing. Explanatory, not authoritative.

- **Hugging Face LLM Course — Introduction** — `sources/videos/hf-llm-course-intro.md`
  - URL: https://huggingface.co/learn/llm-course/chapter1/1
  - Best for: the NLP-vs-LLM framing used in the ELI-Engineer section (§2).

- **mlabonne/llm-course — LLM Engineer Track** — `sources/articles/mlabonne-llm-course.md`
  - URL: https://github.com/mlabonne/llm-course
  - Best for: validating curriculum order — "Running LLMs" as the foundational first step (§1, §10).

---

## Recommended Reading Order

For a learner new to this topic:

1. Start with: **mlabonne — "Running LLMs"** (where this project sits in the path).
2. Then read: **Anthropic Messages API** §request/response and stateless multi-turn (the core contract).
3. Then read: **Anthropic Pricing** (so cost is in mind *before* you build the loop).
4. For depth: **Anthropic Streaming**, then **LiteLLM** (delivery and provider abstraction).

---

## Further Reading

Topics adjacent to this lesson worth exploring later:

- **Prompt caching** — caching the stable history prefix to cut repeated-input cost ~10× (Anthropic pricing doc) → motivates P5 Memory.
- **Tokenization internals** — why `~4 chars/token` is only an estimate (note: Opus 4.7+ tokenizer differs) → P2.
- **Tool use / function calling** — `stop_reason == "tool_use"` turns this REPL into an agent loop → P8.
