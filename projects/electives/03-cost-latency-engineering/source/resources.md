# Resources — Elective 03: Cost & Latency Engineering

> Curated reading. Truth lives in `sources/`. Read in order.

## Read first — the principle
1. **FrugalGPT** — `sources/papers/frugalgpt.md` (Chen/Zaharia/Zou 2023). The three strategies and
   the cascade. Read for *why* cheap-first-escalate works and where the quality risk is.
2. **Project 07 recap** — `sources/papers/mt-bench.md`. The eval is the gate. A cost win without a
   quality number is half a result.

## Read second — the levers
3. **Anthropic prompt caching** — `sources/official-docs/anthropic-prompt-caching.md`. Stable
   prefix; write ~1.25× / read ~0.1×; stable-before-variable. The zero-quality-risk lever.
4. **GPTCache** — `sources/official-docs/gptcache-semantic-caching.md`. Embed → ANN → threshold =
   hit. The false hit. The lever with quality risk #1.
5. **Anthropic pricing** — `sources/official-docs/anthropic-pricing.md`. The real per-MTok prices.
   Every cost number traces here. Don't invent prices.

## Carried from prior projects
- **Project 02** — embeddings (`word2vec.md`, `sentence-bert.md`): the semantic cache is a
  similarity lookup; same embedder both sides.
- **Project 03** — ANN (`hnsw.md`): the nearest-neighbor search under the cache.
- **Project 08** — the budget pattern: `CostTracker` reuses it.

## How sources map to code
| Source | Code |
|--------|------|
| prompt caching | M1 (cached prefix; usage tokens) |
| GPTCache | `cache.py` (M2) |
| FrugalGPT | `cascade.py` (M3) |
| pricing | `budget.py` / `cost_of` (M4) |
| MT-Bench (P07) | `evaluate_cost.py` (the gate) |

## Out of scope
- **Model training / distillation** — a real cost lever, but a different discipline (no training
  here). The cascade *approximates* it with routing.
- **Infra-level latency** (CDN, region, batching internals) — touched only via the batch extension.
