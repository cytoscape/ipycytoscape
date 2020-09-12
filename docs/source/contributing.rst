============
Contributing
============

Thanks for thinking of a way to help improve this library! Remember that contributions come in all
shapes and sizes beyond writing bug fixes: Contributing to documentation, opening new `issues <https://github.com/quantstack/ipycytoscape/issues>`_ for bugs, asking for clarification 
on things you find unclear, and requesting new features, are all super valuable contributions. 

Code Improvements
-----------------

All development for this library happens on Github at `ipycytoscape <https://github.com/quantstack/ipycytoscape>`_.

Seeing your changes
^^^^^^^^^^^^^^^^^^^

If you are working in a Jupyter Notebook, then in order to see your code changes you will need to either:

* Restart the Kernel every time you make a change to the code.
* **Or:** Make the function reload from the source file every time you run it by using `autoreload <https://ipython.readthedocs.io/en/stable/config/extensions/autoreload.html>`_.

.. code-block:: python

    %load_ext autoreload
    %autoreload 2

    from ipycytoscape import ....

Working with Git
^^^^^^^^^^^^^^^^

Using Git/Github can confusing (https://xkcd.com/1597/) so if you're new to Git, you may find
it helpful to use a program like `Github Desktop <desktop.github.com>`_ and to follow
a `guide <https://github.com/firstcontributions/first-contributions#first-contributions>`_. 

Also feel free to ask for help/advice on the relevant Github `issue <https://github.com/quantstack/ipycytoscape/issues>`_
or in the `Gitter chat <https://gitter.im/QuantStack/Lobby>`_.

Documentation
-------------

Following changes to the source files, you can view recent adjustments by building the documentation.

1. Make sure you have installed the requirements for building the documentation:

.. code-block:: bash

    cd ipycytoscape
    pip install -e.[docs]

2. Run the following commands:

.. code-block:: bash

    cd docs
    make html

If you open the ``build/html/index.html`` file in your browser you should now be able to see the rendered documentation.

Autobuild the documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Alternatively, you can use `sphinx-autobuild <https://github.com/GaretJax/sphinx-autobuild>`_ to continuously watch the documentation for changes and rebuild it for you.
Sphinx-autobuild will be installed automatically by the above ``pip`` command, and we've added it to the ``Makefile``. All you need to do is:

.. code-block:: bash

    cd docs
    make watch

In a few seconds your web browser should open up the documentation. Now whenever you save a source ``rst`` file
the documentation will automatically regenerate and the webpage will refresh for you! However, if you are writing a notebook
that is included in the documentation via ``nblink`` then you will need to manually rebuild to capture the changes to that file.
