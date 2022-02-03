#!/usr/bin/env python

# Copyright (c) 2021, QuantStack and ipycytoscape Contributors
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.


import copy

import pytest

from ipycytoscape.cytoscape import Edge, Graph, Node

from ._util import compare_edges, compare_nodes


@pytest.fixture(name="edges", scope="function")
def _make_edges():
    ids = ["0", "1", "2"]
    edges = [
        Edge(data={"source": source, "target": target})
        for source, target in zip(ids[:-1], ids[1:])
    ]
    edges_weighted = [
        Edge(data={"source": "0", "target": "1", "weight": str(i)}) for i in range(1, 3)
    ]
    edge_inv = Edge(data={"source": "1", "target": "0"})

    edges += edges_weighted
    edges += [edge_inv]
    return edges


class TestGraphRemoveMethods:
    def test_remove_edge(self):
        """
        Test to ensure that edges will be removed
        """
        # only a small test because everything else is covered in remove_edge_by_id()
        data = {
            "nodes": [
                {"data": {"id": "0"}},
                {"data": {"id": "1"}},
                {"data": {"id": "2"}},
            ],
            "edges": [
                {"data": {"source": "0", "target": "1"}},
                {"data": {"source": "1", "target": "2"}},
                {"data": {"source": "2", "target": "0"}},
            ],
        }
        expected_nodes = [
            Node(data={"id": "0"}, position={}),
            Node(data={"id": "1"}, position={}),
            Node(data={"id": "2"}, position={}),
        ]
        expected_edges = [
            Edge(classes="", data={"source": "1", "target": "2"}),
            Edge(classes="", data={"source": "2", "target": "0"}),
        ]

        graph = Graph()
        graph.add_graph_from_json(data)
        graph.remove_edge(graph.edges[0])
        compare_edges(expected_edges, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)

    def test_remove_edge_by_id(self):
        """
        Test to ensure that edges will be removed given the ids of the nodes
        for different graphs
        """
        data = {
            "nodes": [
                {"data": {"id": "0"}},
                {"data": {"id": "1"}},
                {"data": {"id": "2"}},
            ],
            "edges": [
                {"data": {"source": "0", "target": "1", "weight": "1"}},
                {"data": {"source": "0", "target": "1", "weight": "2"}},
                {"data": {"source": "1", "target": "0"}},
                {"data": {"source": "1", "target": "2"}},
                {"data": {"source": "2", "target": "0"}},
            ],
        }
        expected_nodes = [
            Node(data={"id": "0"}, position={}),
            Node(data={"id": "1"}, position={}),
            Node(data={"id": "2"}, position={}),
        ]
        expected_edges_undirected = [
            Edge(classes="", data={"source": "1", "target": "2"}),
            Edge(classes="", data={"source": "2", "target": "0"}),
        ]
        expected_edges_directed = [
            Edge(classes=" directed ", data={"source": "1", "target": "0"}),
            Edge(classes=" directed ", data={"source": "1", "target": "2"}),
            Edge(classes=" directed ", data={"source": "2", "target": "0"}),
        ]
        expected_edges_multiple = [
            Edge(classes=" multiple_edges ", data={"source": "1", "target": "2"}),
            Edge(classes=" multiple_edges ", data={"source": "2", "target": "0"}),
        ]

        graph = Graph()
        graph.add_graph_from_json(data)
        graph.remove_edge_by_id("0", "1")
        compare_edges(expected_edges_undirected, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)

        graph = Graph()
        graph.add_graph_from_json(data, directed=True)
        graph.remove_edge_by_id("0", "1")
        compare_edges(expected_edges_directed, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)
        graph.remove_edge_by_id("1", "0")
        compare_edges(expected_edges_directed[1:], graph.edges)
        compare_nodes(expected_nodes, graph.nodes)

        graph = Graph()
        graph.add_graph_from_json(data, multiple_edges=True)
        graph.remove_edge_by_id("0", "1")
        compare_edges(expected_edges_multiple, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)

    def test_remove_node(self):
        """
        Test to ensure that nodes will be removed correctly
        """
        data = {
            "nodes": [
                {"data": {"id": "0"}},
                {"data": {"id": "1"}},
                {"data": {"id": "2"}},
            ],
            "edges": [
                {"data": {"source": "0", "target": "1"}},
                {"data": {"source": "1", "target": "2"}},
                {"data": {"source": "2", "target": "0"}},
            ],
        }
        expected_nodes = [
            Node(data={"id": "1"}, position={}),
            Node(data={"id": "2"}, position={}),
        ]
        expected_edges = [
            Edge(classes="", data={"source": "1", "target": "2"}),
        ]

        graph = Graph()
        graph.add_graph_from_json(data)
        graph.remove_node(graph.nodes[0])
        compare_edges(expected_edges, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)

    def test_remove_node_by_id(self):
        """
        Test to ensure that nodes will be removed given the id
        for different graphs with the corresponding edges
        """
        data = {
            "nodes": [
                {"data": {"id": "0"}},
                {"data": {"id": "1"}},
                {"data": {"id": "2"}},
            ],
            "edges": [
                {"data": {"source": "0", "target": "1", "weight": "1"}},
                {"data": {"source": "0", "target": "1", "weight": "2"}},
                {"data": {"source": "1", "target": "0"}},
                {"data": {"source": "1", "target": "2"}},
                {"data": {"source": "2", "target": "0"}},
            ],
        }
        expected_nodes = [
            Node(data={"id": "1"}, position={}),
            Node(data={"id": "2"}, position={}),
        ]
        expected_edges_undirected = [
            Edge(classes="", data={"source": "1", "target": "2"}),
        ]
        expected_edges_directed = [
            Edge(classes=" directed ", data={"source": "1", "target": "2"}),
        ]
        expected_edges_multiple = [
            Edge(classes=" multiple_edges ", data={"source": "1", "target": "2"}),
        ]

        graph = Graph()
        graph.add_graph_from_json(data)
        graph.remove_node_by_id("0")
        compare_edges(expected_edges_undirected, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)

        graph = Graph()
        graph.add_graph_from_json(data, directed=True)
        graph.remove_node_by_id("0")
        compare_edges(expected_edges_directed, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)
        graph.remove_node_by_id("1")
        compare_edges(expected_edges_directed[1:], graph.edges)
        compare_nodes(expected_nodes[1:], graph.nodes)

        graph = Graph()
        graph.add_graph_from_json(data, multiple_edges=True)
        graph.remove_node_by_id("0")
        compare_edges(expected_edges_multiple, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)
        graph.remove_node_by_id("1")
        compare_edges(expected_edges_multiple[1:], graph.edges)
        compare_nodes(expected_nodes[1:], graph.nodes)


