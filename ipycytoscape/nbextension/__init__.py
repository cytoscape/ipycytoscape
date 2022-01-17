#!/usr/bin/env python

# Copyright (c) 2020, QuantStack, Mariana Meireles and ipycytoscape Contributors
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.


def _jupyter_nbextension_paths():
    return [
        {
            "section": "notebook",
            "src": "nbextension/static",
            "dest": "jupyter-cytoscape",
            "require": "jupyter-cytoscape/extension",
        }
    ]
