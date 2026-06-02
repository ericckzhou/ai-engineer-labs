"""embedding_explorer.py — [partial] Milestone M3 of Project 02 (Token & Embedding Explorer).

Turn text into a MEANING-bearing vector via litellm, and read the vector's dimensionality FROM the
vector itself. This is a different system from the tokenizer: the tokenizer gives reversible IDs
with no meaning; the embedding model gives a (non-reversible) vector whose geometry encodes meaning.

PROVIDED: main() printing harness.
LEARNER: implement embed(). The provider is chosen by config.py (default: local ollama/nomic-embed-text,
768-dim) — you do not pick it here, and you NEVER hardcode the dimension.

Run:  python embedding_explorer.py     (needs an embedding provider — USE_OLLAMA=1 or OPENAI_API_KEY)
"""
from __future__ import annotations

import numpy as np

from config import default_embedding_model


def embed(text: str) -> np.ndarray:
    """[learner] Embed `text` and return the vector as a 1-D numpy array.

    Steps:
      1. resp = litellm.embedding(model=default_embedding_model(), input=[text])
      2. the vector is at  resp["data"][0]["embedding"]
      3. return np.array(that vector)
    Do NOT hardcode the length — different models give different dimensions (768 vs 1536).

    Example (provider-dependent — needs USE_OLLAMA=1 or a cloud key, so there is no offline test;
    shape shown for the default ollama/nomic-embed-text model):
        v = embed("the cat sat on the mat")
        type(v)     # -> numpy.ndarray (1-D)
        v.shape     # -> (768,)   for nomic-embed-text  (READ from the vector, never hardcode)
        embed("the cat sat on the mat")  # same text → same vector (deterministic)
    """
    import litellm

    resp = litellm.embedding(model=default_embedding_model(), input=[text])
    return np.array(resp["data"][0]["embedding"])


# ----------------------------------------------------------------------------------------------
# [provided] Harness: embed a sample, show its dimensionality and first few components.
# ----------------------------------------------------------------------------------------------
def main() -> None:
    print(f"Project 02 — Embedding Explorer (model: {default_embedding_model()})")
    text = "the cat sat on the mat"
    v = embed(text)
    print(f"text       : {text!r}")
    print(f"dimensions : {v.shape[0]}   (read from the vector — never hardcoded)")
    print(f"first 8    : {np.round(v[:8], 4).tolist()}")
    print(f"‖v‖        : {float(np.linalg.norm(v)):.4f}")

    # Determinism check: same text → same vector.
    again = embed(text)
    print(f"stable     : {bool(np.allclose(v, again))}  (same text should give the same vector)")


if __name__ == "__main__":
    main()
