#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2020, QuantStack and ipycytoscape Contributors
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.

import pytest

from ipycytoscape.cytoscape import Graph, Node, Edge
import networkx as nx


def compare_nodes(expected_nodes, actual_nodes):
    for expected, actual in zip(expected_nodes, actual_nodes):
        assert expected.data == actual.data
        assert expected.classes == actual.classes
        assert expected.position == actual.position


def compare_edges(expected_edges, actual_edges):
    for expected, actual in zip(expected_edges, actual_edges):
        assert expected.data == actual.data
        assert expected.classes == actual.classes


class TestNetworkx:
    def test_lonely_nodes(self):
        """
        Test to ensure that nodes with no associated edges end up in the graph
        """
        G1 = nx.complete_graph(5)
        G2 = nx.Graph()
        G2.add_node("unconnected_node")
        G2 = nx.complete_graph(1)
        graph = Graph()
        graph.add_graph_from_networkx(G1)
        graph.add_graph_from_networkx(G2)
        expected_nodes = [
            Node(data={"id": "0"}, position={}),
            Node(data={"id": "1"}, position={}),
            Node(data={"id": "2"}, position={}),
            Node(data={"id": "3"}, position={}),
            Node(data={"id": "4"}, position={}),
            Node(data={"id": "unconnected_node"}, position={}),
        ]
        expected_edges = [
            Edge(data={"source": "0", "target": "1"}),
            Edge(data={"source": "0", "target": "2"}),
            Edge(data={"source": "0", "target": "3"}),
            Edge(data={"source": "0", "target": "4"}),
            Edge(data={"source": "1", "target": "2"}),
            Edge(data={"source": "1", "target": "3"}),
            Edge(data={"source": "1", "target": "4"}),
            Edge(data={"source": "2", "target": "3"}),
            Edge(data={"source": "2", "target": "4"}),
            Edge(data={"source": "3", "target": "4"}),
        ]
        compare_nodes(expected_nodes, graph.nodes)
        compare_edges(expected_edges, graph.edges)

    def test_classes(self):
        """
        Test to ensure that approriate classes are added to the networkx object
        """
        G = nx.Graph()
        G.add_node("separate node 1", classes="class1")
        G.add_node("separate node 2", classes="class2")
        G.add_edge("separate node 1", "separate node 2")
        graph = Graph()
        graph.add_graph_from_networkx(G)

        expected_nodes = [
            Node(classes="class1", data={"id": "separate node 1"}),
            Node(classes="class2", data={"id": "separate node 2"}),
        ]
        expected_edges = [
            Edge(data={"source": "separate node 1", "target": "separate node 2"})
        ]

        compare_nodes(expected_nodes, graph.nodes)
        compare_edges(expected_edges, graph.edges)

    def test_directed(self):
        """
        Check that the ' directed ' class is added appropriately
        """
        G = nx.Graph()
        G.add_node("separate node 1")
        G.add_node("separate node 2")
        G.add_edge("separate node 1", "separate node 2")
        G.add_edge("separate node 2", "separate node 1")
        graph = Graph()
        graph.add_graph_from_networkx(G, directed=True)

        expected_nodes = [
            Node(classes="", data={"id": "separate node 1"}, position={}),
            Node(classes="", data={"id": "separate node 2"}, position={}),
        ]
        expected_edges = [
            Edge(
                data={"source": "separate node 1", "target": "separate node 2"},
                classes=" directed ",
            ),
            Edge(
                data={"source": "separate node 2", "target": "separate node 1"},
                classes=" directed ",
            ),
        ]

        compare_nodes(expected_nodes, graph.nodes)
        compare_edges(expected_edges, graph.edges)

    def test_multigraphs(self):
        """
        Test to ensure multigraphs are generated correctly.
        """
        G = nx.MultiGraph()
        G.add_edge(1, 2, weight=15)
        G.add_edge(1, 2, weight=15)
        G.add_edge(1, 2, weight=1)
        G.add_edge(2, 1, weight=10)
        G.add_edge(2, 4)
        graph = Graph()
        graph.add_graph_from_networkx(G)

        expected_edges = [
            Edge(
                classes=" multiple_edges ",
                data={"source": "1", "target": "2", "weight": 15},
            ),
            Edge(
                classes=" multiple_edges ",
                data={"source": "1", "target": "2", "weight": 15},
            ),
            Edge(
                classes=" multiple_edges ",
                data={"source": "1", "target": "2", "weight": 1},
            ),
            Edge(
                classes=" multiple_edges ",
                data={"source": "1", "target": "2", "weight": 10},
            ),
            Edge(classes=" multiple_edges ", data={"source": "2", "target": "4"}),
        ]

        expected_nodes = [
            Node(data={"id": "1"}, position={}),
            Node(data={"id": "2"}, position={}),
            Node(data={"id": "4"}, position={}),
        ]

        compare_edges(expected_edges, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)

        graph = Graph()
        # override default behavior
        graph.add_graph_from_networkx(G, multiple_edges=False)
        expected_edges = [
            Edge(data={"source": "1", "target": "2", "weight": 15}),
            Edge(data={"source": "2", "target": "4"}),
        ]

        compare_edges(expected_edges, graph.edges)

    def test_multidigraphs(self):
        """
        Test to ensure multidigraphs are generated correctly.
        """
        G = nx.MultiDiGraph()
        G.add_edge(1, 2, weight=15)
        G.add_edge(1, 2, weight=15)
        G.add_edge(1, 2, weight=1)
        G.add_edge(2, 1, weight=10)
        G.add_edge(2, 4)
        graph = Graph()
        graph.add_graph_from_networkx(G)

        expected_edges = [
            Edge(
                classes=" directed  multiple_edges ",
                data={"source": "1", "target": "2", "weight": 15},
            ),
            Edge(
                classes=" directed  multiple_edges ",
                data={"source": "1", "target": "2", "weight": 15},
            ),
            Edge(
                classes=" directed  multiple_edges ",
                data={"source": "1", "target": "2", "weight": 1},
            ),
            Edge(
                classes=" directed  multiple_edges ",
                data={"source": "2", "target": "1", "weight": 10},
            ),
            Edge(
                classes=" directed  multiple_edges ",
                data={"source": "2", "target": "4"},
            ),
        ]

        expected_nodes = [
            Node(data={"id": "1"}, position={}),
            Node(data={"id": "2"}, position={}),
            Node(data={"id": "4"}, position={}),
        ]

        compare_edges(expected_edges, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)

        graph = Graph()
        # override default behavior
        graph.add_graph_from_networkx(G, multiple_edges=False, directed=False)
        expected_edges = [
            Edge(data={"source": "1", "target": "2", "weight": 15}),
            Edge(data={"source": "2", "target": "4"}),
        ]

        compare_edges(expected_edges, graph.edges)

    def test_hybridgraphs(self):
        """
        Test graphs with both directed and undirected edges.
        """
        G = nx.MultiGraph()
        G.add_edge(1, 2, weight=15)
        G.add_edge(1, 2, weight=15)
        G.add_edge(2, 4)
        graph = Graph()
        graph.add_graph_from_networkx(G)
        # a custom directed edge in an undirected networkx multigraph
        e = Edge()
        e.data["source"] = "1"
        e.data["target"] = "4"
        graph.add_edge(e, directed=True)

        expected_edges = [
            Edge(
                classes=" multiple_edges ",
                data={"source": "1", "target": "2", "weight": 15},
            ),
            Edge(
                classes=" multiple_edges ",
                data={"source": "1", "target": "2", "weight": 15},
            ),
            Edge(classes=" multiple_edges ", data={"source": "2", "target": "4"}),
            Edge(classes=" directed ", data={"source": "1", "target": "4"}),
        ]
        compare_edges(expected_edges, graph.edges)

    def test_custom_node(self):
        class custom_node:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return "Node: " + str(self.name)

        n1 = custom_node("node 1")
        n2 = custom_node("node 2")

        G = nx.Graph()
        G.add_node(n1)
        G.add_node(n2)
        G.add_edge(n1, n2)
        graph = Graph()
        graph.add_graph_from_networkx(G)

        expected_nodes = [
            Node(classes="", data={"id": "Node: node 1"}, position={}),
            Node(classes="", data={"id": "Node: node 2"}, position={}),
        ]
        expected_edges = [
            Edge(data={"source": "Node: node 1", "target": "Node: node 2"}, classes="")
        ]

        compare_edges(expected_nodes, graph.nodes)
        compare_edges(expected_edges, graph.edges)

    def test_subclassed_node(self):
        class CustomNode(Node):
            def __init__(self, name, classes="", custom_variable=1234):
                super().__init__()
                self.data["id"] = name
                self.classes = classes
                self.custom_variable = custom_variable

        n1 = CustomNode("node 1", classes="class1")
        n2 = CustomNode("node 2", classes="class2")
        G = nx.Graph()
        G.add_node(n1)
        G.add_node(n2)
        G.add_edge(n1, n2)
        graph = Graph()
        graph.add_graph_from_networkx(G)

        expected_nodes = [n1, n2]
        expected_edges = [
            Edge(data={"source": "node 1", "target": "node 2"}, classes="")
        ]

        for expected, actual in zip(expected_nodes, graph.nodes):
            assert expected is actual
        compare_edges(expected_edges, graph.edges)
