
.. _installation:

Installation
============


To get started with ipycytoscape, install with pip::

    pip install ipycytoscape

or with conda/`mamba <https://github.com/TheSnakePit/mamba>`_::

    conda install -c conda-forge ipycytoscape
    # or with mamba
    mamba install -c conda-forge ipycytoscape


.. _jlab-install-instructions:

JupyterLab Installation
-----------------------

In order to install the JupyterLab extension jupyter-cytoscape, you will first need to install nodejs,
you can install it with conda by doing

.. code-block:: bash
    
    conda install -c conda-forge nodejs

The ``jupyter-cytoscape`` labextension should have been automatically installed for you when you installed
the Python package, but you still need to install the JupyterLab widget manager:

.. code-block:: bash

    jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build

    # if you already installed the manager you still to run jupyter lab build
    jupyter lab build



Old version of Jupyter notebook
-------------------------------
If you installed via pip, and use Juptyer Notebook with a version < 5.3, you will also have to
install / configure the front-end extension as well. If you are using classic
notebook (as opposed to Jupyterlab), run::

    jupyter nbextension install [--sys-prefix / --user / --system] --py ipycytoscape

    jupyter nbextension enable [--sys-prefix / --user / --system] --py ipycytoscape

with the `appropriate flag`_. 


If you are installing using conda, these commands should be unnecessary, but If
you need to run them the commands should be the same (just make sure you choose the
``--sys-prefix`` flag).


.. links

.. _`appropriate flag`: https://jupyter-notebook.readthedocs.io/en/stable/extending/frontend_extensions.html#installing-and-enabling-extensions
