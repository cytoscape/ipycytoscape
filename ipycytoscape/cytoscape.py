#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mariana Meireles.
# Distributed under the terms of the Modified BSD License.

import copy

from spectate import mvc
from traitlets import TraitType

from ipywidgets import DOMWidget, Widget, widget_serialization
from traitlets import Unicode, Bool, Float, Integer, Instance, Dict, List
from ._frontend import module_name, module_version

"""TODO: Remove this after this is somewhat done"""
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    nodes = MutableList(Instance(Node)).tag(sync=True, **widget_serialization)
    edges = MutableList(Instance(Edge)).tag(sync=True, **widget_serialization)

    def __init__(self):
        super(Graph, self).__init__()

    def add_node(self, node):
        """
        Appends node to the end of the list. Equivalent to Python's append method.
        Parameters
        ----------
        self: cytoscape graph
        node: cytoscape node
        """
        self.nodes.append(node)

    def remove_node(self, node):
        """
        Removes node from the end of the list. Equivalent to Python's remove method.
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
                raise ValueError("The id doesn't exist in your graph.")

    def add_edge(self, edge):
        """
        Appends edge from the end of the list. Equivalent to Python's append method.
        Parameters
        ----------
        self: cytoscape graph
        edge: cytoscape edge
        """
        self.edges.append(edge)

    def remove_edge(self, edge):
        """
        Removes edge from the end of the list.  Equivalent to Python's remove method.
        Parameters
        ----------
        self: cytoscape graph
        edge: cytoscape edge
        """
        self.edges.remove(edge)

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
                raise ValueError("The id doesn't exist in your graph.")

    def add_graph_from_networkx(self, g):
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
            node_instance = Node()
            node_instance.data = {'id': int(node)}
            self.nodes.append(node_instance)

        for edge in g.edges():
            edge_instance = Edge()
            edge_instance.data = {'source': edge[0],'target': edge[1]}
            self.edges.append(edge_instance)

    def add_graph_from_json(self, json_file):
        """
        Converts a JSON Cytoscape graph in to a ipycytoscape graph.
        (This method only allows the conversion from a JSON that's already
        formatted as a Cytoscape graph).
        Parameters
        ----------
        self: cytoscape graph
        json_file: json file
        """
        for node in json_file['nodes']:
            node_instance = Node()
            node_instance.data = node['data']
            self.nodes.append(node_instance)

        if 'edges' in json_file:
            for edge in json_file['edges']:
                edge_instance = Edge()
                edge_instance.data = edge['data']
                self.edges.append(edge_instance)

    def add_graph_from_df(self, df, groupby_cols, attribute_list=[], edges=tuple()):
        """
        Converts any Pandas DataFrame in to a Cytoscape graph.
        Parameters
        ----------
        self: cytoscape graph
        df: pandas dataframe
        groupby_cols: list of strings (dataframe columns)
        attribute_list: list of strings (dataframe columns)
        edges: tuple in wich the first argument is the source edge and the
            second is the target edge
        """
        grouped = df.groupby(groupby_cols)
        group_nodes = {}
        for i, name in enumerate(grouped.groups):
            if not isinstance(name, tuple):
                name = (name,)
            group_nodes[name] = Node(data={'id': 'parent-{}'.format(i), 'name': name})

        graph_nodes = []
        graph_edges = []
        for index, row in df.iterrows():
            parent = group_nodes[tuple(row[groupby_cols])]

            # Includes content to tips
            tip_content = ''
            for attribute in attribute_list:
                tip_content += '{}: {}\n'.format(attribute, row[attribute])

            # Creates a list with all nodes adding them in the correct node parents
            graph_nodes.append(Node(data={'id': index, 'parent': parent.data['id'],
                                        'name': tip_content}))

            if not all(edges):
                # Creates a list with all nodes adding them in the correct node parents
                graph_nodes.append(Node(data={'id': index, 'parent': parent.data['id'],
                                            'name': tip_content}))

                graph_edges.append(Edge(data={'id': index, 'source': edges[0],
                                            'target': edges[1]}))

        # Adds group nodes and regular nodes to the graph object
        all_nodes = list(group_nodes.values()) + graph_nodes
        self.nodes.extend(all_nodes)

        self.edges.extend(graph_edges)


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
    cytoscape_style = List([
                            {
                            'selector': 'node',
                            'css': {
                                'background-color': '#11479e'
                                }
                            },
                            {
                            'selector': 'node:parent',
                            'css': {
                                'background-opacity': 0.333
                                }
                            },
                            {
                                'selector': 'edge',
                                'style': {
                                    'width': 4,
                                    'line-color': '#9dbaea',
                                }
                            }
                        ]).tag(sync=True)
    zoom = Float(2.0).tag(sync=True)
    rendered_position = Dict({'renderedPosition': { 'x': 100, 'y': 100 }}).tag(sync=True)

    graph = Instance(Graph, args=tuple()).tag(sync=True, **widget_serialization)

    def __init__(self):
        super(CytoscapeWidget, self).__init__()

        self.graph = Graph()

    def set_layout(self, **kwargs):
        """
        Sets the layout of the current object. Change the parameters individually.
        For extensive documentation on the different kinds of layout please refer
        to https://js.cytoscape.org/#layouts
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
        dummyDict = {}
        dummyDict = copy.deepcopy(self.cytoscape_layout)

        for key, value in kwargs.items():
            dummyDict[key] = value

        self.cytoscape_layout = dummyDict


    def get_layout(self):
        """
        Gets the layout of the current object.
        """
        return self.cytoscape_layout

    def set_style(self, style):
        """
        Sets the layout of the current object. Change the parameters with a dictionary.
        Parameters
        ----------
        stylesheet: dict
            See https://js.cytoscape.org for layout examples.
        """
        self.cytoscape_style = style

    def get_style(self):
        """
        Gets the style of the current object.
        """
        return self.cytoscape_style
