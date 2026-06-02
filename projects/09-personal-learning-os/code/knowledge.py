"""knowledge.py — [partial] Milestone M2 — a lightweight personal KNOWLEDGE GRAPH over saved items.

A flat memory store is a pile; a graph is a map. As you save items, this links them by shared
tags/concepts so "recall" can surface *related* notes, not just exact keyword hits. It's the
engineering cousin of reflection's "link memories into higher-level structure"
(sources/papers/generative-agents.md).

The graph is undirected and weighted: an edge (a, b) exists when items a and b share >= min_shared
tags, and its weight is the NUMBER of shared tags. `related(a)` returns a's neighbors, most-connected
first.

PROVIDED: the KnowledgeGraph dataclass fields (nodes, edges).
LEARNER:  add (M2) and related (M2).

Run:  python -m pytest tests/test_knowledge.py
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class KnowledgeGraph:
    """[partial] Saved items as nodes; shared-tag links as weighted, undirected edges.

    nodes: item_id -> set of tags
    edges: item_id -> {other_id: shared_tag_count}   (kept symmetric: edges[a][b] == edges[b][a])
    """
    nodes: dict = field(default_factory=dict)   # id -> set[str]
    edges: dict = field(default_factory=dict)   # id -> {other_id: int}

    def add(self, item_id, tags, *, min_shared: int = 1) -> None:
        """[learner] Add `item_id` with `tags`, linking it to EXISTING nodes sharing >= min_shared tags. (M2)

        Steps:
          1. Normalize: tags = set(tags). Register the node: self.nodes[item_id] = tags, and make
             sure self.edges[item_id] exists (e.g. self.edges.setdefault(item_id, {})).
          2. INCREMENTALLY link to current members — one pass over self.nodes:
               for other_id, other_tags in self.nodes.items():
                   if other_id == item_id:  continue          # NO self-edge
                   shared = len(tags & other_tags)
                   if shared >= min_shared:
                       self.edges[item_id][other_id] = shared   # set BOTH directions (symmetric)
                       self.edges[other_id][item_id] = shared
          (Do NOT rebuild every pair on each call — that's O(N^2) per save. Link only the new node.)

        The traps:
          - No self-edge: an item is never related to itself (skip other_id == item_id).
          - Symmetric: write edges[a][b] AND edges[b][a] with the same weight.
          - Incremental: link the new node to existing nodes; don't recompute the whole graph.

        Example (mirrors tests/test_knowledge.py::test_graph_*):
            g = KnowledgeGraph()
            g.add(1, {"ai", "memory"}); g.add(2, {"ai", "agents"}); g.add(3, {"cooking"})
            g.edges[1][2] == 1        # share "ai"
            2 not in g.edges.get(3, {})   # 3 shares nothing
            1 not in g.edges[1]       # no self-edge
        """
        raise NotImplementedError("M2: register the node and link it to sharers (symmetric, no self-edge)")

    def related(self, item_id, k: int = 5) -> list:
        """[learner] Return up to `k` neighbor ids of `item_id`, most shared tags first. (M2)

        Steps:
          1. If item_id not in self.edges: return [] (unknown node — nothing related).
          2. Take self.edges[item_id].items() -> (other_id, weight) pairs.
          3. Sort by weight DESC (you may tie-break by other_id for determinism).
          4. Return just the ids, at most k of them. Never include item_id itself (there's no self-edge,
             so this falls out for free).

        Example (mirrors tests/test_knowledge.py::test_related_*):
            # with the graph above:
            related(1) -> [2]      # only neighbor
            related(3) -> []       # no neighbors
        """
        raise NotImplementedError("M2: return up to k neighbor ids ranked by shared-tag weight")
