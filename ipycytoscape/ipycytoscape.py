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

from ipywidgets import DOMWidget
from traitlets import Dict, Unicode, Bool, List, Float
from ._frontend import module_name, module_version

"""TODO: Remove this after this is somewhat done"""
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class CytoscapeWidget(DOMWidget):
    """
    Implements the main Cytoscape Widget
    """

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
    elements = Dict({'nodes': [], 'edges': []}).tag(sync=True)
    zoom = Float(2.0).tag(sync=True)
    rendered_position = Dict({'renderedPosition': { 'x': 100, 'y': 100 }}).tag(sync=True)

    """
    Graphs need to be copied because of https://github.com/ipython/traitlets/issues/495
    """
    def complete_graph(self, g):
        """
        Converts a NetworkX graph in to a Cytoscape graph.
        Parameters
        ----------
        g: nx graph
            receives a generic NetworkX graph. more info in
            https://networkx.github.io/documentation/
        """
        d = copy.deepcopy(self.elements)
        for node in g.nodes():
            d['nodes'].append({'data': {'id': node, 'label': ""}})
            logging.debug(node)
        for edge in g.edges():
            d['edges'].append({'data': {'source': edge[0],'target': edge[1]}})
        self.elements = d

    def add_node(self, node_id, label="", parent=""):
        d = copy.deepcopy(self.elements)
        d['nodes'].append({'data': {'id': node_id, 'label': label}})
        self.elements = d

    def add_edge(self, edge_source, edge_target):
        d = copy.deepcopy(self.elements)
        d['edges'].append({'data': {'source': edge_source,'target': edge_target}})
        self.elements = d

    """
    TODO: Implement remove node and edges. Not sure how useful this will be since
    we can use all of the NetworkX functions. Also, I'd have to implement a
    generalist template that would deal with all the kinds of graphs and NetX
    already does it. Don't think this is worthwhile. 
    """
    def remove_node(self):
        pass

    def remove_edge(self, source, target):
        pass

    def set_layout(self, name='', nodeSpacing='', edgeLengthVal='',
                    animate='', randomize='', maxSimulationTime=''):
        """
        Sets the layout of the current object.
        Parameters
        ----------
        name: str
            name of the layout, ex.: cola, grid.
        """
        self.cytoscape_layout = {'name': name, 'nodeSpacing': nodeSpacing,
                                'edgeLengthVal': edgeLengthVal,
                                'animate': animate, 'randomize': randomize,
                                'maxSimulationTime': randomize}

    def get_layout(self):
        """
        Gets the layout of the current object.
        """
        return self.cytoscape_layout

    def set_style(self, stylesheet):
        """
        Sets the layout of the current object.
        Parameters
        ----------
        stylesheet: dict
            adds a complete stylesheet to the graph see https://js.cytoscape.org
            for examples
        """
        self.cytoscape_style = stylesheet

    def get_style(self):
        """
        Gets the style of the current object.
        """
        return self.cytoscape_style

