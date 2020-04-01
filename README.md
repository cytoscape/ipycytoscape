# ipycytoscape

[![Build Status](https://travis-ci.org/Quantstack/ipycytoscape.svg?branch=master)](https://travis-ci.org/Quantstack/ipycytoscape)
[![codecov](https://codecov.io/gh/Quantstack/ipycytoscape/branch/master/graph/badge.svg)](https://codecov.io/gh/Quantstack/ipycytoscape)

Python implementation of the graph visualization tool Cytoscape.

Try it out using binder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/QuantStack/ipycytoscape/stable?filepath=examples)

![cytoscape screencast](https://user-images.githubusercontent.com/17600982/76328068-bbbbcf00-62e2-11ea-93ed-01ba392ac50c.gif)

Offers full support to NetworkX lib. Just follow the example under `/examples/Test NetworkX methods.ipynb`.

## Installation

With conda: (recommended)

```
conda install -c conda-forge ipycytoscape
```

With `pip`:

```bash
pip install ipycytoscape
```

Or if you use jupyterlab:

```bash
pip install ipycytoscape
jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-cytoscape
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] ipycytoscape
```

**For a development installation:** (requires npm)

```
$ git clone https://github.com/QuantStack/ipycytoscape.git
$ cd ipycytoscape
$ pip install -e .
$ jupyter nbextension install --py --symlink --sys-prefix ipycytoscape
$ jupyter nbextension enable --py --sys-prefix ipycytoscape
$ jupyter labextension install @jupyter-widgets/jupyterlab-manager
$ jupyter labextension install js
```

## License

We use a shared copyright model that enables all contributors to maintain the
copyright on their contributions.

This software is licensed under the BSD-3-Clause license. See the
[LICENSE](LICENSE) file for details.
