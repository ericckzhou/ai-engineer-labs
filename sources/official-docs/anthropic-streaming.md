# Anthropic Messages API — Streaming

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** Anthropic
**Date:** Accessed 2026-06-01
**URL:** https://platform.claude.com/docs/en/docs/build-with-claude/streaming
**Accessed:** 2026-06-01

## Why This Source Matters

Defines how a response is delivered token-by-token instead of all at once. Streaming is what makes a chatbot feel responsive: the user sees text appear immediately rather than waiting for the full completion. This source gives the exact event protocol so the learner understands what is actually arriving over the wire, not just what the SDK abstracts away.

## Key Claims

### Enabling streaming
- Set `"stream": true` on a Messages request. The response is delivered as **server-sent events (SSE)**.
- Each SSE has a named event type (`event: message_stop`) and a JSON `data` payload whose `type` matches.

### Event flow (in order)
1. `message_start` — a `Message` object with empty `content`.
2. For each content block: a `content_block_start`, one or more `content_block_delta` events, then a `content_block_stop`. Each block has an `index` matching its position in the final `content` array.
3. One or more `message_delta` events — top-level changes to the final `Message` (e.g. `stop_reason`, final `usage`).
4. A final `message_stop`.
- `ping` events may be interleaved at any time; `error` events can also occur.

### Content block delta types
- A text delta:
  ```
  event: content_block_delta
  data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"ello frien"}}
  ```
- A tool-use delta uses `input_json_delta` with chunked `partial_json`.

### SDK usage (Python)
The official SDK abstracts the SSE parsing:
```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
    model="claude-opus-4-8",
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```
- `stream.text_stream` yields only the text deltas.
- `stream.get_final_message()` returns the complete accumulated `Message` (identical to `.create()`), useful when you also need final `usage`.
- For large `max_tokens`, the SDKs require streaming to avoid HTTP timeouts.

## Relevant To

- concepts: [streaming, server-sent-events, content-block-delta, token-by-token-generation]
- projects: [01-ai-chatbot]

## Notes

- Final token `usage` arrives in the `message_delta` / final message, not in the first event — so cost can only be finalized after the stream completes.
- LiteLLM exposes streaming via `stream=True`, yielding OpenAI-style chunks (`chunk.choices[0].delta.content`) rather than raw Anthropic events.
