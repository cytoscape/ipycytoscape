# ipycytoscape

[![Build Status](https://travis-ci.com/Quantstack/ipycytoscape.svg?branch=master)](https://travis-ci.com/Quantstack/ipycytoscape) [![Documentation Status](https://readthedocs.org/projects/ipycytoscape/badge/?version=latest)](https://ipycytoscape.readthedocs.io/en/latest/?badge=latest) [![Join the chat at https://gitter.im/QuantStack/Lobby](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/QuantStack/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A widget enabling interactive graph visualization with [cytoscape.js](https://js.cytoscape.org/) in JupyterLab and the Jupyter notebook.

Try it out using binder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/QuantStack/ipycytoscape/stable?filepath=examples) or install and try out the [examples](examples).

![cytoscape screencast](https://user-images.githubusercontent.com/17600982/76328068-bbbbcf00-62e2-11ea-93ed-01ba392ac50c.gif)

#### Supports:

* Conversion from NetworkX see [example1](https://github.com/QuantStack/ipycytoscape/blob/master/examples/Test%20NetworkX%20methods.ipynb), [example2](https://github.com/QuantStack/ipycytoscape/blob/master/examples/NetworkX%20Example.ipynb)
* Conversion from Pandas DataFrame see [example](https://github.com/QuantStack/ipycytoscape/blob/master/examples/pandas.ipynb)

## Installation

With `mamba`:

```
mamba install -c conda-forge ipycytoscape
```

With `conda`:

```
conda install -c conda-forge ipycytoscape
```

With `pip`:

```bash
pip install ipycytoscape
```

#### For jupyterlab users:

If you are using JupyterLab 1.x or 2.x then you will also need to install `nodejs` and the `jupyterlab-manager` extension. You can do this like so:

```bash
# installing nodejs
conda install -c conda-forge nodejs


# install jupyterlab-manager extension
jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build

# if you have previously installed the manager you still to run jupyter lab build
jupyter lab build
```

### For Jupyter Notebook 5.2 and earlier

You may also need to manually enable the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] ipycytoscape
```

## For a development installation:

**(requires npm)**

While not required, we recommend creating a conda environment to work in:
```bash
conda create -n ipycytoscape -c conda-forge jupyterlab nodejs networkx
conda activate ipycytoscape

# clone repo
git clone https://github.com/QuantStack/ipycytoscape.git
cd ipycytoscape

# Install python package for development, runs npm install and npm run build
pip install -e .
```

When developing ipycytoscape, you need to manually enable the extension with the
notebook / lab frontend. For lab, this is done by the command:

```
# install jupyterlab-manager and this extension
jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build
jupyter labextension install .
```

For classic notebook, you can run:

```
jupyter nbextension install --sys-prefix --symlink --overwrite --py ipycytoscape
jupyter nbextension enable --sys-prefix --py ipycytoscape
```

Note that the `--symlink` flag doesn't work on Windows, so you will here have to run
the `install` command every time that you rebuild your extension. For certain installations
you might also need another flag instead of `--sys-prefix`, but we won't cover the meaning
of those flags here.

You need to install and build `npm` packages:

```
npm install && npm run build
```

Every time you change your typescript code it's necessary to build it again:

```
npm run build
```

It's possible to see your changes in real time, more about it in the [How to see your changes](https://github.com/QuantStack/ipycytoscape#how-to-see-your-changes) session.

### How to see your changes

#### Typescript: 
To continuously monitor the project for changes and automatically trigger a rebuild, start Jupyter in watch mode:
```bash
jupyter lab --watch
```
And in a separate session, begin watching the source directory for changes:
```bash
npm run watch
```

#### Python:
If you make a change to the python code then you need to restart the notebook kernel to have it take effect.

### How to run tests locally

Install necessary dependencies with pip:

```
pip install -e .[test]
```

Or with mamba:

```
mamba -c conda-forge install networkx pandas matplotlib nbval pytest
```

Or with conda:

```
conda -c conda-forge install networkx pandas matplotlib nbval pytest
```

#### And to run it:

```
pytest
```

### How to build the docs

`cd docs`

Install dependencies:

`conda env update --file doc_environment.yml`

And build them: 

`make html`

## License

We use a shared copyright model that enables all contributors to maintain the
copyright on their contributions.

This software is licensed under the BSD-3-Clause license. See the
[LICENSE](LICENSE) file for details.
