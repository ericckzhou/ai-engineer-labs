# Resources & Sources

> All sources used for this lesson, organized by tier.
> Every claim in lesson.agent.md traces back to one of these.

---

## Tier 1: Official Documentation

> Primary sources. Check these first.

- **Anthropic — Tool Use (Function Calling) Overview** — `sources/official-docs/anthropic-tool-use.md`
  - URL: https://platform.claude.com/docs/en/docs/build-with-claude/tool-use/overview
  - What to read: tools are `name` + `description` + `input_schema`; the model returns `stop_reason: "tool_use"` with `tool_use` blocks; you execute and return a `tool_result`; the **agentic loop** repeats until it stops; `tool_choice` (auto/any/tool/none); tools as structured output. This is the protocol the project implements.

- **Anthropic — Building Effective Agents** — `sources/articles/building-effective-agents.md`
  - URL: https://www.anthropic.com/engineering/building-effective-agents
  - What to read: the **definition of an agent** ("LLMs using tools based on environmental feedback in a loop"), workflows vs. agents, the **augmented LLM** (retrieval + tools + memory), and the **agent-computer interface (ACI)** — invest in tool descriptions. First-party engineering guidance.

- **LiteLLM — completion()** — `sources/official-docs/litellm-completion.md` (carried from Project 01)
  - URL: https://docs.litellm.ai/docs/completion/input
  - What to read: the `tools` / `tool_choice` params and the OpenAI-style `tool_calls` response shape — each call's `function.arguments` is a **JSON string** you must `json.loads`. The lab's cross-provider tool path.

---

## Tier 2: Foundational Papers

> Academic papers that established the concepts in this lesson.

- **ReAct** — `sources/papers/react-paper.md`
  - Title: ReAct: Synergizing Reasoning and Acting in Language Models
  - Authors: Yao, Zhao, Yu, Du, Shafran, Narasimhan, Cao
  - Year: 2022
  - URL: https://arxiv.org/abs/2210.03629
  - Why it matters: the foundational pattern of the loop — **interleaving reasoning traces and actions** (Thought → Action → Observation). Acting fetches ground truth, which is why it "overcomes issues of hallucination" present in reasoning-only prompting. The conceptual ancestor of tool-use APIs.

- **RAG** — `sources/papers/rag-paper.md` (carried from Project 04)
  - URL: https://arxiv.org/abs/2005.11401
  - Why it matters: retrieval-augmented generation — the **context-injection** half (retrieve relevant files, ground the answer in them) the copilot reuses before reaching for tools.

---

## Tier 3: Engineering Guides

> Practical engineering perspectives.

- **Chunking Strategies** — `sources/articles/chunking-strategies.md` (carried from Project 03/04)
  - URL: https://www.pinecone.io/learn/chunking-strategies/
  - Why it matters: for the extended "chunk + embed per-chunk" code retrieval — chunk-size precision/context tradeoff and overlap, applied to source files.

---

## Tier 4: Educational Sources

> Tutorials, courses, and explanatory content useful for learning.

- (None specific to this lesson. The Anthropic tool-use docs and the ReAct paper are themselves the
  primary teaching sources; the Project 03/04 retrieval sources are the conceptual prerequisites for
  context injection.)

---

## Recommended Reading Order

For a learner new to this topic:

1. Start with: `sources/articles/building-effective-agents.md` — what an agent *is* (an LLM using tools in a loop) and why to keep it simple.
2. Then read: `sources/official-docs/anthropic-tool-use.md` — the concrete protocol (schema → call → result → loop) and `tool_choice`.
3. Then read: `sources/papers/react-paper.md` — why interleaving reasoning and acting reduces hallucination and makes the loop terminate.
4. Reference: `sources/official-docs/litellm-completion.md` — the exact `tools` / `tool_calls` shape the code uses (and the JSON-string `arguments` trap).
5. Reference: `sources/papers/rag-paper.md` — the context-injection half (carried from Project 04).

---

## Further Reading

Topics adjacent to this lesson worth exploring later:

- Self-editing memory as tool use: letting the model decide what to remember/retrieve (MemGPT; bridge from Project 05 to Project 08).
- Multi-tool planning, orchestrator-workers, and evaluator-optimizer agent patterns (Building Effective Agents; bridge to Project 08).
- Strict/structured tool output and schema validation for reliable final answers (Anthropic tool-use docs).
- Sandboxing and permissioning real tools (filesystem, shell, network) — the security surface of an acting agent.
- Evaluating tool-using agents: correctness, tool-call accuracy, and hallucination over actions (bridge to Project 07).
