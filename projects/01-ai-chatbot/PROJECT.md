# Project 1: AI Chatbot

## What We're Building

A multi-turn conversational AI with streaming responses, a persistent system prompt, configurable context windows, and real-time token/cost tracking.

This is not a wrapper around ChatGPT's UI. You'll build the conversation loop yourself — managing message history, handling context limits, streaming tokens, and understanding what happens at the API level.

## Why We're Building It

Every AI product starts here. RAG systems, agents, copilots — they all use the same fundamental pattern: send messages, get completions, manage context. If you don't understand this foundation deeply, every subsequent project will have invisible gaps.

Most developers use a chat UI and never see the mechanics underneath. We're going to see everything.

## Learning Objectives

By the end of this project, you will be able to:

- [ ] Call a chat completion API and understand every field in the request and response
- [ ] Implement multi-turn conversation with correct message history management
- [ ] Explain why context windows exist and what happens when you exceed them
- [ ] Stream tokens to the UI instead of waiting for full responses
- [ ] Calculate the cost of every API call and project costs at scale
- [ ] Design system prompts that reliably change model behavior
- [ ] Switch between LLM providers without changing application logic (LiteLLM)
- [ ] Identify when a chatbot is the right architecture — and when it isn't

## Prerequisites

- Python basics (functions, classes, loops, async/await)
- Familiarity with REST APIs
- `.env` file set up with at least one API key (see SETUP.md)

## Key Concepts

- **Messages array** — the full conversation history sent on every call
- **System prompt** — persistent instructions that shape model behavior
- **Context window** — the maximum tokens a model can "see" at once
- **Tokens** — the unit of text that LLMs process (not words, not characters)
- **Streaming** — receiving the response token-by-token instead of all at once
- **Temperature** — the randomness/creativity dial
- **LiteLLM** — a library that gives all LLM providers the same API interface

## Core Engineering Problem

**Problem:** LLMs are stateless. Every API call starts fresh. How do you give them "memory" of the conversation?

**Answer:** You send the entire conversation history with every request. This has major implications for cost, performance, and context management.

## Expected Outcomes

- A working CLI chatbot with streaming
- A clear mental model of how the messages array works
- Cost-per-conversation tracking
- Understanding of context window limits

## Time Estimate

**Lesson reading:** 1–2 hours
**Implementation:** 2–4 hours
**Break + Evaluate:** 1–2 hours
**Total:** 4–8 hours

## Startup Lens

**Would users pay for this?** On its own, no — they have ChatGPT. But the *infrastructure* you're building here underpins every paid AI product.

**Where is the value?** In the customization: system prompts, context management, data the public model doesn't have.

## Key Files

```
code/
  chatbot.py          — Main chatbot loop
  config.py           — Model, temperature, max tokens settings
  context.py          — Context window management
  cost_tracker.py     — Token counting and cost calculation
  requirements.txt    — Dependencies
  README.md           — How to run it
```
