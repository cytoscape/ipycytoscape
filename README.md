# ipycytoscape

[![Tests](https://github.com/cytoscape/ipycytoscape/actions/workflows/test.yml/badge.svg)](https://github.com/cytoscape/ipycytoscape/actions/workflows/test.yml) [![Documentation Status](https://readthedocs.org/projects/ipycytoscape/badge/?version=latest)](https://ipycytoscape.readthedocs.io/en/latest/?badge=latest) [![StackOverflow](https://img.shields.io/badge/stackoverflow--orange.svg)](https://stackoverflow.com/questions/tagged/ipycytoscape) [![Join the chat at https://gitter.im/QuantStack/Lobby](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/QuantStack/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A widget enabling interactive graph visualization with [cytoscape.js](https://js.cytoscape.org/) in JupyterLab and the Jupyter notebook.

Try it out using binder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cytoscape/ipycytoscape/HEAD?filepath=examples) or install and try out the [examples](examples).

![cytoscape screencast](https://user-images.githubusercontent.com/17600982/76328068-bbbbcf00-62e2-11ea-93ed-01ba392ac50c.gif)

#### Supports:

* Conversion from NetworkX see [example1](https://github.com/cytoscape/ipycytoscape/blob/master/examples/Test%20NetworkX%20methods.ipynb), [example2](https://github.com/cytoscape/ipycytoscape/blob/master/examples/NetworkX%20Example.ipynb)
* Conversion from Pandas DataFrame see [example](https://github.com/cytoscape/ipycytoscape/blob/master/examples/pandas.ipynb)
* Conversion from neo4j see [example](https://github.com/cytoscape/ipycytoscape/blob/master/examples/Neo4j_Example.ipynb)

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

### Pandas installation

You can install the Pandas dependencies for `ipycytoscape` with pip:

```
pip install pandas
```

Or conda-forge:

```
mamba install pandas
```

### Neo4j installation

You can install the neo4j dependencies for `ipycytoscape` with pip:

```
pip install -e ".[neo4j]"
```

Or conda-forge:
```
mamba install py2neo neotime
```

#### For jupyterlab 1.x or 2.x:

If you are using JupyterLab 1.x or 2.x then you will also need to install `nodejs` and the `jupyterlab-manager` extension. You can do this like so:

```bash
# installing nodejs
conda install -c conda-forge nodejs


# install jupyterlab-manager extension
jupyter labextension install @jupyter-widgets/jupyterlab-manager@2.0 --no-build

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
conda create -n ipycytoscape -c conda-forge jupyterlab nodejs>13 networkx
conda activate ipycytoscape

# clone repo
git clone https://github.com/cytoscape/ipycytoscape.git
cd ipycytoscape
```

### Install python package for development

This will `run npm install` and `npm run build`. 
This command will also install the test suite and the [docs](https://ipycytoscape.readthedocs.io/en/latest/) locally:

```
pip install jupyter_packaging==0.7.9
pip install -e ".[test, docs]"

jupyter labextension develop . --overwrite
```


Or for classic notebook, you can run:

```
jupyter nbextension install --sys-prefix --symlink --overwrite --py ipycytoscape
jupyter nbextension enable --sys-prefix --py ipycytoscape
```

Note that the `--symlink` flag doesn't work on Windows, so you will here have to run
the `install` command every time that you rebuild your extension. For certain installations
you might also need another flag instead of `--sys-prefix`, but we won't cover the meaning
of those flags here.

### How to see your changes

#### Typescript: 
To continuously monitor the project for changes and automatically trigger a rebuild, start watching the ipycytoscape code:
```bash
npm run watch
```
And in a separate terminal start JupyterLab normally:
```bash
jupyter lab
```
once the webpack rebuild finishes refresh the JupyterLab page to have your changes take effect.

#### Python:
If you make a change to the python code then you need to restart the notebook kernel to have it take effect.

### How to run tests locally

Install necessary dependencies with pip:

```
pip install -e ".[test]"
```

Or with mamba:

```
mamba -c conda-forge install networkx pandas nbval pytest
```

Or with conda:

```
conda -c conda-forge install networkx pandas nbval pytest
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

## Acknowledgements

The ipycytoscape project was started by [Mariana Meireles](https://github.com/marimeireles) at [QuantStack](https://quantstack.net). This initial development was funded as part of the [PLASMA](https://plasmabio.org) project, which is led by Claire Vandiedonck, Pierre Poulain, and Sandrine Caburet.

## License

We use a shared copyright model that enables all contributors to maintain the
copyright on their contributions.

This software is licensed under the BSD-3-Clause license. See the
[LICENSE](LICENSE) file for details.
