# Lesson 01: AI Chatbot
<!-- lesson.agent.md — Agent-optimized canonical source. Do not simplify; this is the truth layer. -->

## Metadata

| Field | Value |
|-------|-------|
| Project | 01-ai-chatbot |
| Core Concepts | LLM APIs, messages array, stateless multi-turn, system prompt, context window, streaming, temperature, token cost, provider abstraction |
| Prerequisites | See PROJECT.md |
| Difficulty | Intermediate |
| Estimated Time | See PROJECT.md |
| Last Updated | 2026-06-01 |

---

## Learning Objectives

By completing this lesson, the learner will be able to:

1. Call a chat completion API and explain every field in the request and response (`model`, `messages`, `system`, `max_tokens`, `temperature`, `stop_reason`, `usage`). [src: anthropic-messages-api]
2. Implement multi-turn conversation by correctly maintaining and resending the `messages` array, given that the API is stateless. [src: anthropic-messages-api]
3. Explain why context windows exist and predict what happens when a conversation exceeds one. [src: anthropic-messages-api]
4. Stream tokens to the UI using server-sent events instead of waiting for the full response. [src: anthropic-streaming]
5. Calculate the exact cost of any API call from `usage` and per-MTok pricing, and project costs at scale. [src: anthropic-pricing]
6. Design a system prompt that reliably changes model behavior, and distinguish it from a user message. [src: anthropic-messages-api]
7. Switch LLM providers without changing application logic, using LiteLLM's unified `completion()` interface. [src: litellm-completion]
8. Identify when a chatbot is the right architecture — and when a single-shot call or a different pattern is better.

---

## Prerequisite Knowledge Check

Before beginning, the learner should be able to answer:

1. What is an HTTP POST request, and what do "request body" and "response body" mean?
2. In Python, what is the difference between a synchronous loop and an `async`/`await` coroutine?
3. What is a list of dictionaries in Python, and how would you append to it inside a loop?
4. What does "stateless" mean for a web server, and why might that be a problem for a conversation?

If any answer is unclear, review it before continuing — the lesson assumes all four.

---

## Core Concepts

| Concept | Definition | Why It Matters |
|---------|-----------|----------------|
| Chat Completions API | A single endpoint (`POST /v1/messages`) that takes a list of messages and returns the model's next message. [src: anthropic-messages-api] | Every AI product is built on this call. |
| Messages array | The ordered list of `{role, content}` turns sent on every request. [src: anthropic-messages-api] | It *is* the conversation — there is no server-side memory. |
| Stateless | The model retains nothing between requests; each call starts fresh. [src: anthropic-messages-api] | Forces you to resend history, which drives cost and context limits. |
| System prompt | Top-level persistent instructions (`system` field) that shape behavior across all turns. [src: anthropic-messages-api] | The cheapest, highest-leverage way to control the model. |
| Context window | The maximum number of tokens the model can "see" (input + output) in one call. [src: anthropic-messages-api] | When history exceeds it, the call fails or must be trimmed. |
| Token | The unit of text a model processes; ~4 characters / ~0.75 words in English. [src: anthropic-pricing] | Tokens — not words — are what you pay for and what fills the window. |
| Streaming | Receiving the response token-by-token via server-sent events. [src: anthropic-streaming] | Makes the UI feel instant instead of frozen. |
| Temperature | A 0.0–1.0 dial for randomness; 0.0 is deterministic-ish, 1.0 is creative. [src: anthropic-messages-api] | Controls reproducibility vs. variety. |
| Token cost | `(input_tokens × in_price + output_tokens × out_price) / 1M`. [src: anthropic-pricing] | The constraint that shapes every production decision. |
| Provider abstraction | A library (LiteLLM) that gives all providers one interface. [src: litellm-completion] | Avoids vendor lock-in; swap models by changing a string. |

### Concept Relationships

```
stateless API  →  resend messages[] every turn  →  input_tokens grows  →  cost grows + context window fills
                          ↑                                                          ↓
                   system prompt (persistent)                          context management (trim/summarize)

request(messages, system, temperature) → [model] → response(content, stop_reason, usage)
                                                          ↓ stream=true
                                                  token-by-token SSE
```

