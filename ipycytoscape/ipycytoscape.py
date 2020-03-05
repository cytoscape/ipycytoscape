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

class Data(Widget):
    _view_name = Unicode('DataView').tag(sync=True)
    _model_name = Unicode('DataModel').tag(sync=True)

    id = Integer().tag(sync=True)
    idInt = Integer().tag(sync=True)
    name = Unicode().tag(sync=True)
    score = Float().tag(sync=True)
    query = Bool().tag(sync=True)
    gene = Bool().tag(sync=True)
    label = Unicode().tag(sync=True)

class Position(Widget):
    _view_name = Unicode('PositionView').tag(sync=True)
    _model_name = Unicode('PositionModel').tag(sync=True)

    _x = Float().tag(sync=True)
    _y = Float().tag(sync=True)

class Node(Data, Position):
    """ Node Widget """
    _model_name = Unicode('NodeModel').tag(sync=True)
    _view_name = Unicode('NodeView').tag(sync=True)

    group = Unicode().tag(sync=True)
    removed = Bool().tag(sync=True)
    selected = Bool().tag(sync=True)
    selectable = Bool().tag(sync=True)
    locked = Bool().tag(sync=True)
    grabbed = Bool().tag(sync=True)
    grabbable = Bool().tag(sync=True)
    classes = Unicode().tag(sync=True)

    data = Dict(trait=Instance(Data)).tag(sync=True)
    position = Dict(trait=Instance(Position)).tag(sync=True)

    def __init__(self):
        super(Node, self).__init__()

class Edge():
    pass

class Graph(Node):
    """ Graph Widget """
    _model_name = Unicode('GraphModel').tag(sync=True)
    _view_name = Unicode('GraphView').tag(sync=True)

    nodes = List(trait=Instance(Node)).tag(sync=True)
    edges = List(trait=Instance(Edge)).tag(sync=True)

    def __init__(self):
        super(Graph, self).__init__()

    def add_node(self, node):
        self.graph.update(node)

    def add_edge(self):
        pass

class CytoscapeWidget(Graph, DOMWidget):
    """ Implements the main Cytoscape Widget """

    _model_name = Unicode('CytoscapeModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('CytoscapeView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    graph = Dict(trait=Instance(Graph)).tag(sync=True)
