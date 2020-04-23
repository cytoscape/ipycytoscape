# ipycytoscape

[![Build Status](https://travis-ci.org/Quantstack/ipycytoscape.svg?branch=master)](https://travis-ci.org/Quantstack/ipycytoscape)

Python implementation of the graph visualization tool Cytoscape.

Try it out using binder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/QuantStack/ipycytoscape/stable?filepath=examples)

![cytoscape screencast](https://user-images.githubusercontent.com/17600982/76328068-bbbbcf00-62e2-11ea-93ed-01ba392ac50c.gif)

#### Supports:

* Conversion from NetworkX see [example](https://github.com/QuantStack/ipycytoscape/blob/master/examples/Test%20NetworkX%20methods.ipynb)
* Conversion from Pandas DataFrame see [example](https://github.com/QuantStack/ipycytoscape/blob/master/examples/DataFrame%20interaction.ipynb)

## Installation

With `conda`: (recommended)

```
conda install -c conda-forge ipycytoscape
```

With `pip`:

```bash
pip install ipycytoscape
```

#### For jupyterlab users:

There is an aditional step if you're using JupyterLab:

```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-cytoscape
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] ipycytoscape
```

## For a development installation:
**(requires npm)**

```bash
git clone https://github.com/QuantStack/ipycytoscape.git
cd ipycytoscape
```

It's recommended to create a conda environment:

```bash
conda create -n ipycytoscape -c conda-forge jupyterlab nodejs
conda activate ipycytoscape
```

Install and enable extension for `jupyter notebook` and `jupyter lab`:

```bash
python -m pip install -e .
npm install && npm run build
jupyter nbextension install --py --symlink --sys-prefix ipycytoscape
jupyter nbextension enable ipycytoscape --py --sys-prefix
jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-cytoscape
jupyter labextension install js
```

## License

We use a shared copyright model that enables all contributors to maintain the
copyright on their contributions.

This software is licensed under the BSD-3-Clause license. See the
[LICENSE](LICENSE) file for details.