---

## Section 1: Motivation

### Why This Exists
A raw language model is a function: text in, next-token-probabilities out. It has no concept of "a conversation," no memory, and no notion of who is speaking. Before the chat-completions abstraction, using a model for dialogue meant manually formatting a single prompt string and re-parsing the output every turn. The **messages array** standardized this: a structured, role-tagged conversation format that every major provider now speaks. [src: anthropic-messages-api]

### The Problem We're Solving
**LLMs are stateless. Every API call starts fresh.** [src: anthropic-messages-api] If you send "What's the capital of France?" and the model says "Paris," then send "What's its population?", the model has *no idea* what "its" refers to — the second call knows nothing about the first.

The solution is counterintuitive and has huge consequences: **you give the model memory by resending the entire conversation every single time.** The model re-reads the whole history on every turn. This one fact explains why long chats get slow, why they get expensive, and why context windows matter.

### Real-World Stakes
Every RAG system, coding copilot, and agent is a chatbot underneath. Cursor, Claude.ai, ChatGPT, customer-support bots — all manage a messages array, a system prompt, and a context budget. The teams that ship reliable, affordable AI products are the ones who understand this layer instead of treating it as magic. A team that doesn't track tokens ships a product that quietly costs 10× what it should.

### Would Users Pay For This?
On its own, no — a bare chatbot competes with free ChatGPT. The value is in what you wrap around the loop: a system prompt encoding domain expertise, private data the public model can't see, context management tuned to your use case, and cost control. The chatbot is the *infrastructure*; the product is the customization. [src: mlabonne-llm-course]

---

## Section 2: Mental Model

### ELI12 (Explain Like I'm 12)
Imagine you have a brilliant friend with total amnesia. Every time you talk to them, they forget everything the instant the conversation ends. So to have a real conversation, you hand them a notebook with *the entire chat so far* written down. They read the whole notebook, say one new thing, and forget again. To continue, you write their new sentence into the notebook and hand the whole thing back. The notebook is the `messages` array. The friend is the model.

### ELI-Engineer (Explain to a Software Engineer)
The chat API is a **pure function** over conversation state: `f(messages, system, params) → next_message`. There is no session, no cookie, no server-side state. [src: anthropic-messages-api] You maintain the state client-side as an append-only list of `{role, content}` dicts. Each request you send the full list; the response is one `assistant` message you append before the next user turn.

This is the same pattern as a reducer: `state = reduce(state, action)` where actions alternate `user`/`assistant`. The model is trained on strictly alternating roles; consecutive same-role messages get merged. [src: anthropic-messages-api] The `system` prompt is not a message in the array — it's a separate top-level field that conditions every turn. [src: anthropic-messages-api]

### Real-World Analogy
A **courtroom transcript**. The stenographer records every exchange in order. Before the judge rules on a new objection, they (in principle) have the entire transcript available — nothing is assumed from memory; it's all in the record. Add a line, and the next ruling is made against the whole updated record. The transcript grows, and reading it takes longer each time — exactly like `input_tokens` growing every turn.

### Intuition Diagram

```
Turn 1 request:                      Turn 2 request (resends everything):
  system: "You are helpful."           system: "You are helpful."
  messages:                            messages:
    [user] "Capital of France?"          [user] "Capital of France?"
                                         [assistant] "Paris."        ← appended from turn 1's response
  →  [assistant] "Paris."                [user] "Its population?"     ← new
                                       →  [assistant] "About 2.1M."

Each turn re-sends all prior turns. input_tokens grows monotonically.
```

---

## Section 3: Technical Explanation

### Formal Definition
A **chat completion** is a request to `POST /v1/messages` containing a `model`, a `max_tokens` cap, and a `messages` array of `{role: "user"|"assistant", content}` objects, optionally a top-level `system` string and sampling parameters (`temperature`, `top_p`, `stop_sequences`). The response is a `Message` object with `content` (the generated blocks), a `stop_reason`, and a `usage` object reporting `input_tokens` and `output_tokens`. [src: anthropic-messages-api]

