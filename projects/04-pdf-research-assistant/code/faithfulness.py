"""faithfulness.py — [learner] Milestone M5 — detect hallucination by measuring faithfulness.

"It seemed to work" is not evaluation. Faithfulness turns "did the model hallucinate?" into a number:
decompose the answer into individual claims, check each against the retrieved context, and score
F = |supported| / |total|. A claim the context does not support is, by definition, made up.
(sources/papers/ragas.md)

PROVIDED: FaithfulnessReport dataclass, main() demo, _VERIFY_SYSTEM prompt for the LLM verifier.
LEARNER: faithfulness_score() (pure — offline test) and check_faithfulness() (needs a provider).

Run:  python faithfulness.py
"""
from __future__ import annotations

from dataclasses import dataclass

from chunker import Chunk
from config import load_config

# A grounded verifier instruction: given context + one claim, answer strictly yes/no.
_VERIFY_SYSTEM = (
    "You verify claims against a context. Reply with exactly 'yes' if the claim can be inferred "
    "from the context, or 'no' if it cannot. Do not explain."
)


@dataclass(frozen=True)
class FaithfulnessReport:
    """[provided] Per-claim verdicts and the aggregate faithfulness score."""
    score: float
    claims: list[str]
    verdicts: list[bool]


def faithfulness_score(verdicts: list[bool]) -> float:
    """[learner] Fraction of claims supported by the context: F = |V| / |S|, in [0, 1].

    Steps:
      1. |S| = len(verdicts) (total claims), |V| = number of True verdicts (supported claims).
      2. Return |V| / |S|.
      3. Edge case: no claims (empty list) -> define as 1.0 (vacuously faithful) — document the choice.

    Example (mirrors tests/test_faithfulness.py::test_faithfulness_score):
        faithfulness_score([True, True, False])  -> 0.6667   # 2 of 3 claims grounded
        faithfulness_score([True, True, True])   -> 1.0
        faithfulness_score([False, False])       -> 0.0       # pure hallucination
        faithfulness_score([])                   -> 1.0       # no claims -> vacuously faithful
    """
    if not verdicts:
        return 1.0  # no claims -> nothing unsupported -> vacuously faithful (documented choice)
    return sum(verdicts) / len(verdicts)


def check_faithfulness(answer_text: str, chunks: list[Chunk], claims: list[str] | None = None) -> FaithfulnessReport:
    """[learner] Decompose the answer into claims, verify each against the context, score it.

    Steps:
      1. claims = provided `claims`, or split answer_text into sentence-level claims if None
         (a simple split on '. ' is fine for the lab — real RAGAS uses an LLM to extract statements).
      2. context = "\\n".join(c.text for c in chunks).
      3. For each claim: call litellm.completion with _VERIFY_SYSTEM as the system message and a user
         message containing the context + the claim; map the model's 'yes'/'no' to True/False.
      4. score = faithfulness_score(verdicts).
      5. return FaithfulnessReport(score, claims, verdicts).

    Example (behavioral — needs a provider):
        check_faithfulness("Q3 revenue was 4.2M. Margin was 40%.", [Chunk("c0","Q3 revenue was 4.2M, margin 21%.")])
        -> FaithfulnessReport(score=0.5, claims=[...2...], verdicts=[True, False])
        # claim 1 is supported; claim 2 ("40%") contradicts the context -> unsupported -> hallucination
    """
    import litellm

    if claims is None:
        # Simple sentence split for the lab (real RAGAS uses an LLM to extract statements).
        claims = [s.strip() for s in answer_text.split(". ") if s.strip()]
    context = "\n".join(c.text for c in chunks)
    cfg = load_config()

    verdicts: list[bool] = []
    for claim in claims:
        resp = litellm.completion(
            model=cfg.model,
            messages=[
                {"role": "system", "content": _VERIFY_SYSTEM},
                {"role": "user", "content": f"Context:\n{context}\n\nClaim: {claim}"},
            ],
            temperature=0.0,
        )
        reply = resp.choices[0].message.content.strip().lower()
        verdicts.append(reply.startswith("yes"))

    return FaithfulnessReport(faithfulness_score(verdicts), claims, verdicts)


def main() -> None:
    # The pure score works offline; check_faithfulness needs a provider (see the lesson).
    print("Project 04 — Faithfulness")
    print("faithfulness_score([True, True, False]) =", round(faithfulness_score([True, True, False]), 4))


if __name__ == "__main__":
    main()
