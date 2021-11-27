ipycytoscape
============

Version: |release|

Visualize graphs using `Cytoscape.js <https://js.cytoscape.org/>`_ in a Jupyter Notebook. You
can either create graphs using the ipycytoscape API or create them from:

- `NetworkX <https://networkx.github.io/>`_
- JSON
- `Pandas <https://pandas.pydata.org/>`_ Dataframes


Quickstart
----------

To get started with ipycytoscape, install with pip::

    pip install ipycytoscape

or with conda/`mamba <https://github.com/TheSnakePit/mamba>`_::

    conda install -c conda-forge ipycytoscape
    # or with mamba
    mamba install -c conda-forge ipycytoscape

If you are using JupyterLab 1.x or 2.x you will also need to follow the instructions in :ref:`jlab-install-instructions`.

Simple Example
--------------

.. jupyter-execute::

   from ipycytoscape import CytoscapeWidget
   import networkx as nx
   G = nx.complete_graph(5)
   cyto = CytoscapeWidget()
   cyto.graph.add_graph_from_networkx(G)
   display(cyto)

joseberlines_ created a series of blog posts explaining key points on the functioning of ipycytoscape:

Learning and visualising Graphs with ipycytoscape Part_1_

The series of notebook examples "Ipycytoscape from Scratch" found on this repository maps to these blog posts.

Contents
--------

.. toctree::
   :maxdepth: 2

   installing

.. toctree::
   :maxdepth: 2
   :caption: Graph Creation

   examples/graph-init 
   examples/networkx
   examples/json
   examples/pandas


.. toctree::
   :maxdepth: 2
   :caption: Customization and Styling

   examples/node-text
   examples/labels

.. toctree::
   :maxdepth: 2
   :caption: Advanced Usage

   examples/interaction

.. toctree::
   :maxdepth: 2
   :caption: Development

   develop-install
   contributing


.. links

.. _`Jupyter widgets`: https://jupyter.org/widgets.html

.. _`notebook`: https://jupyter-notebook.readthedocs.io/en/latest/

.. _`joseberlines`: https://github.com/joseberlines/

.. _`Part_1`: https://joseberlines.medium.com/learning-and-visualising-graphs-with-ipycytoscape-1ca150f24933
