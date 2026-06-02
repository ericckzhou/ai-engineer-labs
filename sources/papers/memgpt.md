# MemGPT: Towards LLMs as Operating Systems

**Type:** paper
**Tier:** 2 (Foundational Paper)
**Author(s):** Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez
**Date:** 2023 (submitted 2023-10-12)
**URL:** https://arxiv.org/abs/2310.08560
**Accessed:** 2026-06-01

## Why This Source Matters

Generative Agents tells you *how to score* memories for retrieval; MemGPT tells you *where memories live* and *how data moves between tiers*. The key insight for Project 05: the LLM's context window is small and fixed, so a real memory system is a **hierarchy** — a little memory in the prompt, a lot of memory outside it — and the system must **page** the right information in and out, just like an operating system manages physical RAM versus disk. This grounds the project's distinction between *what's in the prompt right now* and *the full memory store*, and the idea that retrieval is a paging decision under a budget.

## Key Claims

### The problem: bounded context windows
- "LLMs are constrained by limited context windows, which hinders their utility in tasks ... that require processing or reasoning over extended conversation histories." The context window is finite; conversation and knowledge are not. You cannot just keep appending — you run out of room (and pay for every token).

### The OS analogy: virtual context management
- MemGPT draws "inspiration from traditional operating systems' hierarchical memory systems that ... [provide] the appearance of large memory resources through ... paging between physical memory and disk." It applies this to LLMs: **virtual context management.**
- **Two tiers:**
  - **Main context** — the data in the LLM's prompt/context window. Fast, in-attention, but small (the "RAM"). Holds the system instructions, a working-context scratchpad, and the recent conversation.
  - **External context** — out-of-context storage the model cannot see directly (the "disk"): **recall storage** (full event/conversation history) and **archival storage** (a general read/write datastore, typically vector-searchable).

### Self-editing memory via function calls
- The LLM itself decides what to move between tiers by emitting **function calls**: search recall/archival storage, write new facts to archival memory, edit the working context, evict stale content. "MemGPT ... manages its own memory" — the model is given tools to read and write its memory and is prompted to use them when relevant.
- This makes memory **self-editing**: when the working context fills up, the system flushes/recursively summarizes older content into external storage, and pulls relevant content back in on demand.

### Result
- With paging, an LLM with a small context window can sustain "perpetual" multi-session conversations and reason over documents far larger than its window — by retrieving only the relevant slices into main context at each step.

## Relevant To

- concepts: [memory-hierarchy, context-window-management, paging, self-editing-memory, working-context, archival-storage, recall-storage, retrieval-under-budget]
- projects: [05-personal-memory-system, 08-ai-agent]

## Notes

- **Main context vs external context = "what's in the prompt" vs "the store."** Project 05's retriever is exactly the paging step: pick the top-k memories from the (large) external store to inject into the (small) main context for this turn.
- **Retrieval is a budget decision.** You can't inject everything; `top_k` is the page size. This reframes "which memories to retrieve" (Generative Agents' scoring) as "which pages to load" (MemGPT's hierarchy) — the two papers are complementary halves of the same system.
- **Self-editing memory (the model writing its own memory via tools) is the bridge to Project 08** (agents/tool use). In Project 05 the write-back can be a simple "store every turn"; letting the model *decide* what to remember and rate its importance is the agentic extension.
- **Summarization on eviction** is the standard production move when even external retrieval isn't enough: recursively summarize old history so the gist survives in fewer tokens. Connects to the conversation-memory work in Project 01.
- The OS framing ("LLMs as operating systems") is the mental model: prompt = RAM, vector store = disk, retriever = pager.
