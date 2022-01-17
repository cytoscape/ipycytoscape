#!/usr/bin/env python

# Copyright (c) 2020, QuantStack, Mariana Meireles and ipycytoscape Contributors
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.

import copy
import json
from os import path

from ipywidgets import CallbackDispatcher, DOMWidget, Widget, widget_serialization
from spectate import mvc
from traitlets import (
    Bool,
    CaselessStrEnum,
    CFloat,
    Dict,
    Instance,
    Integer,
    List,
    TraitError,
    TraitType,
    Unicode,
    Union,
)

from ._frontend import module_name, module_version

try:
    import networkx as nx
except ModuleNotFoundError:
    nx = None

try:
    import pandas as pd

except ModuleNotFoundError:
    pd = None

try:
    import py2neo

except ModuleNotFoundError:
    py2neo = None

"""TODO: Remove this after this is somewhat done"""
import logging

logger = logging.getLogger(__name__)

__all__ = [
    "MONITORED_USER_TYPES",
    "MONITORED_USER_INTERACTIONS",
    "Node",
    "Edge",
    "Graph",
    "CytoscapeWidget",
]


MONITORED_USER_TYPES = ("node", "edge")
MONITORED_USER_INTERACTIONS = (
    "mousedown",  # when the mouse button is pressed
    "mouseup",  # when the mouse button is released
    "click",  # after mousedown then mouseup
    "mouseover",  # when the cursor is put on top of the target
    "mouseout",  # when the cursor is moved off of the target
    "mousemove",  # when the cursor is moved somewhere on top of the target
    "touchstart",  # when one or more fingers starts to touch the screen
    "touchmove",  # when one or more fingers are moved on the screen
    "touchend",  # when one or more fingers are removed from the screen
    "tapstart",  # normalised tap start event (either mousedown or touchstart)
    "vmousedown",  # alias for 'tapstart'
    "tapdrag",  # normalised move event (either touchmove or mousemove)
    "vmousemove",  # alias for 'tapdrag'
    "tapdragover",  # normalised over element event (either touchmove or mousemove/mouseover) # noqa
    "tapdragout",  # normalised off of element event (either touchmove or mousemove/mouseout) # noqa
    "tapend",  # normalised tap end event (either mouseup or touchend)
    "vmouseup",  # alias for 'tapend'
    "tap",  # normalised tap event (either click, or touchstart followed by touchend without touchmove) # noqa
    "vclick",  # alias for 'tap'
    "taphold",  # normalised tap hold event
    "cxttapstart",  # normalised right-click mousedown or two-finger tapstart
    "cxttapend",  # normalised right-click mouseup or two-finger tapend
    "cxttap",  # normalised right-click or two-finger tap
    "cxtdrag",  # normalised mousemove or two-finger drag after cxttapstart but before cxttapend # noqa
    "cxtdragover",  # when going over a node via cxtdrag
    "cxtdragout",  # when going off a node via cxtdrag
    "boxstart",  # when starting box selection
    "boxend",  # when ending box selection
    "boxselect",  # triggered on elements when selected by box selection
    "box",  # triggered on elements when inside the box on boxend
)


class CytoInteractionDict(Dict):
    """A trait for specifying cytoscape.js user interactions."""

    default_value = {}
    info_text = (
        "specify a dictionary whose keys are cytoscape model types "
        "(pick from %s) and whose values are iterables of user interaction "
        "event types to get updates on (pick from %s)"
    ) % (
        MONITORED_USER_TYPES,
        MONITORED_USER_INTERACTIONS,
    )

    def validate(self, obj, value):
        retval = super().validate(obj, value)
        try:
            if not (
                set(value.keys()).difference(MONITORED_USER_TYPES)
                or any(
                    set(v).difference(MONITORED_USER_INTERACTIONS)
                    for v in value.values()
                )
            ):
                return retval
        except (AttributeError, TypeError):
            msg = (
                "The %s trait of %s instance must %s, but a value of %s was "
                "specified."
            ) % (self.name, type(obj).__name__, self.info_text, value)
            raise TraitError(msg)


