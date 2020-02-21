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

    def complete_graph(self, g):
        #trying not to do deepcopies here
        #idk why it only works if I deepcopy this here, cause I created the 
        #exact same obj, this: Dict({'nodes': [], 'edges': []}).tag(sync=True) doesn't work
        #not sure what this self.elements has
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

    def remove_node(self, id):
        pass

    def remove_edge(self, source, target):
        pass

    def set_layout(self, layout):
        self.cytoscape_layout = Dict({'name': cytoscape_layout}).tag(sync=True)

    def set_style(self, stylesheet):
        self.cytoscape_style = stylesheet
