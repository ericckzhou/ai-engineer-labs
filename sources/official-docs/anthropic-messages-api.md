# Anthropic Messages API Reference

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** Anthropic
**Date:** Accessed 2026-06-01 (API version `2023-06-01`)
**URL:** https://platform.claude.com/docs/en/api/messages (redirected from https://docs.anthropic.com/en/api/messages)
**Accessed:** 2026-06-01

## Why This Source Matters

This is the definitive specification for how an application talks to a Claude model. Every chatbot, RAG system, and agent built on Claude issues `POST /v1/messages` requests under the hood. It establishes the request/response contract, the stateless multi-turn model, and the token-accounting fields that drive cost. For Project 1, this is the primary truth layer.

## Key Claims

### Endpoint
- `POST /v1/messages` — single endpoint for all chat completions.
- Required header: `anthropic-version: 2023-06-01`, plus `x-api-key`.

### Request — required fields
- `model` (string) — e.g. `claude-opus-4-8`, `claude-sonnet-4-6`, `claude-haiku-4-5`.
- `max_tokens` (number) — maximum tokens to generate. **Must be set.** The model may stop earlier.
- `messages` (array) — ordered conversation turns. Each is `{"role": "user" | "assistant", "content": "..."}`. `content` may be a string or an array of content blocks.

### Request — common optional fields
- `system` (string | array) — the system prompt: persistent instructions applied to the whole conversation. It is a **top-level field, not a message** (Claude has no `system` role inside `messages`).
- `temperature` (number, 0.0–1.0, default 1.0) — randomness. Use 0.0 for analytical/deterministic tasks, higher for creative.
- `stop_sequences` (array) — custom strings that force the model to stop.
- `stream` (boolean) — enable server-sent-event streaming.
- `top_p`, `top_k` — alternative sampling controls.
- `tools`, `tool_choice` — function/tool calling.

### The stateless multi-turn model (CENTRAL CONCEPT for Project 1)
- The API is **stateless**. The model retains nothing between requests.
- "Memory" of a conversation is created by **resending the entire `messages` array** — all prior user and assistant turns — on every request.
- Models are trained on **alternating** `user` / `assistant` turns. Consecutive same-role messages are merged into one turn.
- If the final message has the `assistant` role, the model continues from that content (prefill).
- Limit: 100,000 messages per request.

### Response structure
```json
{
  "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message",
  "role": "assistant",
  "content": [{"type": "text", "text": "The capital of France is Paris."}],
  "model": "claude-opus-4-8",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 25,
    "output_tokens": 12,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0
  }
}
```

### Stop reasons
- `end_turn` — natural stopping point.
- `max_tokens` — hit the `max_tokens` limit (response may be truncated mid-thought).
- `stop_sequence` — a custom stop sequence triggered.
- `tool_use` — model invoked a tool.
- `refusal` — policy violation.
- `pause_turn` — long-running turn paused.

### Token accounting
- `usage.input_tokens` — tokens in the request (system prompt + entire message history).
- `usage.output_tokens` — tokens the model generated.
- Because the full history is resent each turn, `input_tokens` **grows with conversation length** — the core cost dynamic of any chatbot.

### Example request
```bash
curl https://api.anthropic.com/v1/messages \
  -H 'Content-Type: application/json' \
  -H 'anthropic-version: 2023-06-01' \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "system": "You are a helpful assistant.",
    "messages": [
      {"role": "user", "content": "What is the capital of France?"}
    ],
    "temperature": 0.7
  }'
```

## Relevant To

- concepts: [chat-completions-api, messages-array, system-prompt, multi-turn-conversation, context-window, temperature, stop-reason, token-usage]
- projects: [01-ai-chatbot]

## Notes

- The stateless multi-turn model is the single most important idea in Project 1; everything about cost and context management follows from "resend the whole history every time."
- Field names are Anthropic-specific. LiteLLM normalizes most of these to the OpenAI shape (see `litellm-completion.md`) — notably, LiteLLM puts the system prompt as a `{"role": "system"}` message, whereas the raw Anthropic API uses a top-level `system` field.
