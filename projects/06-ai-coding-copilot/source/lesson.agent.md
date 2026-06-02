# Lesson 06: AI Coding Copilot
<!-- lesson.agent.md — Agent-optimized canonical source. Do not simplify; this is the truth layer. -->

## Metadata

| Field | Value |
|-------|-------|
| Project | 06-ai-coding-copilot |
| Core Concepts | tool use (function calling), the agentic loop (ReAct), tool schemas / the agent-computer interface, context injection vs. tool-fetched context, structured output via tools, sandboxed tool execution |
| Prerequisites | See PROJECT.md (Project 01: chat completions via LiteLLM; Project 03/04: embeddings + retrieval for context injection) |
| Difficulty | Intermediate |
| Estimated Time | See PROJECT.md (10–14 hours total) |
| Last Updated | 2026-06-01 |

---

## Learning Objectives

By completing this lesson, the learner will be able to:

1. Explain why an LLM with **no tools** can only *guess* about your codebase, and why giving it tools is "one of the highest-leverage primitives you can give an agent" (source: `sources/official-docs/anthropic-tool-use.md`).
2. Define a **tool** as a `name` + `description` + JSON-schema `parameters`, and explain why "the description is the API" — the model chooses tools from the description alone (source: `sources/official-docs/anthropic-tool-use.md`, `sources/articles/building-effective-agents.md`).
3. Trace the **tool-use request/response protocol**: the model returns a structured tool *call*, your code *executes* it, you feed the *result* back, and the model continues (source: `sources/official-docs/anthropic-tool-use.md`).
4. Implement the **agentic loop** — call the model → if it requested tools, dispatch them and feed results back → repeat until it answers — and explain why the loop, not a clever prompt, is the program (source: `sources/articles/building-effective-agents.md`).
5. Explain **ReAct** (interleaved reasoning + acting) and why *acting* (reading the real file) reduces the hallucination a reasoning-only prompt produces (source: `sources/papers/react-paper.md`).
6. Distinguish **context injection** (retrieve relevant files up front, one shot — Project 03/04 reuse) from **tool-fetched context** (the model pulls exactly the files it decides it needs), and say when each wins.
7. Parse provider tool calls correctly through LiteLLM's OpenAI-style interface — including the trap that `arguments` arrives as a **JSON string** — and bound the loop with `max_steps` (source: `sources/official-docs/litellm-completion.md`, `sources/official-docs/anthropic-tool-use.md`).
8. Name the major **failure modes** of a tool-using copilot (no loop cap → runaway; unsandboxed paths → traversal escape; vague tool descriptions → wrong tool; never feeding results back → the model ignores its own actions) and say which design decision causes each.

---

## Prerequisite Knowledge Check

Before beginning, the learner should be able to answer:

1. From Project 01: how do you build a `messages` list (system + user) and send a chat completion through `litellm.completion`, and where does the reply text live (`response.choices[0].message.content`)?
2. From Project 03/04: how do you embed a query and retrieve the top-k most similar documents from a store? (Context injection is exactly this, applied to source files.)
3. From any prior project: what does it mean that the LLM is a pure text function — it cannot read your disk, run code, or see anything you didn't put in the prompt?

If the learner cannot construct and send a basic LiteLLM chat call (Project 01), revisit that first — the tool loop is that call wrapped in a `while`.

---

## Core Concepts

