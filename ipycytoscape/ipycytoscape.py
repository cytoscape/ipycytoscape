#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mariana Meireles.
# Distributed under the terms of the Modified BSD License.

"""
Graph visualization in Jupyter.
"""

from spectate import mvc
from traitlets import TraitType, HasTraits, observe

from ipywidgets.widgets.trait_types import InstanceDict, TypedTuple

from ipywidgets import DOMWidget, register, Widget, widget_serialization
from traitlets import Dict, Unicode, Bool, List, Float, Integer, Tuple, Instance, Union
from ._frontend import module_name, module_version

"""TODO: Remove this after this is somewhat done"""
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#TODO:
#[] - add_node
#[] - add_edge
#[] - remove_node
#[] - remove_edge
#[] - set_layout
#[] - get_layout
#[] - set_style
#[] - get_style
#[] - set_tip
#  [] - update TippyJS for latest version
#[] - add from csv
#[] - add from json
#[x] - add support for edges

class Mutable(TraitType):
    """A base class for mutable traits using Spectate"""

    _model_type = None
    _event_type = "change"

    def instance_init(self, obj):
        default = self._model_type()

        @mvc.view(default)
        def callback(default, events):
            logging.debug('🐸')
            logging.debug(events)
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
    """A mutable dictionary trait"""
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

    # @observe('data', type='item')
    # def _on_attr_change(self, change):
    #     print(change)
    #     self.notify_change(dict(
    #         owner=self,
    #         name='data',
    #         type='change',
    #         new=self.data,
    #     ))

class Graph(Widget):
    """ Graph Widget """
    _model_name = Unicode('GraphModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    nodes = MutableList(Instance(Node)).tag(sync=True, **widget_serialization)
    edges = MutableList(Instance(Edge)).tag(sync=True, **widget_serialization)

    def __init__(self):
        super(Graph, self).__init__()

    # @observe('nodes', type='item')
    # def _on_nodes_change(self, change):
    #     logging.debug(change)
    #     self.notify_change(dict(
    #         owner=self,
    #         name='nodes',
    #         type='change',
    #         new=self.nodes,
    #     ))

    # @observe('edges', type='item')
    # def _on_edges_change(self, change):
    #     logging.debug(change)
    #     self.notify_change(dict(
    #         owner=self,
    #         name='edges',
    #         type='change',
    #         new=self.edges,
    #     ))

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

    def __init__(self):
        super(CytoscapeWidget, self).__init__()

        self.graph = Graph()

