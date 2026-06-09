# Elective 05: Advanced RAG / Query Engineering

# source/project.md — Detailed Project Specification

> High-level overview: root `PROJECT.md`. Teaching content: `source/lesson.agent.md`.
> Implementation contracts, not teaching content.
> **Elective — Production & Hardening track** (depth elective on retrieval). Prereqs: P02, P03, P04.

---

## The One-Sentence Brief

Take Project 04's naive retrieve-then-read and add a **query-transformation stage** — **rewriting**,
**HyDE**, and **multi-hop decomposition + fusion** — then prove on P04's **faithfulness eval** which
transforms actually help (and which don't), using the **provided** P03 re-ranker for fusion.

---

## Definition of Done

- [ ] `query_transforms.py` implements `rewrite(query)`, `hyde(query)`, and `decompose(query)`
      (returns sub-questions).
- [ ] `advanced_rag.answer(query, transform=...)` runs: transform → retrieve(per query) → **fuse**
      (dedupe + re-rank via the provided re-ranker) → read.
- [ ] **Fusion** dedupes the union of multi-query results and re-ranks it (does **not** just
      concatenate); keeps top-N within the context budget.
- [ ] `evaluate_rag.py` runs the frozen QA set **per transform** (baseline / rewrite / HyDE /
      decompose) and reports **faithfulness + answer-relevance + retrieval-hit**.
- [ ] Guiding tests pass offline once cores are implemented; fail with `NotImplementedError` on the
      starter.
- [ ] `UNDERSTANDING.md` (before code) states the two failure modes of naive RAG and that
      transforms must be **eval-gated**.
- [ ] `FAILURE_ANALYSIS.md` ≥3 experiments, **including** a transform that **did not help / hurt**
      (e.g. HyDE on a factual query lowering faithfulness) and a **naive-concatenation fusion**
      blowing relevance.
- [ ] `EVALUATION.md` reports faithfulness **per transform**, honestly — including the ones that
      didn't help.
- [ ] `STARCALLOS_REFLECTION.md` names ≥1 concrete StarcallOS retrieval problem a transform fixes,
      with a mechanism.

---

## File Specification

`code/` provides the **retriever + corpus + re-ranker + faithfulness eval**; the learning target is
the **query-transformation stage** and its **fusion**.

### `config.py` — `provided`
Canonical provider block + `Config`: `retrieve_k` (8), `rerank_top_n` (4),
`faithfulness_threshold` (0.66). Cores read these.

### `rag_backend.py` — `reference`
Condensed Project-04 retriever + corpus + reader, **offline/deterministic**:
- `embed(text)`, `retrieve(query, k)` → ranked chunks (token-overlap retriever, no provider),
- `read(query, chunks)` → an answer grounded in the chunks,
- a small corpus including paraphrase and **multi-hop** items.
Also provides **canned** transform outputs (a fixture map) so the offline core needs no LLM: a
known rewrite / hypothetical-doc / decomposition per eval query.

### `rerank.py` — `provided`
Project 03's cross-encoder-style re-ranker (deterministic). **Used for fusion — do not rebuild.**
`rerank(query, chunks, top_n)` → re-ordered top-n.

### `query_transforms.py` — `learner`
```python
def rewrite(query: str, *, cfg=...) -> str: ...              # reformulate for retrieval (M1)
def hyde(query: str, *, cfg=...) -> str: ...                 # a hypothetical answer to embed (M2)
def decompose(query: str, *, cfg=...) -> list[str]: ...      # sub-questions for multi-hop (M3)
```
Offline: read the canned transform for the query from `rag_backend`; live (extension): call an LLM.

### `advanced_rag.py` — `partial`
```python
@dataclass
class RagResult: answer:str; contexts:list; transform:str

def answer(query: str, *, transform: str = "none", cfg=...) -> RagResult: ...
```
Provided: the skeleton + the `read` call. Learner (TODOs): apply the transform, retrieve per
(sub-)query, **fuse** (dedupe + `rerank`), then read. (M4)

### `eval_set.jsonl` — `provided`
Frozen QA set: `{"query", "answer_keywords", "kind": "paraphrase"|"multihop"|"factual"}` with the
gold chunk id(s). Includes cases where a transform helps AND where it hurts.

### `evaluate_rag.py` — `provided`
Runs each transform over the set; reports faithfulness (supported-claim proxy), answer-relevance,
and retrieval-hit **per transform** — so "which helped" is visible, not assumed.

### `tests/` — `provided`
`test_config.py` (drift), `test_transforms.py` (rewrite/hyde/decompose return the expected shapes
for known queries; decompose yields ≥2 for a multi-hop case), `test_fusion.py` (fusion dedupes the
union and re-ranks; no duplicate chunk ids; ≤ rerank_top_n), `test_pipeline.py` (answer runs for
each transform; a multi-hop query's fused context contains both gold chunks). Offline; fail with
`NotImplementedError` until done.

### `pytest.ini`, `.env.example`, `README.md`, `requirements.txt` — `provided`

---

## Input / Output Contracts

| Function | Input | Output | Edge |
|----------|-------|--------|------|
| `rewrite(query)` | str | reformulated query str | unknown query (offline) → returns query unchanged |
| `hyde(query)` | str | hypothetical-answer str to embed | — |
| `decompose(query)` | str | `list[str]` sub-questions | single-hop → `[query]` |
| `answer(query, transform)` | str, str | `RagResult(answer, contexts, transform)` | fused contexts ≤ `rerank_top_n`, deduped |

---

## Extended Requirements
- [ ] **Self-RAG gate:** a retrieve-or-not decision + relevance/support critique (prompted).
- [ ] **Live transforms:** swap canned transforms for an LLM (rewrite/HyDE/decompose).
- [ ] **Hybrid search:** BM25 + dense union (the hook in `concept-map.md`).
- [ ] **GraphRAG:** link corpus chunks and traverse for multi-hop.

---

## Known Difficulty Spikes
1. **Fusion = dedupe + re-rank, not concatenate.** Naive concatenation dilutes relevance and lowers
   faithfulness.
2. **Not every transform helps.** HyDE can hurt factual queries; rewriting can drift. The eval
   decides.
3. **Don't rebuild re-ranking.** It's P03, provided. Use it for fusion.
4. **Faithfulness, not recall, is the gate.** Retrieving more but grounding worse is a regression.

---

## Debugging Approach
1. `python -m pytest` — implement transforms → fusion/pipeline until green.
2. `python evaluate_rag.py` — read faithfulness **per transform**. A transform with higher hit but
   lower faithfulness is a regression.
3. Replace fusion with naive concatenation and watch faithfulness drop on multi-hop (then restore).
4. Source: re-read `source/lesson.agent.md` §6 (fusion), §8 (eval-gated), `ragas.md`.

---

## Integration Notes
**Depends on:** Project 04 (retriever + corpus + faithfulness eval — provided here), Project 03
(re-ranking — provided), Project 02 (embeddings). **Relates to:** Elective 02 (retrieved content is
also an injection channel — guard it), Elective 03 (each transform costs a generation), Project 09
(routing could pick a transform per query class). The index and re-ranker are given; the **query**
is the new surface.