def _interaction_handlers_to_json(pydt, _widget):
    return {k: list(v) for k, v in pydt.items()}


def _interaction_handlers_from_json(js, widget):
    raise ValueError(
        "Do not set ``_interaction_handlers`` from the client. "
        "Widget %s received JSON: %s" % (widget, js)
    )


interaction_serialization = {
    "to_json": _interaction_handlers_to_json,
    "from_json": _interaction_handlers_from_json,
}


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


class Element(Widget):
    _model_name = Unicode("ElementModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("ElementView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    removed = Bool().tag(sync=True)
    selected = Bool().tag(sync=True)
    selectable = Bool().tag(sync=True)
    classes = Unicode().tag(sync=True)
    data = MutableDict().tag(sync=True)
    pannable = Bool().tag(sync=True)
    _base_cyto_attrs = [
        "removed",
        "selected",
        "selectable",
        "classes",
        "data",
        "pannable",
    ]


class Edge(Element):
    """Edge Widget"""

    _model_name = Unicode("EdgeModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("EdgeView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    pannable = Bool(True).tag(sync=True)

    # currently we don't sync anything for edges outside of the base Element
    _cyto_attrs = []


class Node(Element):
    """Node Widget"""

    _model_name = Unicode("NodeModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("NodeView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    position = MutableDict().tag(sync=True)
    locked = Bool(False).tag(sync=True)
    grabbable = Bool(True).tag(sync=True)
    grabbed = Bool(False).tag(sync=True)
    pannable = Bool(False).tag(sync=True)

    _cyto_attrs = ["position", "locked", "grabbable"]


def _set_attributes(instance, data):
    cyto_attrs = instance._cyto_attrs + instance._base_cyto_attrs
    for k, v in data.items():
        if k in cyto_attrs:
            setattr(instance, k, v)
        else:
            instance.data[k] = v


class Graph(Widget):
    """Graph Widget"""

    _model_name = Unicode("GraphModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    nodes = MutableList(Instance(Node)).tag(sync=True, **widget_serialization)
    edges = MutableList(Instance(Edge)).tag(sync=True, **widget_serialization)
    # dictionary for syncing graph structure
    _adj = MutableDict().tag(sync=True)

    def add_node(self, node):
        """
        Appends node to the end of the list. Equivalent to Python's append method.

        Parameters
        ----------
        node : ipycytoscape.Node
        """
        self.add_nodes([node])

    def add_nodes(self, nodes):
        """
        Appends nodes to the end of the list. Equivalent to Python's extend method.

        Parameters
        ----------
        nodes : list of ipycytoscape.Node
        """
        node_list = list()
        for node in nodes:
            if node.data["id"] not in self._adj:
                self._adj[node.data["id"]] = dict()
                node_list.append(node)
        self.nodes.extend(node_list)

    def remove_node(self, node):
        """
        Removes node from the end of the list. Equivalent to Python's remove method.

        Parameters
        ----------
        node : ipycytoscape.Node
        """
        try:
            self.nodes.remove(node)
            for target in list(self._adj[node.data["id"]]):
                self.remove_edge_by_id(node.data["id"], target)
            for source in list(self._adj):
                for target in list(self._adj[source]):
                    if target == node.data["id"]:
                        self.remove_edge_by_id(source, node.data["id"])
            del self._adj[node.data["id"]]
        except ValueError:
            raise ValueError(f'{node.data["id"]} is not present in the graph.')

    def remove_node_by_id(self, node_id):
        """
        Removes node by the id specified.

        Parameters
        ----------
        node_id : numeric or string
        """
        node_list_id = -1
        for i, node in enumerate(self.nodes):
            if node.data["id"] == node_id:
                node_list_id = i
        if node_list_id != -1:
            self.remove_node(self.nodes[node_list_id])
        else:
            raise ValueError(f"{node_id} is not present in the graph.")

    def add_edge(self, edge, directed=False, multiple_edges=False):
        """
        Appends edge from the end of the list. Equivalent to Python's append method.

        Parameters
        ----------
        edge : cytoscape edge
        directed : bool
        multiple_edges : bool
        """
        self.add_edges([edge], directed=directed, multiple_edges=multiple_edges)

    def add_edges(self, edges, directed=False, multiple_edges=False):
        """
        Appends edges from the end of the list. If either the source or target Node
        of an Edge is not already in the graph it will be created and added to
        the Nodes list.

        Parameters
        ----------
        edges : list of ipycytoscape.Edge
        directed : bool
        multiple_edges : boolean
        """
        node_list = list()
        edge_list = list()
        for edge in edges:
            source, target = edge.data["source"], edge.data["target"]

            if directed and "directed" not in edge.classes:
                edge.classes += " directed "
            if multiple_edges and "multiple_edges" not in edge.classes:
                edge.classes += " multiple_edges "

            # If multiple edges are allowed, it's okay to add more
            # edges between the source and target
            if multiple_edges:
                new_edge = True
            # Check to see if the edge source -> target exists in the graph
            # If it does then don't add it again
            elif source in self._adj and target in self._adj[source]:
                new_edge = False
            # Check to see if the edge target-> source exists in an
            # undirected graph (don't add it again)
            elif not directed and target in self._adj and source in self._adj[target]:
                new_edge = False
            # If the edge doesn't exist already
            else:
                new_edge = True
            if new_edge:  # if the edge is not present in the graph
                edge_list.append(edge)
                if source not in self._adj:
                    node_instance = Node()
                    # setting the id, according to current spec should be only int/str
                    node_instance.data = {"id": source}
                    node_list.append(node_instance)
                    self._adj[source] = dict()
                if target not in self._adj:
                    node_instance = Node()
                    # setting the id, according to current spec should be only int/str
                    node_instance.data = {"id": target}
                    node_list.append(node_instance)
                    self._adj[target] = dict()

                if multiple_edges and target in self._adj[source]:
                    self._adj[source][target] += 1
                else:
                    self._adj[source][target] = 1
                if not (directed or "directed" in edge.classes):
                    if multiple_edges and source in self._adj[target]:
                        self._adj[target][source] += 1
                    else:
                        self._adj[target][source] = 1
            else:  # Don't add this edge, already present
                pass
        self.nodes.extend(node_list)
        self.edges.extend(edge_list)

    def remove_edge(self, edge):
        """
        Removes edge from the end of the list.  Equivalent to Python's remove method.

        Parameters
        ----------
        edge : ipcytoscape.Edge
        """
        source = edge.data["source"]
        target = edge.data["target"]

        try:
            self.edges.remove(edge)
            if self._adj[source][target] == 1:
                del self._adj[source][target]
            else:
                self._adj[source][target] -= 1
            if "directed" not in edge.classes:
                if self._adj[target][source] == 1:
                    del self._adj[target][source]
                else:
                    self._adj[target][source] -= 1
        except ValueError:
            raise ValueError(
                f"Edge from {edge.data['source']} to {edge.data['target']} "
                "is not present in the graph."
            )

    def remove_edge_by_id(self, source_id, target_id):
        """
        Removes edge by the id specified.

        Parameters
        ----------
        source_id : numeric or string
        target_id : numeric or string
        """
        contains_edge = False
        edges = copy.copy(self.edges)

        for edge in edges:
            if (
                edge.data["source"] == source_id and edge.data["target"] == target_id
            ) or (
                "directed" not in edge.classes
                and edge.data["source"] == target_id
                and edge.data["target"] == source_id
            ):
                self.remove_edge(edge)
                contains_edge = True
        if not contains_edge:
            raise ValueError(
                f"Edge between {source_id} and {target_id} is not present in the graph."
            )

    def clear(self):
        """
        Remove all the nodes and edges from the graph.
        Parameters
        ----------
        self: cytoscape graph
        """
        self.nodes.clear()
        self.edges.clear()
        self._adj.clear()

    def add_graph_from_networkx(self, g, directed=None, multiple_edges=None):
        """
        Converts a NetworkX graph in to a Cytoscape graph.

        Parameters
        ----------
        g : networkx graph
            receives a generic NetworkX graph. more info in
            https://networkx.github.io/documentation/
        directed : bool
            If true all edges will be given directed as class if
            they do not already have it. Equivalent to adding
            'directed' to the 'classes' attribute of edge.data for all edges
        """
        # override type infering if directed is provided by the user
        if isinstance(g, nx.DiGraph) and directed is None:
            directed = True
        # override type infering if multiple_edges is provided by the user
        if isinstance(g, nx.MultiGraph) and multiple_edges is None:
            multiple_edges = True

        node_list = list()
        for node, data in g.nodes(data=True):
            if issubclass(type(node), Node):
                node_instance = node
            else:
                node_instance = Node()
                _set_attributes(node_instance, data)
                if "id" not in data:
                    node_instance.data["id"] = str(node)
            node_list.append(node_instance)
        self.add_nodes(node_list)

        edge_list = list()
        for source, target, data in g.edges(data=True):
            edge_instance = Edge()

            if issubclass(type(source), Node):
                edge_instance.data["source"] = source.data["id"]
            else:
                edge_instance.data["source"] = str(source)

            if issubclass(type(target), Node):
                edge_instance.data["target"] = target.data["id"]
            else:
                edge_instance.data["target"] = str(target)

            _set_attributes(edge_instance, data)

            if directed and "directed" not in edge_instance.classes:
                edge_instance.classes += " directed "
            if multiple_edges and "multiple_edges" not in edge_instance.classes:
                edge_instance.classes += " multiple_edges "
            edge_list.append(edge_instance)
        self.add_edges(edge_list, directed, multiple_edges)

    def add_graph_from_json(self, json_file, directed=False, multiple_edges=False):
        """
        Converts a JSON Cytoscape graph in to a ipycytoscape graph.
        (This method only allows the conversion from a JSON that's already
        formatted as a Cytoscape graph).

        Parameters
        ----------
        json_file : dict or string
            If a dict is passed, it will be parsed as a JSON object,
            a file path (to the json graph file) can also be passed as a
            string, the file will be loaded it's content parsed as JSON an
            object.
        directed : bool
            If True all edges will be given 'directed' as a class if
            they do not already have it.
        """
        if path.isfile(str(json_file)):
            with open(json_file) as f:
                json_file = json.load(f)

        node_list = list()
        for node in json_file["nodes"]:
            node_instance = Node()
            _set_attributes(node_instance, node)
            node_list.append(node_instance)
        self.add_nodes(node_list)
        edge_list = list()
        if "edges" in json_file:
            for edge in json_file["edges"]:
                edge_instance = Edge()
                _set_attributes(edge_instance, edge)
                if directed and "directed" not in edge_instance.classes:
                    edge_instance.classes += " directed "
                if multiple_edges and "multiple_edges" not in edge_instance.classes:
                    edge_instance.classes += " multiple_edges "
                edge_list.append(edge_instance)
            self.add_edges(edge_list, directed, multiple_edges)

    def add_graph_from_df(
        self,
        df,
        groupby_cols,
        attribute_list=[],
        edges=tuple(),
        directed=False,
        multiple_edges=False,
    ):
        """
        Converts any Pandas DataFrame in to a Cytoscape graph.

        Parameters
        ----------
        df : pandas dataframe
        groupby_cols : list of str
            List of dataframe columns
        attribute_list : list of str
            List of dataframe columns
        edges : tuple of edges
            The first item is the source edge and the second is the target edge
        directed : bool
            If True all edges will be given 'directed' as a class if
            they do not already have it.
        """
        grouped = df.groupby(groupby_cols)
        group_nodes = {}
        for i, name in enumerate(grouped.groups):
            if not isinstance(name, tuple):
                name = (name,)
            group_nodes[name] = Node(data={"id": f"parent-{i}", "name": name})

        graph_nodes = []
        graph_edges = []
        for index, row in df.iterrows():
            parent = group_nodes[tuple(row[groupby_cols])]

            # Includes content to tips
            tip_content = ""
            for attribute in attribute_list:
                tip_content += f"{attribute}: {row[attribute]}\n"

            # Creates a list with all nodes adding them in the correct node parents
            graph_nodes.append(
                Node(
                    data={"id": index, "parent": parent.data["id"], "name": tip_content}
                )
            )

            if not all(edges):
                # Creates a list with all nodes adding them in the correct node parents
                graph_nodes.append(
                    Node(
                        data={
                            "id": index,
                            "parent": parent.data["id"],
                            "name": tip_content,
                        }
                    )
                )

                if directed:
                    classes = "directed "
                else:
                    classes = ""
                graph_edges.append(
                    Edge(
                        data={
                            "id": index,
                            "source": edges[0],
                            "target": edges[1],
                            "classes": classes,
                        }
                    )
                )

        # Adds group nodes and regular nodes to the graph object
        all_nodes = list(group_nodes.values()) + graph_nodes
        self.add_edges(graph_edges, directed, multiple_edges)
        self.add_nodes(all_nodes)

    def add_graph_from_neo4j(self, g):
        """
        Converts a py2neo Neo4j subgraph into a Cytoscape graph. It also adds
        a 'tooltip' node attribute to the Cytoscape graph if it is not present
        in the Neo4j subgraph. This attribute can be set as a tooltip by
        set_tooltip_source('tooltip'). The tooltip then displays the node
        properties from the Neo4j nodes.

        Parameters
        ----------
        g : py2neo Neo4j subgraph object
            See https://py2neo.org/v4/data.html#subgraph-objects
        """

        def convert_types_to_string(node_attributes):
            """
            Converts types not compatible with cytoscape to strings.

            Parameters
            ----------
            node_attributes : dictionary of node attributes
            """
            for k, v in node_attributes.items():
                try:
                    json.dumps(v)
                except TypeError:
                    node_attributes[k] = str(v)

            return node_attributes

        def get_node_labels_by_priority(g):
            """
            Returns a list of Neo4j node labels in priority order.
            If a Neo4j node has multiple labels, the most distinctive
            (least frequently occuring) label will appear first in this list.
            Example: five nodes have the labels (Person|Actor) and five nodes
            have the labels (Person|Director). In this case the Actor and Director
            labels have priority over the Person label.

            Parameters
            ----------
            g : py2neo Neo4j subgraph object
                See https://py2neo.org/v4/data.html#subgraph-objects
            """
            counts = dict()

            # This counts the number of instances that a node has a particular
            # label (a node can have multiple labels in Neo4j).
            # counts.get(label, 0) initializes the count with zero, and then
            # increments the value if more of the same labels are encountered.
            for node in g.nodes:
                for label in node.labels:
                    counts[label] = counts.get(label, 0) + 1

            return sorted(counts, key=counts.get)

        def create_tooltip(node_attributes, node_labels):
            """
            Returns a string of node labels and node attributes to be used as a tooltip.

            Parameters
            ----------
            node_attributes : dictionary of node attributes
            node_labels : list of node labels
            """
            labels = ",".join(label for label in node_labels)
            attributes = "\n".join(k + ":" + str(v) for k, v in node_attributes.items())
            return labels + "\n" + attributes

        # select labels to be displayed as node labels
        priority_labels = get_node_labels_by_priority(g)

        # convert Neo4j nodes to cytoscape nodes
        node_list = list()
        for node in g.nodes:
            node_attributes = dict(node)

            # convert Neo4j specific types to string
            node_attributes = convert_types_to_string(node_attributes)

            # create tooltip text string
            if "tooltip" not in node_attributes:
                tooltip_text = create_tooltip(node_attributes, node.labels)
                node_attributes["tooltip"] = tooltip_text

            # assign unique id to node
            node_attributes["id"] = node.identity

            # assign class label with the highest priority
            index = len(priority_labels)
            for label in node.labels:
                index = min(index, priority_labels.index(label))

            node_attributes["label"] = priority_labels[index]

            # create node
            node_instance = Node()
            _set_attributes(node_instance, node_attributes)
            node_list.append(node_instance)

        self.add_nodes(node_list)

        # convert Neo4j relationships to cytoscape edges
        edge_list = list()
        for rel in g.relationships:
            edge_instance = Edge()

            # create dictionaries of relationship
            rel_attributes = dict(rel)

            # convert Neo4j specific types to string
            rel_attributes = convert_types_to_string(rel_attributes)

            # assign name of the relationship
            if "name" not in rel_attributes:
                rel_attributes["name"] = rel.__class__.__name__

            # assign unique node ids
            edge_instance.data["source"] = rel.start_node.identity
            edge_instance.data["target"] = rel.end_node.identity
            _set_attributes(edge_instance, rel_attributes)

            edge_list.append(edge_instance)

        # Neo4j graphs are directed and may have multiple edges
        directed = True
        multiple_edges = True

        self.add_edges(edge_list, directed, multiple_edges)


class CytoscapeWidget(DOMWidget):
    """Implements the main Cytoscape Widget"""

    _model_name = Unicode("CytoscapeModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("CytoscapeView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    # interaction options
    min_zoom = CFloat(1e-50).tag(sync=True)
    max_zoom = CFloat(1e50).tag(sync=True)
    zooming_enabled = Bool(True).tag(sync=True)
    user_zooming_enabled = Bool(True).tag(sync=True)
    panning_enabled = Bool(True).tag(sync=True)
    user_panning_enabled = Bool(True).tag(sync=True)
    box_selection_enabled = Bool(False).tag(sync=True)
    selection_type = CaselessStrEnum(
        ["single", "additive"], default_value="single"
    ).tag(sync=True)
    touch_tap_threshold = Integer(8).tag(sync=True)
    desktop_tap_threshold = Integer(4).tag(sync=True)
    autolock = Bool(False).tag(sync=True)
    auto_ungrabify = Bool(False).tag(sync=True)
    auto_unselectify = Bool(True).tag(sync=True)

    # rendering options
    headless = Bool(False).tag(sync=True)
    style_enabled = Bool(True).tag(sync=True)
    hide_edges_on_viewport = Bool(False).tag(sync=True)
    texture_on_viewport = Bool(False).tag(sync=True)
    motion_blur = Bool(False).tag(sync=True)
    motion_blur_opacity = CFloat(0.2).tag(sync=True)
    wheel_sensitivity = CFloat(1).tag(sync=True)
    cytoscape_layout = Dict({"name": "cola"}).tag(sync=True)
    pixel_ratio = Union([Unicode(), CFloat()], default_value="auto").tag(sync=True)
    cytoscape_style = List(
        [
            {"selector": "node", "css": {"background-color": "#11479e"}},
            {"selector": "node:parent", "css": {"background-opacity": 0.333}},
            {
                "selector": "edge",
                "style": {
                    "width": 4,
                    "line-color": "#9dbaea",
                },
            },
            {
                "selector": "edge.directed",
                "style": {
                    "curve-style": "bezier",
                    "target-arrow-shape": "triangle",
                    "target-arrow-color": "#9dbaea",
                },
            },
            {
                "selector": "edge.multiple_edges",
                "style": {
                    "curve-style": "bezier",
                },
            },
        ]
    ).tag(sync=True)
    zoom = CFloat(2.0).tag(sync=True)
    rendered_position = Dict({"renderedPosition": {"x": 100, "y": 100}}).tag(sync=True)
    tooltip_source = Unicode("tooltip").tag(sync=True)
    _interaction_handlers = CytoInteractionDict({}).tag(
        sync=True, **interaction_serialization
    )

    graph = Instance(Graph, args=tuple()).tag(sync=True, **widget_serialization)

    def __init__(self, graph=None, **kwargs):
        """
        Initializes the graph widget.

        Parameters
        ----------
        graph: graph: string, dict, pandas.DataFrame, networkx.Graph,
               neo4j.Graph, Graph object, optional
               The graph to initialize with. Equivalent to calling the
               appropriate ``CytoscapeWidget.graph.add_graph_from_` method.
        """
        super().__init__(**kwargs)

        self.on_msg(self._handle_interaction)
        self.graph = Graph()

        if nx and isinstance(graph, nx.Graph):
            self.graph.add_graph_from_networkx(graph)
        elif isinstance(graph, (dict, str)):
            self.graph.add_graph_from_json(graph)
        elif pd and isinstance(graph, pd.DataFrame):
            self.graph.add_graph_from_df(graph, **kwargs)
        elif isinstance(graph, Graph):
            self.graph = graph
        elif py2neo and isinstance(graph, py2neo.Graph):
            self.graph.add_graph_from_neo4j(graph)

    # Make sure we have a callback dispatcher for this widget and event type;
    # since _interaction_handlers is synced with the frontend and changes to
    # mutable values don't automatically propagate, we need to explicitly set
    # the value of `_interaction_handlers` through the traitlet and allow the
    # serialized version to propagate to the frontend, where the client code
    # will add event handlers to the DOM graph.
    def on(self, widget_type, event_type, callback, remove=False):
        """
        Register a callback to execute when the user interacts with the graph.

        Parameters
        ----------
        widget_type : str
            Specify the widget type to monitor. Pick from:
            - %s
        event_type : str
            Specify the type of event to monitor. See documentation on these
            event types on the cytoscape documentation homepage,
            (https://js.cytoscape.org/#events/user-input-device-events). Pick
            from:
            - %s
        callback : func
            Callback to run in the kernel when the user has an `event_type`
            interaction with any element of type `widget_type`. `callback`
            will be called with one argument: the JSON-dictionary of the target
            the user interacted with (which includes a `data` key for the
            user-provided data in the node).
        remove : bool, optional
            Set to true to remove the callback from the list of callbacks.
        """
        if widget_type not in self._interaction_handlers:
            self._interaction_handlers = dict(
                [
                    *self._interaction_handlers.items(),
                    (widget_type, {event_type: CallbackDispatcher()}),
                ]
            )
        elif event_type not in self._interaction_handlers[widget_type]:
            self._interaction_handlers = dict(
                [
                    *(
                        (wt, v)
                        for wt, v in self._interaction_handlers.items()
                        if wt != widget_type
                    ),
                    (
                        widget_type,
                        dict(
                            [
                                *self._interaction_handlers[widget_type].items(),
                                (event_type, CallbackDispatcher()),
                            ]
                        ),
                    ),
                ]
            )
        self._interaction_handlers[widget_type][event_type].register_callback(
            callback, remove=remove
        )

    on.__doc__ = on.__doc__ % (
        "\n            - ".join(MONITORED_USER_TYPES),
        "\n            - ".join(MONITORED_USER_INTERACTIONS),
    )

    def _handle_interaction(self, _widget, content, _buffers):
        handlers = self._interaction_handlers
        if (
            ("widget" in content)
            and ("event" in content)
            and (content["widget"] in handlers)
            and (content["event"] in handlers[content["widget"]])
        ):
            handlers[content["widget"]][content["event"]](content["data"])

    def set_layout(self, **kwargs):
        """
        Sets the layout of the current object. Change the parameters individually.
        For extensive documentation on the different kinds of layout please refer
        to https://js.cytoscape.org/#layouts

        Parameters
        ----------
        name : str
            name of the layout, ex.: cola, grid.
        nodeSpacing : int
        edgeLengthVal : int
        padding : int
            adds padding to the whole graph in comparison to the Jupyter's cell
        **kwargs :
            All kwargs will be added to the dictionary of the layout.
        """
        dummy_dict = copy.deepcopy(self.cytoscape_layout)

        for key, value in kwargs.items():
            dummy_dict[key] = value

        self.cytoscape_layout = dummy_dict

    def get_layout(self):
        """
        Get the currently used layout.
        """
        return self.cytoscape_layout

    def relayout(self):
        """
        Cause the graph run the layout algorithm again.
        https://js.cytoscape.org/#cy.layout
        """
        self.send({"name": "layout"})

    def set_style(self, style):
        """
        Sets the layout of the current object. Change the parameters
        with a dictionary.

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

    def set_tooltip_source(self, source):
        """
        Parameters
        ----------
        source : string
            The key in data that will be used to populate the tooltip
        """
        self.tooltip_source = source
