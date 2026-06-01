"""embedding_helpers.py — [provided] litellm embedding glue. NOT the learning target.

Thin wrapper so the rest of the project gets embeddings as plain Python lists without repeating the
provider call. The model is chosen by config.py's provider resolution (default: local
`ollama/nomic-embed-text`, 768-dim) — never hardcoded here. Pin ONE model for both indexing and
querying; mixing models makes distances meaningless (carries over from Project 02).

Run:  python embedding_helpers.py     (prints the active model + a vector dimension)
"""
from __future__ import annotations

from config import default_embedding_model


def embed_many(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts. Returns one vector (list[float]) per input, in order.

    Example:
        embed_many(["hello", "world"])  ->  [[0.01, ...], [0.02, ...]]   # each len == model dim
    """
    import litellm  # lazy: importing this module shouldn't require the provider lib

    resp = litellm.embedding(model=default_embedding_model(), input=texts)
    # litellm normalizes to OpenAI shape: {"data": [{"embedding": [...]}, ...]}
    return [row["embedding"] for row in resp["data"]]


def embed_one(text: str) -> list[float]:
    """Embed a single text. Convenience for queries.

    Example:
        len(embed_one("hello"))  ->  768   # for the default nomic-embed-text model
    """
    return embed_many([text])[0]


def main() -> None:
    model = default_embedding_model()
    v = embed_one("the central bank raised interest rates")
    print(f"embedding model: {model}")
    print(f"dimension      : {len(v)}   (read from the vector — model-specific)")


if __name__ == "__main__":
    main()
