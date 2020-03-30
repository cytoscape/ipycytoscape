#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mariana Meireles.
# Distributed under the terms of the Modified BSD License.

"""
Graph visualization in Jupyter.
"""

from spectate import mvc
from traitlets import TraitType

from ipywidgets.widgets.trait_types import InstanceDict

from ipywidgets import DOMWidget, register, Widget, widget_serialization
from traitlets import Unicode, Bool, Float, Integer, Instance, Dict, List
from ._frontend import module_name, module_version

"""TODO: Remove this after this is somewhat done"""
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#TODO:
#[x] - add_node
#[x] - add_edge
#[x] - remove_node
#[x] - remove_edge
#[x] - set_layout
#[x] - get_layout
#[x] - set_style
#[x] - get_style
#[] - set_tip
#  [] - update TippyJS for latest version
#[] - add from csv
#[] - add from json
#[] - implement get/set for rendered_position
#[x] - add support for edges

class Mutable(TraitType):
    """A base class for mutable traits using Spectate"""

    _model_type = None
    _event_type = "change"

    def instance_init(self, obj):
        default = self._model_type()

        @mvc.view(default)
        def callback(default, events):
            change = dict(
                new=getattr(obj, self.name),
                name=self.name,
                type=self._event_type,
            )
            obj.notify_change(change)

        setattr(obj, self.name, default)

class MutableDict(Mutable):
    """A mutable dictionary trait"""
    _model_type = mvc.Dict

class MutableList(Mutable):
    """A mutable list trait"""
    _model_type = mvc.List

class Edge(Widget):
    """ Edge Widget """
    _model_name = Unicode('EdgeModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    group = Unicode().tag(sync=True)
    removed = Bool().tag(sync=True)
    selected = Bool().tag(sync=True)
    selectable = Bool().tag(sync=True)
    locked = Bool().tag(sync=True)
    grabbed = Bool().tag(sync=True)
    grabbable = Bool().tag(sync=True)
    classes = Unicode().tag(sync=True)

    data = MutableDict().tag(sync=True)
    position = MutableDict().tag(sync=True)

    def __init__(self, **kwargs):
        super(Edge, self).__init__()

        for key, val in kwargs.items():
            setattr(self, key, val)

class Node(Widget):
    """ Node Widget """
    _model_name = Unicode('NodeModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('NodeView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    group = Unicode().tag(sync=True)
    removed = Bool().tag(sync=True)
    selected = Bool().tag(sync=True)
    selectable = Bool().tag(sync=True)
    locked = Bool().tag(sync=True)
    grabbed = Bool().tag(sync=True)
    grabbable = Bool().tag(sync=True)
    classes = Unicode().tag(sync=True)

    data = MutableDict().tag(sync=True)
    position = MutableDict().tag(sync=True)

    def __init__(self, **kwargs):
        super(Node, self).__init__()

        for key, val in kwargs.items():
            setattr(self, key, val)

class Graph(Widget):
    """ Graph Widget """
    _model_name = Unicode('GraphModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    nodes = MutableList(Instance(Node)).tag(sync=True, **widget_serialization)
    edges = MutableList(Instance(Edge)).tag(sync=True, **widget_serialization)

    def __init__(self):
        super(Graph, self).__init__()

    def add_node(self, node):
        """
        Equivalent to Python's append method.
        Parameters
        ----------
        self: cytoscape graph
        node: cytoscape node
        """
        self.nodes.append(node)

    def remove_node(self, node):
        """
        Equivalent to Python's remove method.
        Parameters
        ----------
        self: cytoscape graph
        node: cytoscape node
        """
        self.nodes.remove(node)

    def remove_node_by_id(self, node_id):
        """
        Removes node by the id specified.
        Parameters
        ----------
        self: cytoscape graph
        node_id: numeric types and string
        """
        for node in self.nodes:
            if node.data['id'] == node_id:
                self.nodes.remove(node)
            else:
                print("The id doesn't exist in your graph.")

    def add_edge(self, edge):
        """
        Equivalent to Python's append method.
        Parameters
        ----------
        self: cytoscape graph
        edge: cytoscape edge
        """
        self.edges.append(node)

    def remove_edge(self, edge):
        """
        Equivalent to Python's remove method.
        Parameters
        ----------
        self: cytoscape graph
        edge: cytoscape edge
        """
        self.edges.remove(node)

    def remove_edge_by_id(self, edge_id):
        """
        Removes edge by the id specified.
        Parameters
        ----------
        self: cytoscape graph
        edge_id: numeric types and string
        """
        for edge in self.edges:
            if edge.data['id'] == edge_id:
                self.edges.remove(edge)
            else:
                print("The id doesn't exist in your graph.")

    def complete_graph(self, g):
        """
        Converts a NetworkX graph in to a Cytoscape graph.
        Parameters
        ----------
        self: cytoscape graph
        g: nx graph
            receives a generic NetworkX graph. more info in
            https://networkx.github.io/documentation/
        """
        for node in g.nodes():
            #TODO: test with different **kwargs
            self.nodes.append({'data': {'id': node, 'label': ""}})
        for edge in g.edges():
            self.edges.append({'data': {'source': edge[0],'target': edge[1]}})

class CytoscapeWidget(DOMWidget):
    """ Implements the main Cytoscape Widget """
    _model_name = Unicode('CytoscapeModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('CytoscapeView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    auto_unselectify = Bool(True).tag(sync=True)
    box_selection_enabled = Bool(False).tag(sync=True)
    cytoscape_layout = Dict({'name': 'cola'}).tag(sync=True)
    cytoscape_style = List([{
                        'selector': 'node',
                        'css': {
                            'background-color': 'blue'
                            }
                        },
                        {
                        'selector': 'edge',
                        'css': {
                            'line-color': 'blue'
                            }
                        }]).tag(sync=True)
    zoom = Float(2.0).tag(sync=True)
    rendered_position = Dict({'renderedPosition': { 'x': 100, 'y': 100 }}).tag(sync=True)

    graph = Instance(Graph, args=tuple()).tag(sync=True, **widget_serialization)

    def __init__(self):
        super(CytoscapeWidget, self).__init__()

        self.graph = Graph()

    def set_layout(self, **kwargs):
        """
        Sets the layout of the current object. You can either pass a dictionary
        or change the parameters individually.
        Parameters
        ----------
        name: str
            name of the layout, ex.: cola, grid.
        nodeSpacing: int
            changes padding between nodes
        edgeLengthVal: int
            changes lenght of edges
        padding: int
            adds padding to the whole graph in comparison to the Jupyter's cell
        """

        for key, val in kwargs.items():
            self.cytoscape_layout[key] = val

    def get_layout(self):
        """
        Gets the layout of the current object.
        """
        return self.cytoscape_layout

    def set_style(self, **kwargs):
        """
        Sets the layout of the current object. You can either pass a dictionary
        or change the parameters individually.
        Parameters
        ----------
        stylesheet: dict
            See https://js.cytoscape.org for layout examples.
        """

        for key, val in kwargs.items():
            self.cytoscape_style[key] = val

    def get_style(self):
        """
        Gets the style of the current object.
        """
        return self.cytoscape_style