### How It Works (Mechanically)
1. You assemble `messages` (full history) + `system` + params.
2. The provider tokenizes the entire input. The token count = `input_tokens`. [src: anthropic-pricing]
3. The model generates output tokens one at a time until it emits a natural stop, hits `max_tokens`, or matches a `stop_sequence`. This is recorded in `stop_reason`. [src: anthropic-messages-api]
4. Non-streaming: you get the whole `Message` at once. Streaming: tokens arrive as SSE events (`message_start` → `content_block_delta`* → `message_stop`). [src: anthropic-streaming]
5. You read `usage` to compute cost, append the `assistant` message to your history, and wait for the next user turn.

### The Math (When Necessary)
Cost per call: [src: anthropic-pricing]
```
cost = input_tokens/1e6 * input_price_per_MTok
     + output_tokens/1e6 * output_price_per_MTok
```
Across an `N`-turn conversation where each turn adds roughly `t` tokens, the input cost is **quadratic-ish**: turn `k` resends ~`k·t` tokens, so total input tokens ≈ `t·(1+2+…+N) = t·N(N+1)/2`. This is *why* long conversations get disproportionately expensive and why context management exists.

### Implementation Details
- **System prompt placement differs by interface.** Raw Anthropic API: top-level `system` field. LiteLLM (OpenAI shape): a `{"role": "system"}` message at the front of `messages`. [src: anthropic-messages-api] [src: litellm-completion]
- **`max_tokens` caps output only**, not input. A `stop_reason` of `max_tokens` means your answer was truncated mid-thought. [src: anthropic-messages-api]
- **Final `usage` in streaming** arrives at the end (`message_delta`/final message), so cost is known only after the stream completes. [src: anthropic-streaming]

---

## Section 4: Guided Examples

### Example 1: Simple Case — one stateless call
```python
import litellm

response = litellm.completion(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    max_tokens=100,
)
print(response.choices[0].message.content)        # "The capital of France is Paris."
print(response.usage.prompt_tokens,                # input_tokens
      response.usage.completion_tokens)            # output_tokens
```
**What to observe:** A single call carries no memory. The `usage` fields are your cost ground-truth — note how small `prompt_tokens` is here versus later. [src: litellm-completion] [src: anthropic-messages-api]

### Example 2: Real-World Case — multi-turn loop with system prompt
```python
import litellm

SYSTEM = "You are a concise assistant. Answer in one sentence."
history = [{"role": "system", "content": SYSTEM}]   # LiteLLM puts system in messages

def ask(user_text: str) -> str:
    history.append({"role": "user", "content": user_text})
    resp = litellm.completion(
        model="claude-sonnet-4-6", messages=history, max_tokens=200, temperature=0.7,
    )
    answer = resp.choices[0].message.content
    history.append({"role": "assistant", "content": answer})   # CRITICAL: persist the turn
    return answer

print(ask("What is the capital of France?"))   # "Paris."
print(ask("What is its population?"))          # resolves "its" -> Paris, because history was resent
```
**What to observe:** The second question only works because the assistant's prior answer was appended to `history`. Forget that append and the model loses the thread. Watch `prompt_tokens` climb each turn. [src: anthropic-messages-api]

### Example 3: Edge Case — streaming + cost tracking
```python
import litellm

PRICES = {"claude-sonnet-4-6": (3.0, 15.0)}   # ($/MTok in, out) — src: anthropic-pricing

def stream_ask(history, model="claude-sonnet-4-6"):
    stream = litellm.completion(model=model, messages=history, max_tokens=500, stream=True)
    parts = []
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)     # token-by-token to the terminal
            parts.append(delta)
    print()
    return "".join(parts)
```
**What to observe:** Text appears incrementally — that's the SSE `content_block_delta` stream. [src: anthropic-streaming] But notice the trap: streamed chunks don't reliably carry final `usage`, so you must count tokens yourself (or do a non-streaming `get_final_message`-style call) to bill accurately. [src: anthropic-streaming]

---

## Section 5: Reflection Before Building

> The learner should fill UNDERSTANDING.md before proceeding to implementation.

**Questions to answer in UNDERSTANDING.md:**

