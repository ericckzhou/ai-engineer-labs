# Building Effective Agents

**Type:** article (first-party engineering guidance)
**Tier:** 1 (Official Engineering Guidance)
**Author(s):** Anthropic (Erik Schluntz, Barry Zhang)
**Date:** 2024-12-19 (accessed 2026-06-01)
**URL:** https://www.anthropic.com/engineering/building-effective-agents
**Accessed:** 2026-06-01

## Why This Source Matters

This is the primary source for the **definition of an agent** and for the *agentic loop* that Project 06 implements. It draws the line between **workflows** (LLMs orchestrated through predefined code paths) and **agents** (LLMs that "dynamically direct their own processes and tool usage"), and it gives the one-sentence mental model the whole project hangs on: an agent is **an LLM using tools in a loop based on environmental feedback.** It also names the discipline that separates a working copilot from a flaky one — investing in the **agent-computer interface (ACI)**, i.e. tool design and documentation.

## Key Claims

### Workflows vs. agents
- **Workflows** are systems where "LLMs and tools are orchestrated through predefined code paths."
- **Agents** are systems where "LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."
- An agent "begins its work with either a command from, or interactive discussion with, the human user" and then "plan[s] and operate[s] independently."

### The core loop
- An agent operates as **"LLMs using tools based on environmental feedback in a loop."** The model acts, observes the result of the action (the environment's feedback), and decides the next action — repeating until the task is done or a stop condition is hit.

### The augmented LLM is the building block
- The foundational unit is an LLM "enhanced with augmentations such as **retrieval, tools, and memory**." Current models "can actively use these capabilities — generating their own search queries, selecting appropriate tools, and determining what information to retain."
- (Project 06 supplies all three: code **retrieval** for context, file **tools** to act, and the prior project's **memory** patterns.)

### Use the simplest thing that works
- "You should consider adding complexity *only* when it demonstrably improves outcomes." Often "optimizing single LLM calls with retrieval and in-context examples is usually enough."
- Agents suit "open-ended problems where it's difficult or impossible to predict the required number of steps" — exactly the copilot case ("fix this bug" might need 1 file read or 5).

### The agent-computer interface (ACI) is as important as the model
- Developers should "invest just as much effort in creating good *agent*-computer interfaces (ACI)" as in human UIs. Tool definitions deserve careful documentation: "example usage, edge cases, input format requirements, and clear boundaries."

### Named patterns (for context)
- **Prompt chaining** (sequential steps with programmatic checks), **routing** (classify then dispatch), **orchestrator-workers** (a central LLM "dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results"), **evaluator-optimizer** ("one LLM call generates a response while another provides evaluation and feedback in a loop"). Project 06 is the simplest agent: one LLM, a tool loop. Project 08 generalizes.

## Relevant To

- concepts: [agent-definition, agentic-loop, augmented-llm, tool-use, agent-computer-interface, workflows-vs-agents]
- projects: [06-ai-coding-copilot, 08-ai-agent]

## Notes

- **The headline for Project 06:** a copilot is the augmented LLM (retrieval + tools) run in a loop. The "intelligence" is mostly the loop + good tools, not a clever prompt.
- **ACI = the tool's `name`/`description`/schema.** This is why Project 06 makes tool definitions a first-class artifact: the model only ever sees the description. Tied to `sources/official-docs/anthropic-tool-use.md`.
- **Bias toward the simplest design.** The lesson should make the learner *earn* the loop: show that a single retrieval-augmented call handles many cases, and the loop is for the open-ended ones. Don't over-engineer.
