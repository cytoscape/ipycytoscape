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
from traitlets import Dict, Unicode, Bool, List
from ._frontend import module_name, module_version

"""TODO: Remove this after this is somewhat done"""
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class CytoscapeWidget(DOMWidget):
    """TODO: Add docstring here
    """

    _model_name = Unicode('CytoscapeModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('CytoscapeView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    autounselectify = Bool(True).tag(sync=True)
    boxSelectionEnabled = Bool(False).tag(sync=True)
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
    changeFlag = Bool(False).tag(sync=True)
    zoom = Dict({'level': 2.0, 'renderedPosition': { 'x': 100, 'y': 100 }}).tag(sync=True)

    """
    Graphs need to be copied because of https://github.com/ipython/traitlets/issues/495
    """

    # def set_graph(self):
    #     d = {'nodes': [], 'edges': []}

    #     for node in self.elements['nodes']:
    #         logging.debug(node)
    #         d['nodes'].append({'data': {'id': node['data']['id'], 'label': node['data']['label']}})
    #     for edge in self.elements['edges']:
    #         logging.debug(edge)
    #         d['edges'].append({'data': {'source': edge['data']['source'],'target': edge['data']['target']}})

    #     return d

    # def display_networkx_graph(self, graph):
    #     """TODO: Implement labels, weights, etc"""
    #     aux_dict = {'nodes': [], 'edges': []}
    #     for node in graph.nodes():
    #         aux_dict['nodes'].append({'data': {'id': node, 'label': ''}})
    #     for edge in graph.edges():
    #         aux_dict['edges'].append({'data': {'source': edge[0], 'targett': edge[1]}})
    #     logging.debug(aux_dict)
    #     self.elements = aux_dict

    def add_node(self, node_id, label=""):
        new_dict = copy.deepcopy(self.elements)
        new_dict['nodes'].append({'data': {'id': node_id, 'label': label}})
        self.elements = new_dict

    def add_edge(self, edge_source, edge_target):
        new_dict = copy.deepcopy(self.elements)
        new_dict['edges'].append({'data': {'source': edge_source,'target': edge_target}})
        self.elements = new_dict

    def remove_node(self, id):
        pass

    def remove_edge(self, source, target):
        pass

    def set_layout(self, layout):
        self.cytoscape_layout = Dict({'name': cytoscape_layout}).tag(sync=True)

    def set_style(self, stylesheet):
        self.cytoscape_style = stylesheet