1. Explain "the API is stateless" in your own words (ELI12, then ELI-Engineer). What concretely gives a chatbot memory?
2. Draw your mental model of how `messages` flows from turn to turn. Where does the assistant's reply go?
3. Predict: if you forget to append the assistant's response to history, what exactly breaks — and on which turn?
4. Predict: what is the most likely failure mode once a conversation runs for 100 turns? Tie it to a specific field (`input_tokens`, context window, or cost).
5. The system prompt vs. a first user message: why prefer the system prompt for persistent instructions?
6. Where have you seen the "resend full state each time" pattern before, inside or outside AI?
7. What is the one thing about streaming or token cost you still don't fully understand?

---

## Section 6: Project Assignment

See PROJECT.md for the high-level overview and source/project.md for the full engineering spec.

### Starter Code & Workflow

Setup is solved for you; the core logic is not. `code/` ships labeled starter files (per OPERATING_RULES.md §Scaffolding):

- `provided` — `config.py`, `.env.example`, `tests/` (guiding tests that fail until you implement the core).
- `partial` — `cost_tracker.py`, `context.py` (signatures given; bodies are `TODO(learner)`/`NotImplementedError`).
- `learner` — `chatbot.py` (the conversation loop — the heart of the project — is yours to build).

Workflow: copy `.env.example` → `.env` and add a key; **run** `python chatbot.py`; **test** `python -m pytest`. Make the provided tests pass first (no network needed), then build the loop. The finished core is intentionally not provided — search the starter files for `TODO(learner)`.

### Core Requirement
A CLI chatbot that: (a) holds a multi-turn conversation with correct history management, (b) applies a configurable system prompt, (c) streams responses token-by-token, and (d) reports per-turn and cumulative token cost. The learner must be able to explain every line — no copied magic. [src: anthropic-messages-api] [src: anthropic-streaming] [src: anthropic-pricing]

### Extended Requirements
- Context-window guard: estimate tokens and warn/trim before exceeding a configured budget.
- Provider switch: change one config value to run the same loop on a different model/provider. [src: litellm-completion]
- `/cost` and `/reset` commands; persist a transcript to disk.

---

## Section 7: Project Milestones

| Milestone | What You Build | Validation |
|-----------|---------------|------------|
| M1: One-shot call | Send a single message, print the reply and raw `usage`. | You can name every field in the response. |
| M2: Multi-turn loop | Append user+assistant turns to a list; resend each turn. | "What is its population?" correctly resolves a pronoun from the prior turn. |
| M3: System prompt | Inject a configurable system prompt; observe behavior change. | Same question, two system prompts → visibly different style. |
| M4: Streaming | Switch to `stream=True`; print tokens as they arrive. | Text appears incrementally, not all at once. |
| M5: Cost tracking | Compute per-turn and cumulative cost from `usage` + prices. | Printed cost matches a hand calculation for a known turn. |

---

## Section 8: Self-Evaluation

| Criterion | Does your implementation... | Pass? |
|-----------|---------------------------|-------|
| History correctness | append BOTH user and assistant messages every turn? | |
| Statelessness understood | resend the full history (not just the latest message)? | |
| System prompt | apply persistent instructions separately from user turns? | |
| Streaming | render tokens incrementally via the stream? | |
| Cost accuracy | compute cost from real `usage`, matching a manual check? | |
| Context awareness | detect/handle approaching the context window? | |
| Provider abstraction | swap models without rewriting the loop? | |

**Red flags (your implementation may have problems if):**
- You only send the latest user message (no history) — the bot will seem to have amnesia.
- Your cost is hardcoded or guessed rather than derived from `usage`.
- You can't explain why `input_tokens` grows each turn.
- Streaming "works" but you never capture final token counts.

---

## Section 9: Common Mistakes