| Concept | Definition | Why It Matters |
|---------|-----------|----------------|
| Tool use (function calling) | Letting the model emit a structured request to call a function you defined; your code runs it and returns the result | Turns a text-in/text-out model into one that can *act* — read files, search code (source: `sources/official-docs/anthropic-tool-use.md`) |
| Tool schema | A tool's `name`, `description`, and JSON-schema `parameters` | The only thing the model sees about a tool; "the description is the API" (source: `sources/articles/building-effective-agents.md`) |
| Tool call / tool result | The model's structured call (id, name, args) and the value you feed back | The two halves of the protocol; the result is the model's "observation" (source: `sources/official-docs/anthropic-tool-use.md`) |
| Agentic loop | call model → run requested tools → feed results back → repeat until it answers | The program itself; the model drives control flow (source: `sources/articles/building-effective-agents.md`) |
| ReAct | Interleaving reasoning traces with actions (Thought → Action → Observation) | Acting fetches ground truth, cutting the hallucination of reasoning-only prompts (source: `sources/papers/react-paper.md`) |
| Context injection | Retrieve the top-k relevant files up front and put them in the prompt (Project 03/04) | Cheap, one-shot grounding; the model still can't reach beyond what you injected |
| Tool-fetched context | The model decides which files to read, via tools, mid-task | Handles open-ended tasks where you can't predict the files in advance (source: `sources/articles/building-effective-agents.md`) |
| Sandboxed execution | Resolving tool file paths under a fixed repo root and rejecting escapes | A tool that takes a path is an attack surface; `../../etc/passwd` must fail closed |

### Concept Relationships

```
                 ┌──────────────── TOOL SCHEMAS (name + description + params) ─── "the ACI"
                 │                        │ (model picks from description alone)
   user question │                        ▼
        │        │   ┌──────────────────────────────────────────────┐
   inject top-k  │   │  run_agent LOOP  (ReAct: think → act → observe)│
   relevant files├──►│  call model(messages, tools)                  │
   (context      │   │     │                                          │
    injection,   │   │     ├─ no tool calls ──────────► return answer │
    P03/P04)     │   │     └─ tool calls ─► dispatch_tool(name,args)  │
                 │   │            │   (read_file / list_dir / search) │
                 │   │            ▼   safe_resolve(repo_root, path)   │
                 │   │       append tool_result ──► loop (≤ max_steps)│
                 │   └──────────────────────────────────────────────┘
```

Critical framing: **a coding copilot is Project 01's chat call wrapped in a loop, where the model is allowed to read your codebase through tools.** Two ways to get code into the model: *inject* the obviously-relevant files up front (retrieval you already built in P03/P04), and let the model *fetch* the rest itself via tools. ReAct is the grammar of the loop; the tool schema is the interface the model programs against; sandboxing is what keeps a path-taking tool from becoming a security hole.

---

## Section 1: Motivation

### Why This Exists
An LLM is a pure text function: it cannot read your files, list your directory, or run your tests. Ask a bare model "why does `auth.py` throw on login?" and it has never seen `auth.py` — so it **guesses**, fluently and wrongly. The two non-answers before tool use were: paste your whole repo into the prompt (blows the context window and the bill, and most of it is irrelevant), or accept generic advice untethered from your actual code. Tool use is the fix: give the model a few functions — read a file, list a directory, search the code — and let it *pull exactly the context it needs*. "Tool access is one of the highest-leverage primitives you can give an agent"; on real software-engineering benchmarks like SWE-bench, "adding even basic tools produces outsized capability gains" (source: `sources/official-docs/anthropic-tool-use.md`).

### The Problem We're Solving
You want an assistant that answers questions about *your* codebase — "where is the rate limiter configured?", "fix this bug" — grounded in the real files, not in a plausible hallucination. You can't fit the repo in the prompt, and you can't predict in advance which files matter ("fix this bug" might touch one file or five). The answer is an **agent**: "an LLM using tools based on environmental feedback in a loop" (source: `sources/articles/building-effective-agents.md`). The model reasons about what it needs, calls a tool to get it, observes the result, and repeats until it can answer — ReAct's interleaving of thought and action (source: `sources/papers/react-paper.md`).

### Real-World Stakes
This is the most widely adopted AI product category: GitHub Copilot, Cursor, Claude Code, and every internal "ask our codebase" tool are this pattern. The difference between a useful copilot and a dangerous toy is engineering discipline you'll build here: a tool that takes a file path is an **attack surface** (an unsandboxed `read_file` will happily return `../../../../etc/passwd`); a loop with no cap will spin forever burning tokens; a vague tool description makes the model call the wrong tool. None of these show up in the happy-path demo — they show up in production.

