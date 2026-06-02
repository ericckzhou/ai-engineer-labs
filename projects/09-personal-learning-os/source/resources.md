# Resources & Sources — Project 09: Personal Learning OS

> All sources used for this lesson, organized by tier.
> Every claim in lesson.agent.md traces back to one of these.
> Project 09 is the **capstone**: it *orchestrates* the prior projects rather than introducing a new
> model technique. The sources are the ones that define **composition** — routing, orchestrator-workers,
> provenance, and reflection — plus the evaluation discipline applied to the system's front door. Most
> carry over from earlier projects; the emphasis shifts to *how the pieces fit into one system.*

---

## Tier 1: Official Documentation / Engineering Guidance

> Primary sources. Check these first.

- **Anthropic — Building Effective Agents** — `sources/articles/building-effective-agents.md`
  - URL: https://www.anthropic.com/engineering/building-effective-agents
  - What to read: the **augmented LLM** as the building block ("an LLM enhanced with augmentations such
    as retrieval, tools, and memory"); the **routing** workflow ("classifies an input and directs it to
    a specialized followup task"; "separation of concerns"; good "for complex tasks where there are
    distinct categories that are better handled separately"); the **orchestrator-workers** pattern (a
    central LLM "dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their
    results"); and "add complexity only when it demonstrably improves outcomes" — here a *routing* rule.
    The spine of the whole capstone.

- **Anthropic — Citations** — `sources/official-docs/anthropic-citations.md`
  - URL: https://platform.claude.com/docs/en/docs/build-with-claude/citations
  - What to read: claim → source location, `cited_text`, verifiable pointers. The production form of the
    **provenance** the orchestrator attaches to every `Response`. (Carried from Project 04.)

- **Anthropic — Tool Use (Function Calling) Overview** — `sources/official-docs/anthropic-tool-use.md`
  - URL: https://platform.claude.com/docs/en/docs/build-with-claude/tool-use/overview
  - What to read: the agentic loop behind the `TASK` route (the bounded agent the OS routes the
    multi-step requests to). Carried from Projects 06/08.

- **LiteLLM — completion()** — `sources/official-docs/litellm-completion.md`
  - URL: https://docs.litellm.ai/docs/completion/input
  - What to read: the single-call interface behind the `CHAT` route and the optional LLM-backed router.
    Carried from Project 01.

---

## Tier 2: Foundational Papers

> Academic papers that established the concepts in this lesson.

- **RAG** — `sources/papers/rag-paper.md`
  - Title: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
  - Authors: Lewis et al.
  - Year: 2020
  - URL: https://arxiv.org/abs/2005.11401
  - Why it matters: **provenance** — an answer should carry a verifiable pointer to what produced it
    (parametric + non-parametric memory; updatable knowledge). Applied here to the orchestrator's
    `Response.provenance`. (Carried from Project 04.)

- **Generative Agents** — `sources/papers/generative-agents.md`
  - Title: Generative Agents: Interactive Simulacra of Human Behavior
  - Authors: Park et al.
  - Year: 2023
  - URL: https://arxiv.org/abs/2304.03442
  - Why it matters: **reflection** — synthesizing/linking memories into higher-level structure — is the
    conceptual basis for the lightweight personal **knowledge graph** (link saved items; surface related)
    and for graph-aware recall. (Carried from Project 05.)

- **MT-Bench / LLM-as-a-Judge** — `sources/papers/mt-bench.md`
  - Title: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
  - Authors: Zheng et al.
  - Year: 2023
  - URL: https://arxiv.org/abs/2306.05685
  - Why it matters: evaluate with **numbers, per case** — applied here to the **router** (per-route
    accuracy, not just an overall mean, so a silently-broken route is visible). (Carried from Projects 07/08.)

- **Knowledge Graphs (survey)** — `sources/papers/knowledge-graphs-survey.md`
  - Title: Knowledge Graphs
  - Authors: Hogan, Blomqvist, Cochez, d'Amato, et al.
  - Year: 2021
  - URL: https://arxiv.org/abs/2003.02320
  - Why it matters: grounds the term **knowledge graph** — entities and relations as a first-class,
    traversable data model. The Project 09 graph stays a **lightweight tag-linked personal graph**
    (not RDF/SPARQL/ontology/KG-embedding); the survey is the source for *why a graph is the right
    structure when links between saved items must be explicit and traversable*.

---

## Tier 3: Engineering Guides

> Practical engineering perspectives.

- (None specific to this lesson beyond the Anthropic engineering guidance in Tier 1. "Building Effective
  Agents" is itself the primary engineering source for the routing and orchestrator-workers patterns the
  capstone is built on.)

---

## Tier 4: Educational Sources

> Tutorials, courses, and explanatory content useful for learning.

- (None specific to this lesson. The prior projects (P01–P08) are the conceptual prerequisites — each
  subsystem the OS routes to is one you already built.)

---

## Scope of the knowledge graph

The *lightweight, tag-linked personal graph* is grounded in two sources: the **knowledge-graphs survey**
(`sources/papers/knowledge-graphs-survey.md`) for the data model — entities and relations as first-class,
traversable structure — and **Generative Agents' reflection** for linking memories into higher-level
structure. The Project 09 implementation stays a **modest educational construct**: a tag-linked personal
graph, **not** a full RDF, SPARQL, ontology, or KG-embedding system. The survey grounds *why a graph is
the right structure* when links between saved items must be explicit and traversable; it does not license
claiming the capstone implements the research area.

---

## Optional — Going Deeper

> Read **after** the OS routes and grades. The capstone is a multi-route system; once it works, the
> real-world question is how to *see inside it* when a route misbehaves. Not required to complete the
> project.

- **OpenTelemetry — GenAI Semantic Conventions** — `sources/official-docs/opentelemetry-genai-semconv.md` *(optional — depth)*
  - URL: https://opentelemetry.io/docs/specs/semconv/gen-ai/
  - Why it matters: standard GenAI telemetry (spans/attributes per model call) — the production form of the per-route logging here. Trace a request across its route, attach token/cost/latency, and make a routing regression a queryable event rather than a guess.
  - Where you'll see this: any production agent/router observed through an OTel-compatible stack (Phoenix, LangSmith, Braintrust, vendor APM).

---

## Recommended Reading Order

For a learner new to this topic:

1. Start with: `sources/articles/building-effective-agents.md` — the augmented LLM, **routing**, and
   **orchestrator-workers**. Read this before writing any code; it defines the whole capstone.
2. Then: `sources/papers/rag-paper.md` — provenance (why every answer carries a pointer to its source).
3. Then: `sources/papers/generative-agents.md` — reflection (the basis for linking saved items into a graph).
4. Reference: `sources/papers/mt-bench.md` — evaluate per case, applied to the router.
5. Reference: `sources/official-docs/anthropic-citations.md` — the production form of provenance.

---

## Further Reading

Topics adjacent to this lesson worth exploring later:

- LLM-based routers vs. small classification models vs. rules — accuracy/latency/cost tradeoffs of each.
- Knowledge-graph construction and entity linking — turning notes into a real semantic graph (the
  primary-source gap noted above).
- Multi-agent orchestration (orchestrator-workers, evaluator-optimizer) — composing several agents
  behind one front door (Building Effective Agents).
- Observability for orchestrated systems: per-route traces, dashboards, and regression alerts on the
  front door.
- Memory consolidation / reflection jobs that summarize and re-index a growing personal store.