class TestGraphAddMethods:
    def test_add_nodes(self):
        """
        Test to ensure that nodes will be added to the graph
        """
        # create some nodes
        ids = ["0", "1"]
        nodes = [Node(data={"id": i}) for i in ids]

        expected_nodes = [
            Node(data={"id": "0"}, position={}),
            Node(data={"id": "1"}, position={}),
        ]
        expected_edges = []

        graph = Graph()
        graph.add_nodes(nodes)
        compare_edges(expected_edges, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)

    def test_add_node(self):
        """
        Test to ensure that a single node will be added to the graph
        """
        # will call add_edges, so no extensive test are necessary
        node = Node(data={"id": "0"})
        expected_nodes = [
            Node(data={"id": "0"}, position={}),
        ]
        expected_edges = []

        graph = Graph()
        graph.add_node(node)
        compare_edges(expected_edges, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)

    def test_add_edges(self, edges):
        """
        Test to ensure that edges with the corresponding nodes will be
        added to the graph.
        """

        expected_nodes = [
            Node(data={"id": "0"}, position={}),
            Node(data={"id": "1"}, position={}),
            Node(data={"id": "2"}, position={}),
        ]
        expected_edges_undirected = [
            Edge(classes="", data={"source": "0", "target": "1"}),
            Edge(classes="", data={"source": "1", "target": "2"}),
        ]

        graph = Graph()
        graph.add_edges(edges)
        compare_edges(expected_edges_undirected, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)

    def test_add_edges_directed(self, edges):
        """
        Test to ensure that edges with the corresponding nodes will be added
        to the graph for directed edges
        """

        expected_nodes = [
            Node(data={"id": "0"}, position={}),
            Node(data={"id": "1"}, position={}),
            Node(data={"id": "2"}, position={}),
        ]
        expected_edges_directed = [
            Edge(classes=" directed ", data={"source": "0", "target": "1"}),
            Edge(classes=" directed ", data={"source": "1", "target": "2"}),
            Edge(classes=" directed ", data={"source": "1", "target": "0"}),
        ]

        graph = Graph()
        graph.add_edges(edges, directed=True)
        compare_edges(expected_edges_directed, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)

    def test_add_edges_multiple_edges(self, edges):
        """
        Test to ensure that edges with the corresponding nodes
        will be added to the graph with multiple_edges.
        """

        expected_nodes = [
            Node(data={"id": "0"}, position={}),
            Node(data={"id": "1"}, position={}),
            Node(data={"id": "2"}, position={}),
        ]
        expected_edges_multiple = [
            Edge(classes=" multiple_edges ", data={"source": "0", "target": "1"}),
            Edge(classes=" multiple_edges ", data={"source": "1", "target": "2"}),
            Edge(
                classes=" multiple_edges ",
                data={"source": "0", "target": "1", "weight": "1"},
            ),
            Edge(
                classes=" multiple_edges ",
                data={"source": "0", "target": "1", "weight": "2"},
            ),
            Edge(classes=" multiple_edges ", data={"source": "1", "target": "0"}),
        ]

        graph = Graph()
        graph.add_edges(edges, multiple_edges=True)
        compare_edges(expected_edges_multiple, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)

    def test_add_edges_2(self):
        """
        Test to ensure that an edge with the corresponding nodes will be
        added to the graph.
        """
        edge = Edge(data={"source": "0", "target": "1"})
        edge_inv = Edge(data={"source": "1", "target": "0"})

        expected_nodes = [
            Node(data={"id": "0"}, position={}),
            Node(data={"id": "1"}, position={}),
        ]
        expected_edges = [
            Edge(classes="", data={"source": "0", "target": "1"}),
        ]
        expected_edges_multiple = [
            Edge(classes="", data={"source": "0", "target": "1"}),
            Edge(classes=" multiple_edges ", data={"source": "1", "target": "0"}),
        ]

        graph = Graph()
        graph.add_edge(copy.copy(edge))
        compare_edges(expected_edges, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)

        # test for passing arguments
        graph.add_edge(copy.copy(edge_inv), multiple_edges=True)
        compare_edges(expected_edges_multiple, graph.edges)
        compare_nodes(expected_nodes, graph.nodes)
