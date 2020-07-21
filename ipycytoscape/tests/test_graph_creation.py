#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mariana Meireles Ian Hunt-Isaak
# Distributed under the terms of the Modified BSD License.

import pytest

from ipycytoscape.cytoscape import Graph, Node, Edge
import networkx as nx


class TestNetworkx:
    def test_lonely_nodes(self):
        """
        Test to ensure that nodes with no associated edges end up in the graph
        """
        G1 = nx.complete_graph(5)
        G2 = nx.Graph()
        G2.add_node('unconnected_node')
        G2 = nx.complete_graph(1)
        undirected = Graph()
        undirected.add_graph_from_networkx(G1)
        undirected.add_graph_from_networkx(G2)
        expected_nodes = [
            Node(data={'id': '0'}, position={}),
            Node(data={'id': '1'}, position={}),
            Node(data={'id': '2'}, position={}),
            Node(data={'id': '3'}, position={}),
            Node(data={'id': '4'}, position={}),
            Node(data={'id': 'unconnected_node'}, position={})
            ] 
        expected_edges = [
            Edge(data={'source': '0', 'target': '1'}, position={}),
            Edge(data={'source': '0', 'target': '2'}, position={}),
            Edge(data={'source': '0', 'target': '3'}, position={}),
            Edge(data={'source': '0', 'target': '4'}, position={}),
            Edge(data={'source': '1', 'target': '2'}, position={}),
            Edge(data={'source': '1', 'target': '3'}, position={}),
            Edge(data={'source': '1', 'target': '4'}, position={}),
            Edge(data={'source': '2', 'target': '3'}, position={}),
            Edge(data={'source': '2', 'target': '4'}, position={}),
            Edge(data={'source': '3', 'target': '4'}, position={})
        ] 
        for expected, actual in zip(expected_nodes, undirected.nodes):
            assert expected.data == actual.data
            assert expected.position == actual.position
        for expected, actual in zip(expected_edges, undirected.edges):
            assert expected.data == actual.data
            assert expected.position == actual.position

    def test_classes(self):
        """
        Test to ensure that approriate classes are added to the networkx object
        """
        G = nx.Graph()
        G.add_node('separate node 1', classes='class1')
        G.add_node('separate node 2', classes='class2')
        G.add_edge('separate node 1', 'separate node 2')
        undirected = Graph()
        undirected.add_graph_from_networkx(G)

        expected_nodes = [
            Node(classes='class1', data={'id': 'separate node 1'}, position={}),
            Node(classes='class2', data={'id': 'separate node 2'}, position={})
            ]
        expected_edges = [
            Edge(data={'source': 'separate node 1', 'target': 'separate node 2'}, position={})
        ]

        for expected, actual in zip(expected_nodes, undirected.nodes):
            assert expected.data == actual.data
            assert expected.position == actual.position
        for expected, actual in zip(expected_edges, undirected.edges):
            assert expected.data == actual.data
            assert expected.position == actual.position

    def test_directed(self):
        """
        Check that the ' directed ' class is added approriately
        """
        G = nx.Graph()
        G.add_node('separate node 1')
        G.add_node('separate node 2')
        G.add_edge('separate node 1', 'separate node 2')
        graph = Graph()
        graph.add_graph_from_networkx(G, directed=True)

        expected_nodes = [
            Node(classes='', data={'id': 'separate node 1'}, position={}),
            Node(classes='', data={'id': 'separate node 2'}, position={})
            ]
        expected_edges = [
            Edge(data={'source': 'separate node 1', 'target': 'separate node 2'}, classes = ' directed ', position={})
        ]

        for expected, actual in zip(expected_nodes, graph.nodes):
            assert expected.data == actual.data
            assert expected.classes == actual.classes
            assert expected.position == actual.position
        for expected, actual in zip(expected_edges, graph.edges):
            assert expected.data == actual.data
            assert expected.classes == actual.classes
            assert expected.position == actual.position