### Would Users Pay For This?
"Developer tools are the fastest category to monetize. Developers will pay for tools that save time" (PROJECT.md). A copilot that reads your code and answers in-context removes the constant context-switch from "writing code" to "grepping and reading docs" — immediately measurable value. The augmented LLM (retrieval + tools + memory) is the unit that every one of these products is built from (source: `sources/articles/building-effective-agents.md`).

---

## Section 2: Mental Model

### ELI12 (Explain Like I'm 12)
Imagine you text a very smart friend "why won't my game start?" — but they can't see your computer. They'll guess, and probably guess wrong. Now imagine you give them three buttons they can press that *you* answer for them: **"show me a file," "list a folder,"** and **"search for a word."** Now the conversation changes: they press "list folder," you tell them what's there; they press "show me `game.py`," you paste it; they read it and say "line 12 — you forgot to load the level." They didn't get smarter — they got *eyes*. The whole project is: (1) build those buttons, (2) let your friend keep pressing buttons until they actually know the answer, and (3) make sure a button labeled "show me a file" can't be tricked into showing them your password file.

### ELI-Engineer (Explain to a Software Engineer)
- A **tool** is a function you expose to the model as a schema: `{"type":"function","function":{"name","description","parameters":<JSON Schema>}}`. The model never sees the body — only the schema (source: `sources/official-docs/anthropic-tool-use.md`).
- You call `litellm.completion(messages, tools=...)`. The model replies one of two ways: plain content (it's done), or **`message.tool_calls`** — a list of `{id, function:{name, arguments}}` where `arguments` is a **JSON string** (source: `sources/official-docs/litellm-completion.md`).
- The **loop**: parse the calls → execute each (`dispatch_tool(name, json.loads(arguments), repo_root)`) → append one `{"role":"tool","tool_call_id":id,"content":result}` message per call → call the model again. Repeat until it returns content with no tool calls, or you hit `max_steps`.
- This is **ReAct**: the model's text is the *Thought*, the tool call is the *Action*, the tool result is the *Observation* you feed back (source: `sources/papers/react-paper.md`).
- **Context injection** (P03/P04) seeds the prompt with the top-k relevant files so the model starts warm; **tools** let it go get whatever else it needs. Use both.
- Every file-taking tool routes through **`safe_resolve(repo_root, path)`** which resolves under the repo root and rejects anything that escapes — fail closed.

### Real-World Analogy
A copilot is a **new contractor on their first day in your codebase**, not a psychic. A bad onboarding hands them nothing and asks "fix the bug" — they guess. A good onboarding gives them a **badge that opens specific doors**: they can read files, list directories, and grep — but only inside *this* building (the repo root), and the badge won't open the server room (the sandbox). They walk around, read what they need, and *then* tell you the fix. The loop is them walking the building; the tool schema is what's printed on each door; the sandbox is what the badge refuses to open.

### Intuition Diagram
```
 USER: "Why does config default to Groq?"
   │  (optionally: inject top-k relevant files as starting context — P03/P04 retrieval)
   ▼
 run_agent loop  (max_steps cap):
   step 1: model ──► tool_call: search_code(query="default_model")
           dispatch ─► safe_resolve+grep ─► "config.py:40 def default_model(): ..."
           append tool_result ──► loop
   step 2: model ──► tool_call: read_file(path="config.py")
           dispatch ─► safe_resolve+open ─► "<contents of config.py>"
           append tool_result ──► loop
   step 3: model ──► (no tool calls) "It defaults to Groq because PROVIDER_DEFAULTS
                      lists GROQ_API_KEY first; see config.py:23." ◄── ANSWER
```

---

## Section 3: Technical Explanation

### Formal Definition
- A **tool** is `(name, description, parameters)` where `parameters` is a JSON Schema. The set of tools is the model's **action space** (source: `sources/official-docs/anthropic-tool-use.md`; `sources/papers/react-paper.md`).
- A **tool call** is `(id, name, arguments)` emitted by the model; in the Anthropic-native shape it is a `tool_use` content block with `stop_reason: "tool_use"`; in the LiteLLM/OpenAI shape it is an entry in `message.tool_calls` with `function.arguments` as a **JSON string** (sources: `sources/official-docs/anthropic-tool-use.md`, `sources/official-docs/litellm-completion.md`).
- A **tool result** is the value your code returns for a given `tool_call_id`, appended as a `{"role":"tool", ...}` message (Anthropic-native: a `tool_result` content block).
- An **agent** is "an LLM using tools based on environmental feedback in a loop" (source: `sources/articles/building-effective-agents.md`). The loop is `run_agent`.

### How It Works (Mechanically)

**Define the tools.** Write `TOOL_SCHEMAS`: for each tool, a `name`, a *careful* `description` (the model picks from this alone), and a `parameters` JSON Schema. Implement the matching functions (`read_file`, `list_directory`, `search_code`).

**(Optional) Inject context.** Embed the user's question, retrieve the top-k most relevant files (Project 03/04 machinery), and prepend them as starting context. This is cheap grounding so the model doesn't have to discover obvious files via tools.

**Call the model.** `litellm.completion(messages, tools=TOOL_SCHEMAS, tool_choice="auto")`. With `auto`, "Claude decides on each turn whether to call a tool or respond directly" (source: `sources/official-docs/anthropic-tool-use.md`).

**Parse tool calls.** If `message.tool_calls` is non-empty, build a list of `(id, name, arguments)` — and `json.loads` the `arguments` string into a dict. If empty, the model answered: return its content.

**Execute (dispatch).** For each call, `dispatch_tool(name, arguments, repo_root)` routes to the right function. Every path argument goes through `safe_resolve` first.

**Feed results back.** Append the assistant message (with its `tool_calls`) to `messages`, then append one `{"role":"tool","tool_call_id":id,"content":result}` per call. The order matters: the assistant turn that *requested* the tools must precede the tool results.

**Loop.** Go back to "Call the model" — now the model sees the observations and either calls more tools or answers. Cap at `max_steps` so a confused model can't loop forever.

### The Math (When Necessary)
There is no math here — this lesson is a control-flow and interface lesson, not a numerical one. The retrieval half (context injection) reuses Project 02's cosine similarity unchanged (`cos(a,b) = (a·b)/(‖a‖‖b‖)`); see that lesson. The only "formula" worth stating is the loop's termination condition: **stop when `message.tool_calls` is empty OR `step == max_steps`.**

### Implementation Details
- **`arguments` is a JSON string, not a dict** (LiteLLM/OpenAI shape). `json.loads(tc.function.arguments)` before dispatch. Forgetting this is the #1 first bug (source: `sources/official-docs/litellm-completion.md`).
- **Append the assistant message before the tool results.** Providers reject a `tool` message that doesn't follow the assistant turn that requested it. Append the returned message object, then the tool results.
- **`max_steps` is mandatory.** A model can request tools indefinitely or thrash on the same call. Bound the loop and return a clear sentinel/last-content when the cap is hit (source: `sources/official-docs/anthropic-tool-use.md`).
- **The description is the API.** The model only sees `name` + `description` + schema — never the body. "Invest just as much effort in creating good agent-computer interfaces (ACI)"; include "edge cases, input format requirements, and clear boundaries" (source: `sources/articles/building-effective-agents.md`).
- **Sandbox every path.** `safe_resolve(repo_root, rel)` resolves the path and confirms it stays under `repo_root`; otherwise raise. An unsandboxed `read_file` is a directory-traversal vulnerability.
- **Tool results are strings.** Return readable text (file contents, a grep listing, an error message) — the model reads them as its observation. On a tool error, return an error *string* the model can react to, don't crash the loop.
- **Context injection vs. tools is not either/or.** Inject the obvious files (cheap, one call), let the model fetch the rest (flexible). "Optimizing single LLM calls with retrieval and in-context examples is usually enough" for simple questions; reserve the loop for open-ended ones (source: `sources/articles/building-effective-agents.md`).
- **Tools are also structured output.** A `tool_use` block is schema-conforming, so defining a tool whose schema is your desired shape *is* how you force structured output (source: `sources/official-docs/anthropic-tool-use.md`).

---

## Section 4: Guided Examples

> The lab stack: `litellm` (chat + tools via `config.py`), provided sandboxed file tools, and a pure-Python loop. See `code/`. Examples below mirror the guiding tests.

### Example 1: Simple Case — sandbox a tool path (`safe_resolve`)
```python
from pathlib import Path
from tools import safe_resolve

repo = "/work/myrepo"
safe_resolve(repo, "src/config.py")     # -> Path("/work/myrepo/src/config.py")  (ok)
safe_resolve(repo, "./README.md")       # -> Path("/work/myrepo/README.md")       (ok)
safe_resolve(repo, "../../etc/passwd")  # -> raises ValueError  (escapes repo root)
```
**What to observe:** a file tool that takes a path is an attack surface. `safe_resolve` resolves the path and **fails closed** if it leaves the repo root. Every tool that touches the filesystem goes through this first — the model's `arguments` are untrusted input.

### Example 2: Real-World Case — parse the model's tool calls (`parse_tool_calls`)
```python
from types import SimpleNamespace
from agent_loop import parse_tool_calls

# Shape LiteLLM returns: message.tool_calls[i].function.arguments is a JSON *string*.
msg = SimpleNamespace(content=None, tool_calls=[
    SimpleNamespace(id="call_1", function=SimpleNamespace(
        name="read_file", arguments='{"path": "config.py"}')),
])
calls = parse_tool_calls(msg)
print(calls[0].name)        # 'read_file'
print(calls[0].arguments)   # {'path': 'config.py'}   ← a dict, json.loads'd from the string
print(parse_tool_calls(SimpleNamespace(content="done", tool_calls=None)))  # []  (model answered)
```
**What to observe:** the model's request arrives as objects whose `arguments` is a **JSON string** — `parse_tool_calls` must `json.loads` it into a dict. When there are no tool calls, it returns `[]`, which is the loop's signal that the model is done (source: `sources/official-docs/litellm-completion.md`).

### Example 3: Edge Case — the loop without a cap runs forever
```python
from agent_loop import run_agent
from types import SimpleNamespace

# A broken/looping model that ALWAYS asks to read the same file, never answers:
def always_calls_tool(messages, tools):
    return SimpleNamespace(content=None, tool_calls=[
        SimpleNamespace(id="c", function=SimpleNamespace(
            name="read_file", arguments='{"path": "config.py"}'))])

answer = run_agent(messages=[{"role":"user","content":"hi"}],
                   repo_root=".", complete=always_calls_tool, max_steps=3)
print(answer)   # a "max steps reached" sentinel — NOT an infinite loop
```
**What to observe:** the model controls the loop, so a confused model can spin forever (or burn your whole budget). `max_steps` is the seatbelt: the loop terminates and returns a clear sentinel. This is the failure the learner reproduces in M6 — and the reason the agentic loop is never an unbounded `while True` (source: `sources/official-docs/anthropic-tool-use.md`).

---

## Section 5: Reflection Before Building

> The learner should fill UNDERSTANDING.md before proceeding to implementation.

**Questions to answer in UNDERSTANDING.md:**

1. In your own words, why does giving a model tools beat writing a cleverer prompt for "why does `auth.py` fail on login?" Use the word *hallucination* and connect it to ReAct.
2. "The description is the API." Explain what the model actually sees about a tool, and predict what happens if two tools have near-identical descriptions.
3. Walk the protocol: the model emits a tool *call*, then what are the exact steps your code takes before the model speaks again? Where does `json.loads` come in, and why?
4. Why must the assistant message be appended *before* the tool-result messages? What breaks if you skip appending the assistant turn?
5. Predict the three failure modes of removing, respectively: (a) the `max_steps` cap, (b) `safe_resolve`, (c) feeding tool results back into `messages`. Which design decision causes each?
6. Context injection vs. tool-fetched context: give one question where injecting the top-k files up front is enough, and one where the model *must* use tools mid-task. Why?
7. The one thing you still don't fully understand about the agentic loop.

---

## Section 6: Project Assignment

See PROJECT.md and source/project.md for the full specification.

### Core Requirement
Build a context-aware coding copilot in `code/` that answers questions about a target repository by reading it through tools:
- **`tools.py`** — `safe_resolve` (path sandbox) and `dispatch_tool` (route a tool call to the right function) are the *learner core*; `read_file` / `list_directory` / `search_code` and `TOOL_SCHEMAS` are *provided* plumbing.
- **`agent_loop.py`** — `parse_tool_calls` (extract calls from the model's message, `json.loads` the args) and `run_agent` (the ReAct loop: call model → dispatch tools → feed results back → repeat to `max_steps`) are the *learner core* — the learning target.
- **`context_selector.py`** — embed the question, rank files by cosine similarity, return the top-k as starting context. *(Provided — Project 02/03 reuse.)*
- **`copilot.py`** — the orchestrator: build the prompt, inject context, run the agent with a real LiteLLM completion, print the answer. *(Provided.)*

### Extended Requirements
- **Reasoning trace (full ReAct):** prompt the model to emit a short *Thought* before each action and surface the Thought→Action→Observation trace so the run is interpretable (source: `sources/papers/react-paper.md`).
- **A write tool (with care):** add `write_file` / apply-a-diff — and require sandboxing + a confirmation/dry-run. Now your copilot edits code, not just reads it.
- **Structured output via a tool:** add an `emit_answer(answer, citations[])` tool and force `tool_choice` to it so the final answer is schema-validated with file:line citations (source: `sources/official-docs/anthropic-tool-use.md`).
- **Parallel tool calls:** handle a model that requests several tools in one turn; execute and feed back all results before looping.

---

## Section 7: Project Milestones

| Milestone | What You Build | Validation |
|-----------|---------------|------------|
| M1: Sandbox paths | `tools.safe_resolve(repo_root, rel)` — resolve under root, reject escapes | valid path resolves; `../../etc/passwd` raises `ValueError` (offline test) |
| M2: Parse tool calls | `agent_loop.parse_tool_calls(message)` — extract `(id,name,args)`, `json.loads` arguments | a fake message yields one call with a dict `arguments`; no calls → `[]` (offline test) |
| M3: Dispatch | `tools.dispatch_tool(name, args, repo_root)` — route to read/list/search, handle unknown | `read_file` dispatch returns the fixture file's contents; unknown tool returns an error string (offline test) |
| M4: The loop | `agent_loop.run_agent(messages, repo_root, complete, max_steps)` — call→dispatch→feed back→repeat | with a scripted `complete`, it executes a tool then returns the final answer; an always-calling `complete` stops at `max_steps` (offline test) |
| M5: Copilot end-to-end | `copilot.py` injects context + runs the agent against a real repo | ask "what does config default to?" and it reads files and answers with a file/line citation |
| M6: Break / Evaluate | Remove `max_steps`, remove `safe_resolve`, or stop feeding results back; observe the failure | runaway loop / path escape / model ignores its own tool output — each recorded in FAILURE_ANALYSIS.md |

---

## Section 8: Self-Evaluation

| Criterion | Does your implementation... | Pass? |
|-----------|---------------------------|-------|
| Tool schemas | define each tool with a `name`, a *specific* `description`, and a JSON-schema `parameters`? | |
| Parse correctly | `json.loads` the `arguments` JSON string into a dict before dispatching? | |
| The loop | call the model, dispatch requested tools, feed results back, and repeat until it answers? | |
| Loop cap | bound the loop with `max_steps` and return cleanly when hit (no infinite loop)? | |
| Message order | append the assistant turn *before* the tool-result messages? | |
| Sandbox | route every file-path argument through `safe_resolve` and reject escapes? | |
| Grounded answer | answer using files it actually read, ideally with a file/line citation — not a guess? | |
| Context injection | seed the prompt with retrieved relevant files (Project 03/04) before the loop? | |

**Red flags (your implementation may have problems if):**
- Your loop is `while True` with no cap — one confused response burns your budget.
- `read_file` will return a path outside the repo (you never sandboxed).
- You pass `tc.function.arguments` straight into the tool without `json.loads`.
- You feed tool results back but forgot to append the assistant message first (provider error).
- The model "answers" without ever calling a tool, and you call that success — it guessed.
- You injected the whole repo into the prompt instead of retrieving the top-k.

---

## Section 9: Common Mistakes

| Mistake | Why It Happens | Consequence | Fix |
|---------|---------------|-------------|-----|
| `arguments` used as a dict directly | It *looks* like an object | `TypeError` / wrong args; tool gets a string | `json.loads(tc.function.arguments)` first (source: `sources/official-docs/litellm-completion.md`) |
| No `max_steps` cap | Happy-path demo always terminates | A looping model spins forever, burning tokens | Bound the loop; return a sentinel at the cap (source: `sources/official-docs/anthropic-tool-use.md`) |
| Unsandboxed file paths | "It's just reading a file" | `../../etc/passwd` traversal; data exfiltration | Route every path through `safe_resolve`; fail closed |
| Tool results without the assistant turn | Appending only the `tool` message | Provider rejects the request (orphan tool result) | Append the assistant message (with `tool_calls`) *then* the results |
| Vague tool descriptions | Treating descriptions as comments | Model picks the wrong tool or fills bad args | "The description is the API" — be specific, give boundaries (source: `sources/articles/building-effective-agents.md`) |
| Crashing on a tool error | Tool raises, loop dies | One bad arg kills the whole answer | Catch and return an error *string*; let the model react (ReAct observation) |
| No tools, clever prompt instead | "The model is smart enough" | Confident hallucination about code it never saw | Give it tools; acting beats reasoning-only (source: `sources/papers/react-paper.md`) |
| Injecting the whole repo | "More context is better" | Context-window blowout and cost; buries the answer | Retrieve top-k relevant files (Project 03/04), let tools fetch the rest |

---

## Section 10: Connections

### How This Connects to Previous Projects
The loop's inner call **is** Project 01's `litellm.completion` — you've just added `tools=` and wrapped it in a `while`. The **context injection** half (embed the question, rank files by cosine, take top-k) is Project 02's similarity and Project 03/04's retrieval applied to source files, unchanged — which is exactly why this lesson leaves it *provided* and spends the learner's effort on the genuinely new thing: the tool loop. The "answer grounded in retrieved text, with citations" goal continues Project 04's faithfulness discipline.

### How This Connects to Future Projects
**Project 07 (evaluation)** is how you'd measure this copilot — correctness, relevance, and whether it hallucinated vs. read the file (the LLM-as-judge and faithfulness metrics applied to tool use). **Project 08 (agent)** is this loop generalized: more tools, planning, sub-tasks, and self-editing memory — "LLMs using tools in a loop" scaled up (source: `sources/articles/building-effective-agents.md`). The tool-use protocol you build here is the substrate for every later agent. MemGPT's "self-editing memory via tools" (Project 05's forward link) is this exact mechanism pointed at the memory store.

### How This Connects to StarcallOS
Any StarcallOS capability that *acts on the user's behalf* — reading their files, searching their data, calling an API, editing a document — is this tool loop. The disciplines here decide whether those actions are safe and useful: sandboxed tools (StarcallOS must never let a tool escape its scope), a bounded loop (never burn the user's budget on a confused agent), grounded answers (act on real data, don't hallucinate), and a clean agent-computer interface (well-described tools the model uses correctly). The copilot is the smallest complete instance of "StarcallOS does something for you."

### Production Patterns
Real copilots are this loop plus engineering: retrieval to seed context (embeddings index over the repo), a curated tool set with carefully documented schemas (the ACI), strict sandboxing and permissioning on every tool, a bounded agentic loop with retries and a step budget, structured/cited final output, and evaluation in the loop (source: `sources/articles/building-effective-agents.md`, `sources/official-docs/anthropic-tool-use.md`). GitHub Copilot, Cursor, and Claude Code are all variations on "augmented LLM (retrieval + tools) run in a loop" with production-grade interfaces and guardrails.

---

## Assessment Rubric

See source/rubric.md for the complete grading rubric.

**Summary criteria:**
- [ ] Implementation runs correctly (inject context → loop: call → dispatch tools → feed back → answer)
- [ ] The loop is bounded (`max_steps`), parses `arguments` via `json.loads`, and orders assistant/tool messages correctly
- [ ] Every file-path tool is sandboxed through `safe_resolve` (traversal fails closed)
- [ ] Understanding document completed in learner's own words
- [ ] Failure analysis demonstrates intentional experimentation (remove the cap / the sandbox / the result feedback — and the resulting failure)
- [ ] Evaluation is concrete (which tools were called, whether the answer cited real files, hallucination check), not impressionistic
- [ ] StarcallOS reflection identifies at least one concrete applicable pattern

---

## Sources

See source/resources.md for the full annotated source list.

**Required reading:**
- `sources/official-docs/anthropic-tool-use.md` — the tool-use protocol: tool schemas, the tool_use/tool_result cycle, the agentic loop, `tool_choice`, tools as structured output
- `sources/articles/building-effective-agents.md` — the definition of an agent ("LLMs using tools in a loop"), the augmented LLM, and the agent-computer interface (ACI)
- `sources/papers/react-paper.md` — ReAct: interleaving reasoning and acting; why acting reduces hallucination and makes loops terminate sensibly

**Recommended reading:**
- `sources/official-docs/litellm-completion.md` — the `tools` / `tool_choice` params and the OpenAI-style `tool_calls` response shape (with `arguments` as a JSON string)
- `sources/papers/rag-paper.md` — retrieval for the context-injection half (carried from Project 04)
- `sources/articles/chunking-strategies.md` — chunking source files for the embeddings index (carried from Project 03/04)

---

## Instructor Notes

<!-- Hidden context for the mentor reviewing the learner's work. -->

**Common misconceptions:**
- That tool use makes the model "smarter." It doesn't — it gives the model *eyes*. The intelligence is the loop + good tools, not a clever prompt (source: `sources/articles/building-effective-agents.md`).
- That `arguments` is a dict. In the LiteLLM/OpenAI shape it's a JSON *string*; you must `json.loads` it (source: `sources/official-docs/litellm-completion.md`).
- That the loop is `while True`. The model drives control flow, so an unbounded loop is a runaway risk — `max_steps` is mandatory (source: `sources/official-docs/anthropic-tool-use.md`).
- That a file tool is harmless. A path argument is untrusted input; without sandboxing it's a directory-traversal hole.
- That context injection and tools are alternatives. They compose: inject the obvious files, let the model fetch the rest.

**Diagnostic questions (reveal genuine vs. surface understanding):**
- "The model returns `tool_calls` but you append only the `tool` result messages and call the model again — what error do you get and why?" (orphan tool result; the assistant turn must precede it.)
- "Your copilot answers instantly without calling any tool. Is that good?" (almost always no — it guessed; check it actually read the file.)
- "Where exactly is the `json.loads`, and what happens if you forget it?" (on `function.arguments`; the tool receives a string, not the parsed args.)
- "Why can't the loop be `while True`?" (the model controls it; a confused model never stops — `max_steps`.)
- "Show me the line that stops `read_file` from returning `/etc/passwd`." (the `safe_resolve` containment check.)

**Signs of genuine understanding:**
- The learner bounds the loop and can explain the runaway failure they're preventing, unprompted.
- They sandbox every path and can demonstrate the traversal attempt failing closed.
- They `json.loads` the arguments and know why (LiteLLM/OpenAI shape).
- They can articulate when a single retrieval-augmented call beats the loop, and reach for the loop only for open-ended tasks (source: `sources/articles/building-effective-agents.md`).
- They connect the loop to ReAct (thought→action→observation) and to Project 08, and treat tool descriptions as an interface to design, not comments.
