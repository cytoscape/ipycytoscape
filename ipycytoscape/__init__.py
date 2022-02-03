#!/usr/bin/env python

# Copyright (c) 2020, QuantStack, Mariana Meireles and ipycytoscape Contributors
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.

from ._version import __version__, version_info
from .cytoscape import (
    MONITORED_USER_INTERACTIONS,
    MONITORED_USER_TYPES,
    CytoscapeWidget,
    Edge,
    Graph,
    Node,
)
from .nbextension import _jupyter_nbextension_paths

npm_pkg_name = "jupyter-cytoscape"


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": npm_pkg_name}]
