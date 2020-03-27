#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mariana Meireles.
# Distributed under the terms of the Modified BSD License.

"""
Graph visualization in Jupyter.
"""

import networkx as nx
import matplotlib.pyplot as plt

import copy

from ipywidgets.widgets.trait_types import InstanceDict, TypedTuple

from ipywidgets import DOMWidget, register, Widget, widget_serialization
from traitlets import Dict, Unicode, Bool, List, Float, Integer, Tuple, Instance, Union
from ._frontend import module_name, module_version

"""TODO: Remove this after this is somewhat done"""
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Node(Widget):
    """ Node Widget """
    _model_name = Unicode('NodeModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    id = Integer().tag(sync=True)
    idInt = Integer().tag(sync=True)
    name = Unicode().tag(sync=True)
    score = Float().tag(sync=True)
    query = Bool().tag(sync=True)
    gene = Bool().tag(sync=True)
    label = Unicode().tag(sync=True)

    x = Float().tag(sync=True)
    y = Float().tag(sync=True)

    group = Unicode().tag(sync=True)
    removed = Bool().tag(sync=True)
    selected = Bool().tag(sync=True)
    selectable = Bool().tag(sync=True)
    locked = Bool().tag(sync=True)
    grabbed = Bool().tag(sync=True)
    grabbable = Bool().tag(sync=True)
    classes = Unicode().tag(sync=True)

    data = Dict().tag(sync=True)
    position = Dict().tag(sync=True)

    def __init__(self, **kwargs):
        super(Node, self).__init__()

        for key, val in kwargs.items():
            setattr(self, key, val)

class Edge(Widget):
    """ Edge Widget """
    _model_name = Unicode('EdgeModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    id = Integer().tag(sync=True)

    def __init__(self, **kwargs):
        super(Edge, self).__init__()

class Graph(Widget):
    """ Graph Widget """
    _model_name = Unicode('GraphModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    #similar to this... I don't think I'll need it
    nodes = List(Instance(Node)).tag(sync=True, **widget_serialization)
    edges = List(Instance(Edge)).tag(sync=True, **widget_serialization)

    def __init__(self, nodes=[], edges=[]):
        super(Graph, self).__init__()

        self.nodes = nodes
        self.edges = edges

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self):
        pass

class CytoscapeWidget(DOMWidget):
    """ Implements the main Cytoscape Widget """
    _model_name = Unicode('CytoscapeModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('CytoscapeView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    graph = Instance(Graph, args=tuple()).tag(sync=True, **widget_serialization)

    def __init__(self, nodes=[], edges=[]):
        super(CytoscapeWidget, self).__init__()

        self.graph = Graph(nodes, edges)

