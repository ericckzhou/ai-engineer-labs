"""[provided] Guiding tests for knowledge.py — M2 (KnowledgeGraph). OFFLINE, pure logic.

These fail with NotImplementedError until you implement add/related. They pin the graph CONTRACT:
incremental linking by shared tags, symmetric edges, no self-edge, and related() ranked by weight.
"""
from knowledge import KnowledgeGraph


def test_graph_links_shared_tags_and_is_symmetric():
    g = KnowledgeGraph()
    g.add(1, {"ai", "memory"})
    g.add(2, {"ai", "agents"})
    g.add(3, {"cooking"})
    assert g.edges[1][2] == 1          # share "ai"
    assert g.edges[2][1] == 1          # symmetric
    assert 3 not in g.edges.get(1, {})  # 3 shares nothing with 1


def test_graph_no_self_edge():
    g = KnowledgeGraph()
    g.add(1, {"ai", "memory"})
    assert 1 not in g.edges.get(1, {})


def test_graph_edge_weight_counts_shared_tags():
    g = KnowledgeGraph()
    g.add(1, {"ai", "memory", "agents"})
    g.add(2, {"ai", "memory"})
    assert g.edges[1][2] == 2           # two shared tags


def test_related_ranks_by_weight():
    g = KnowledgeGraph()
    g.add(1, {"ai", "memory", "agents"})
    g.add(2, {"ai", "memory"})          # shares 2 with 1
    g.add(3, {"ai"})                    # shares 1 with 1
    assert g.related(1, k=5) == [2, 3]  # heavier link first


def test_related_unknown_node_is_empty():
    g = KnowledgeGraph()
    assert g.related(99) == []


def test_related_no_neighbors_is_empty():
    g = KnowledgeGraph()
    g.add(1, {"solo"})
    assert g.related(1) == []


def test_min_shared_threshold_blocks_weak_links():
    g = KnowledgeGraph()
    g.add(1, {"ai", "memory"})
    g.add(2, {"ai"}, min_shared=2)      # shares only 1 tag with 1, but requires >= 2
    assert 1 not in g.edges.get(2, {})
