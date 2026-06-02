# Resources & Sources

> All sources used for this lesson, organized by tier.
> Every claim in lesson.agent.md traces back to one of these.

---

## Tier 1: Official Documentation

> Primary sources. Check these first.

- **LiteLLM — completion()** — `sources/official-docs/litellm-completion.md` (carried from Project 01)
  - URL: https://docs.litellm.ai/docs/completion/input
  - What to read: the judge is one `litellm.completion` call; run it at `temperature=0` for repeatable scores. Provider-swappable by model string.

---

## Tier 2: Foundational Papers

> Academic papers that established the concepts in this lesson.

- **Judging LLM-as-a-Judge (MT-Bench / Chatbot Arena)** — `sources/papers/mt-bench.md`
  - Title: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
  - Authors: Zheng, Chiang, Sheng, Zhuang, Wu, Zhuang, Lin, Li, Li, Xing, Zhang, Gonzalez, Stoica
  - Year: 2023
  - URL: https://arxiv.org/abs/2306.05685
  - Why it matters: the primary source for **LLM-as-a-judge** — GPT-4 reaches >80% agreement with humans ("the same level of agreement between humans"); the named **biases** (position, verbosity, self-enhancement, weak math grading); the **mitigations** (reasoning-before-score / chain-of-thought, reference-guided judging, position-swap). The whole project, and its failure analysis, is built on this.

- **RAGAS** — `sources/papers/ragas.md` (carried from Project 04)
  - Title: RAGAS: Automated Evaluation of Retrieval Augmented Generation
  - Authors: Es, James, Espinosa-Anke, Schockaert
  - Year: 2023
  - URL: https://arxiv.org/abs/2309.15217
  - Why it matters: **reference-free** metrics — faithfulness (`F = |V|/|S|`, the hallucination metric), answer relevance, context relevance. The worked metric this project generalizes, and the extended faithfulness judge.

- **Sentence-BERT (SBERT)** — `sources/papers/sentence-bert.md` (carried from Projects 02/04)
  - URL: https://arxiv.org/abs/1908.10084
  - Why it matters: the embeddings behind answer-relevance similarity (the RAGAS AR metric extension).

---

## Tier 3: Engineering Guides

> Practical engineering perspectives.

- (None specific to this lesson. The MT-Bench paper is itself the engineering reference for judge
  design and bias mitigation; regression testing is the engineering *application* of the harness —
  freeze a dataset, score baseline vs candidate, flag per-case drops.)

---

## Tier 4: Educational Sources

> Tutorials, courses, and explanatory content useful for learning.

- (None specific to this lesson. Production eval platforms — Braintrust, LangSmith, OpenAI Evals — are
  the real-world instantiations of these patterns and worth browsing once the core is built.)

---

## Recommended Reading Order

For a learner new to this topic:

1. Start with: `sources/papers/mt-bench.md` — what LLM-as-a-judge is, that it works (~80% agreement), and how it's biased.
2. Then read: `sources/papers/ragas.md` — reference-free metrics (faithfulness) — the worked example this generalizes.
3. Reference: `sources/official-docs/litellm-completion.md` — the judge is one completion call at `temperature=0` (Project 01).
4. Reference: `sources/papers/sentence-bert.md` — embeddings for the answer-relevance extension (Project 02/04).

---

## Further Reading

Topics adjacent to this lesson worth exploring later:

- Pairwise comparison + position-swap, and why pairwise is more robust than absolute scoring (MT-Bench).
- Calibrating an LLM judge against human labels; active sampling of disagreements for spot-checks.
- Reference-free vs reference-based vs judge-based scoring — picking the metric per task.
- Evaluating multi-step **agents** (transcript-level judging) — bridge to Project 08.
- Eval-in-CI: regression gates that block a merge on a quality drop; cost/latency budgets per run.