| Mistake | Why It Happens | Consequence | Fix |
|---------|---------------|-------------|-----|
| Sending only the latest message | Assuming the server remembers | Bot has no memory; pronouns/context break | Resend the full `messages` array every call [src: anthropic-messages-api] |
| Forgetting to append the assistant reply | Only appending user turns | Model loses its own prior answers | Append BOTH roles each turn |
| Putting instructions in a user message | Not knowing about `system` | Instructions get diluted/overridden as chat grows | Use the `system` field/message [src: anthropic-messages-api] |
| Ignoring `stop_reason` | Only reading `content` | Silent truncation when `max_tokens` hit | Check `stop_reason == "max_tokens"` [src: anthropic-messages-api] |
| Guessing cost | `usage` not inspected | Off-by-orders-of-magnitude budgeting | Compute from `usage` + per-MTok price [src: anthropic-pricing] |
| Assuming words ≈ tokens | Intuitive but wrong | Bad window/cost estimates | Use ~4 chars/token; verify with `usage` [src: anthropic-pricing] |
| Letting history grow unbounded | No trimming | Eventually exceeds context window → error | Cap/trim/summarize history [src: anthropic-messages-api] |

---

## Section 10: Connections

### How This Connects to Previous Projects
This is Project 1 — the foundation. There is no prior project; everything downstream builds on the messages/cost/context mental model established here. [src: mlabonne-llm-course]

### How This Connects to Future Projects
- **P2 (Tokens & Embeddings):** deepens the "what is a token" idea introduced here.
- **P4 (RAG):** retrieved documents get injected into `messages` — the same array, now with stuffed context, making the context-window lesson urgent.
- **P5 (Memory):** an explicit answer to "history grows unbounded" — summarize/store instead of resend.
- **P8 (Agent):** the loop becomes a tool-use loop; `stop_reason == "tool_use"` replaces `end_turn`. [src: anthropic-messages-api]

### How This Connects to StarcallOS
The conversation loop + system prompt + cost tracking is the substrate for any StarcallOS assistant surface. The "resend full state" cost dynamic motivates StarcallOS's memory layer: you cannot resend a user's entire history forever, so you need persistent, retrievable memory (P5) rather than an ever-growing array.

### Production Patterns
Real products manage the array with a **sliding window** (drop oldest turns), **summarization** (compress old turns into a synthetic system note), and **prompt caching** (cache the stable prefix so repeated history costs 0.1× input). [src: anthropic-pricing] Model selection (Haiku→Sonnet→Opus) is a first-order cost lever. [src: anthropic-pricing]

---

## Assessment Rubric

See source/rubric.md for the complete grading rubric.

**Summary criteria:**
- [ ] Implementation runs correctly (multi-turn, system prompt, streaming, cost)
- [ ] Understanding document completed in learner's own words
- [ ] Failure analysis demonstrates intentional experimentation
- [ ] Evaluation is quantitative (real token/cost numbers), not impressionistic
- [ ] StarcallOS reflection identifies at least one concrete applicable pattern

---

## Sources

See source/resources.md for the full annotated source list.

**Required reading:**
- `sources/official-docs/anthropic-messages-api.md` — the request/response contract and stateless multi-turn model
- `sources/official-docs/anthropic-pricing.md` — token cost formula and estimation
- `sources/official-docs/anthropic-streaming.md` — the streaming event protocol

**Recommended reading:**
- `sources/official-docs/litellm-completion.md` — provider abstraction
- `sources/videos/hf-llm-course-intro.md` — NLP vs. LLM framing
- `sources/articles/mlabonne-llm-course.md` — where "running LLMs" sits in the engineer's path

---

## Instructor Notes

<!-- Hidden context for the mentor reviewing the learner's work. -->

**Common misconceptions:**
- "The API remembers my conversation." It does not — the learner must internalize that memory is client-side resending. [src: anthropic-messages-api]
- "Tokens are words." They aren't; ~4 chars/token. [src: anthropic-pricing]
- "Streaming changes the cost/answer." It changes *delivery*, not content or total tokens. [src: anthropic-streaming]
- "`max_tokens` limits the whole conversation." It limits output of one call only.

**Diagnostic questions:**
- "If I delete one line from your loop, which line makes the bot forget everything?" (Appending assistant reply / resending history.)
- "Why does turn 50 cost more than turn 2 even with the same question?" (History resend → input_tokens growth.)
- "Where does the system prompt live, and why not just say it in the first user message?"

**Signs of genuine understanding:**
- Learner predicts the quadratic-ish input-token growth before measuring it.
- Learner reaches for trimming/summarization unprompted when shown a long chat.
- Learner can compute a turn's cost by hand and match it to `usage`.
- Learner explains why streaming complicates accurate cost capture.
