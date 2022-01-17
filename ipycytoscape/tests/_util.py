from typing import List

from ipycytoscape.cytoscape import Edge, Node


def compare_nodes(expected_nodes: List[Node], actual_nodes: List[Node]):
    # if one list is empty
    assert bool(expected_nodes) == bool(actual_nodes)
    for expected, actual in zip(expected_nodes, actual_nodes):
        assert expected.data == actual.data
        assert expected.classes == actual.classes
        assert expected.position == actual.position


def compare_edges(expected_edges: List[Edge], actual_edges: List[Edge]):
    assert bool(expected_edges) == bool(actual_edges)
    for expected, actual in zip(expected_edges, actual_edges):
        assert expected.data == actual.data
        assert expected.classes == actual.classes
