# Anthropic — Tool Use (Function Calling) Overview

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** Anthropic
**Date:** Accessed 2026-06-01
**URL:** https://platform.claude.com/docs/en/docs/build-with-claude/tool-use/overview
**Accessed:** 2026-06-01

## Why This Source Matters

This is the primary source for **tool use** — the central learning target of Project 06. Tool use is how an LLM stops being a text-in/text-out function and starts *acting*: reading a file, searching a codebase, calling an API. The mechanism is a structured request/response protocol — the model emits a structured **call**, your code executes it, you feed the **result** back, and the model continues. That request→execute→feed-back cycle, run in a loop, is the spine of every coding copilot and every agent (Project 08). The lab calls tools through LiteLLM's OpenAI-style interface (`tools` / `tool_calls`), but the conceptual flow below — defined by Anthropic's native API — is identical across providers.

## Key Claims

### Tools are defined by name, description, and an input schema
- A tool definition has a **`name`**, a **`description`**, and an **`input_schema`** (a JSON Schema describing the parameters). "Claude decides when to call a tool based on the user's request and the tool's description."
- The description is load-bearing: the model chooses tools *from the description alone*. Good definitions include "example usage, edge cases, input format requirements, and clear boundaries."

### The request/response flow (client tools)
- **Client tools** "run in your application." The cycle:
  1. You send `messages` plus a `tools` list to the model.
  2. If the model decides to use a tool, it responds with **`stop_reason: "tool_use"`** and one or more **`tool_use`** content blocks. Each `tool_use` block has an `id`, a `name`, and an `input` object (the arguments, matching your schema). Example:
     ```json
     { "type": "tool_use", "id": "toolu_01A09q...", "name": "get_weather",
       "input": { "location": "New York, NY", "unit": "fahrenheit" } }
     ```
  3. **Your code executes the operation** and sends the outcome back as a **`tool_result`** content block (a `user`-role message) carrying the matching `tool_use_id` and the result content.
  4. The model reads the result and either calls another tool or returns a final answer with `stop_reason: "end_turn"`.

### The agentic loop
- The model may call tools **multiple times** before producing a final answer: read a file → decide it needs another → search → then answer. The application loops "send → if `tool_use`, execute + return `tool_result` → repeat" until the model stops requesting tools (`stop_reason` is no longer `"tool_use"`). **The loop is the program; the model drives it.**
- "Tool access is one of the highest-leverage primitives you can give an agent." On benchmarks like SWE-bench, "adding even basic tools produces outsized capability gains."

### Controlling whether the model calls a tool — `tool_choice`
- Default is **`tool_choice: {"type": "auto"}`**: "Claude decides on each turn whether to call a tool or respond directly." It calls a tool "when the request maps to that tool's described capability and the answer isn't already in context."
- For a hard guarantee, `tool_choice` can force tool use (`any` = must use some tool; `tool` = must use a specific named tool; `none` = no tools). Auto behavior is also steerable via the system prompt ("Use the tools to investigate before responding").

### Tools as structured output
- Because a `tool_use` block is a schema-conforming object, tool use **is** the mechanism for structured output: define a tool whose `input_schema` is the shape you want, and the model fills it. `strict: true` "ensures Claude's tool calls always match your schema exactly."

### Missing parameters
- If the prompt lacks enough information to fill a required parameter, more capable models "recognize that a parameter is missing and ask for it," while others "may do its best to infer a reasonable value." Required-parameter design matters.

## Relevant To

- concepts: [tool-use, function-calling, tool-schema, agentic-loop, tool-result, structured-output, tool-choice, react]
- projects: [06-ai-coding-copilot, 08-ai-agent]

## Notes

- **The lab calls tools via LiteLLM (OpenAI-style), not the raw Anthropic API**, so it works across Groq/Ollama/Anthropic with one code path. The OpenAI mapping of the same concepts: a tool is `{"type":"function","function":{"name","description","parameters":<JSON Schema>}}`; the model's request arrives at `response.choices[0].message.tool_calls` (each has `id` and `function.name` + `function.arguments` as a **JSON string**); you append the assistant message, then one `{"role":"tool","tool_call_id":id,"content":result}` message per call; `tool_choice="auto"`. The loop ends when `message.tool_calls` is empty. (Source: `sources/official-docs/litellm-completion.md`.)
- **`arguments` is a JSON string in the OpenAI/LiteLLM shape** — you must `json.loads` it before dispatching. Forgetting this is a common first bug.
- **The description is the API.** The model never sees your function body — only `name` + `description` + schema. A vague description = the model picks the wrong tool or fills bad args. This is the "agent-computer interface" point from `sources/articles/building-effective-agents.md`.
- **The loop needs a cap.** A model can request tools indefinitely (or get stuck calling the same one). Always bound the loop (`max_steps`) — see `sources/papers/react-paper.md` for the reasoning-trace structure that makes loops terminate sensibly.
