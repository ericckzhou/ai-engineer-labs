"""similarity_calculator.py — [learner] Milestone M4 — the CONCEPTUAL CORE of Project 02.

Cosine similarity measures the ANGLE between two vectors, not their distance or magnitude:

    cos(a, b) = (a · b) / (‖a‖ · ‖b‖)          range [-1, 1]
      1  → same direction (maximally similar)
      0  → orthogonal (unrelated)
     -1  → opposite

You must implement this BY HAND with numpy. Do not call sklearn's cosine_similarity or any prebuilt
helper — deriving it yourself is the whole point of this milestone. The guiding tests in
tests/test_similarity.py check the invariants (cos(v,v)=1, cos(v,-v)=-1, bounds) with no network.

PROVIDED: main() (embeds a paraphrase pair and an unrelated pair and prints both scores).
LEARNER: cosine_similarity().

Run:  python similarity_calculator.py    (main needs an embedding provider; the math/tests do not)
"""
from __future__ import annotations

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """[learner] Return the cosine of the angle between vectors `a` and `b`.

    Steps (do them explicitly — do not import a cosine helper):
      1. dot = a · b                  (np.dot or a @ b)
      2. na = ‖a‖, nb = ‖b‖           (np.linalg.norm)
      3. return float(dot / (na * nb))
    Result must lie in [-1, 1]. If you get values outside that range, you forgot to divide by a norm.
    """
    raise NotImplementedError("M4: implement cosine_similarity() from scratch - no library shortcut")


# ----------------------------------------------------------------------------------------------
# [provided] Harness: show that paraphrases score HIGH while unrelated text scores LOW —
# proof that embeddings encode meaning, not surface words.
# ----------------------------------------------------------------------------------------------
def main() -> None:
    from embedding_explorer import embed  # imported here so the math is testable without a provider

    a = embed("the cat sat on the mat")
    b = embed("a feline rested on the rug")   # paraphrase: same meaning, almost no shared words
    c = embed("quarterly tax filing")          # unrelated topic

    print("Project 02 — Similarity Calculator")
    print(f"paraphrase  cos(a, b) = {cosine_similarity(a, b):.3f}   (expect HIGH)")
    print(f"unrelated   cos(a, c) = {cosine_similarity(a, c):.3f}   (expect LOW)")
    print(f"identity    cos(a, a) = {cosine_similarity(a, a):.3f}   (must be 1.0)")


if __name__ == "__main__":
    main()
