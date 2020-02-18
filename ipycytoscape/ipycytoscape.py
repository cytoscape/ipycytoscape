#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mariana Meireles.
# Distributed under the terms of the Modified BSD License.

"""
Graph visualization in Jupyter.
"""

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
    style = List([
                    {
                        'selector': 'node',
                        'css': {
                            'background-color': '#f92411'
                        }
                    },

                    {
                        'selector': 'edge',
                        'css': {
                            'line-color': '#f92411'
                        }
                    }
                ],).tag(sync=True)
    value = Dict({"test":5}).tag(sync=True)
