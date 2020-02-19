#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mariana Meireles.
# Distributed under the terms of the Modified BSD License.

"""
Graph visualization in Jupyter.
"""

import networkx as nx
import matplotlib.pyplot as plt

from ipywidgets import DOMWidget
from traitlets import Dict, Unicode, Bool, List
from ._frontend import module_name, module_version


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
    layout = Dict({'name': 'cola'}).tag(sync=True)
    style = List([{
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
    value = Dict().tag(sync=True)

    nx_graph = nx.Graph()

    """
    Graphs need to be copied because of https://github.com/ipython/traitlets/issues/495
    """
    def add_node(self, id, label=""):
        self.nx_graph.add_node(id, key=label)
        dummy_graph = self.value
        dummy_graph['nodes'].append({"data": {"id": id, "label": label}})
        self.value = dummy_graph

    def add_edge(self, source, target):
        self.nx_graph.add_edge(source, target)
        dummy_graph = self.value
        dummy_graph['edges'].append({"data": {"source": source,"target": target}})
        self.value = dummy_graph

    def set_layout(self, layout):
        self.layout = Dict({'name': layout})

    def set_style(self, stylesheet):
        self.style = stylesheet

