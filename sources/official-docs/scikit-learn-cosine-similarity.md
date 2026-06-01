# scikit-learn — Cosine Similarity

**Type:** official-doc
**Tier:** 1 (Official Doc)
**Author(s):** scikit-learn developers
**Date:** Accessed 2026-06-01
**URL:** https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity
**Accessed:** 2026-06-01

## Why This Source Matters

Cosine similarity is the metric that turns embedding vectors into a usable similarity *number* — it is the operational core of Project 02's similarity calculator and every retrieval project after it. This source gives the precise formula and, critically, the geometric meaning (angle, not distance) and the magnitude-invariance property that the learner must internalize to avoid the most common embedding bug: confusing "similar" with "close in magnitude."

## Key Claims

### Definition / formula
- Cosine similarity computes the **L2-normalized dot product** of two vectors:

  `k(x, y) = (x · yᵀ) / (‖x‖ · ‖y‖)`

  i.e. the dot product divided by the product of the two vectors' L2 norms (magnitudes).

### What it measures
- Geometrically, it is **the cosine of the angle between the two vectors**. "Euclidean (L2) normalization projects the vectors onto the unit sphere, and their dot product is then the cosine of the angle between the points denoted by the vectors."
- It measures **direction/orientation, not magnitude or distance**.

### Range
- Values run from **−1 to 1**:
  - `1` → same direction (angle 0°) → maximally similar
  - `0` → orthogonal (90°) → unrelated
  - `−1` → opposite direction (180°)
- For typical text/embedding vectors (often non-negative-dominated) values cluster in `[0, 1]`.

### Why it's used for text/embeddings
- Because it ignores magnitude, documents/sentences of **different lengths are compared fairly** — only the orientation of the feature vectors matters, not their absolute scale.
- When vectors are already L2-normalized, cosine similarity equals the plain dot product (`linear_kernel`).

## Relevant To

- concepts: [cosine-similarity, vector-math, semantic-similarity, embedding-space]
- projects: [02-token-embedding-explorer, 03-semantic-search]

## Notes

- Implementation note for the lab: with `numpy`, cosine similarity is `np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))`. Project 02 has the learner write this **by hand once** before reaching for a library, to make the "angle between vectors" intuition concrete.
- Common pitfall to teach: **cosine similarity ≠ Euclidean distance.** Two vectors can have a small angle (high cosine similarity) yet large Euclidean distance if their magnitudes differ. For normalized embeddings the two rankings agree, but the learner should know they are different measures.
- Cosine *similarity* vs. cosine *distance*: distance = `1 − similarity`. Retrieval libraries vary in which they return; mixing them up silently inverts rankings.
