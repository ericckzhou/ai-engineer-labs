# LiteLLM — completion() Unified Interface

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** BerriAI (LiteLLM)
**Date:** Accessed 2026-06-01
**URL:** https://docs.litellm.ai/docs/completion/input
**Accessed:** 2026-06-01

## Why This Source Matters

LiteLLM is the lab's provider-abstraction layer. It lets the same application code call OpenAI, Anthropic, and 20+ other providers by changing only the `model` string. This source establishes the unified function signature and the "switch providers without changing logic" property that Learning Objective 7 of Project 1 depends on.

## Key Claims

### Unified interface
- `litellm.completion()` accepts **OpenAI Chat Completion params** and translates them to each provider's native API. Write once, switch providers by changing the model identifier.

### Function signature (key params)
```python
def completion(
    model: str,
    messages: List = [],
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    stream: Optional[bool] = None,
    stop=None,
    max_tokens: Optional[int] = None,
    response_format: Optional[dict] = None,
    seed: Optional[int] = None,
    tools: Optional[List] = None,
    tool_choice: Optional[str] = None,
    **kwargs,
) -> ModelResponse:
```

### Message shape (OpenAI style)
- `messages` is a list of `{"role": ..., "content": ...}`.
- Unlike the raw Anthropic API, the **system prompt is a message** with `{"role": "system", "content": ...}` (LiteLLM maps it to Anthropic's top-level `system` field internally).

### Provider switching
```python
import litellm

# OpenAI
litellm.completion(model="gpt-4o", messages=[{"role":"user","content":"Hello!"}], max_tokens=10)

# Anthropic — only the model string changes
litellm.completion(model="claude-sonnet-4-6", messages=[{"role":"user","content":"Hello!"}], max_tokens=10)
```

### Response shape
- Returns a `ModelResponse` normalized to the OpenAI shape: text at `response.choices[0].message.content`, token counts at `response.usage` (`prompt_tokens`, `completion_tokens`, `total_tokens`).
- Streaming (`stream=True`) yields chunks; text at `chunk.choices[0].delta.content`.

## Relevant To

- concepts: [provider-abstraction, litellm, model-string, openai-message-format]
- projects: [01-ai-chatbot]

## Notes

- The abstraction is leaky in useful ways: provider-specific features pass through `**kwargs`. The learner should understand what LiteLLM normalizes (message shape, usage fields) vs. what it passes through.
- `litellm.completion_cost(response)` can compute cost directly, but Project 1 has the learner compute it by hand first (from `usage` + `anthropic-pricing.md`) to build the mental model before using the helper.
