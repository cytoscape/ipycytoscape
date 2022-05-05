#!/usr/bin/env python

# Copyright (c) 2020, QuantStack, Mariana Meireles and ipycytoscape Contributors
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.

import os
from glob import glob
from os import path

from jupyter_packaging import (
    combine_commands,
    create_cmdclass,
    ensure_targets,
    get_version,
    install_npm,
)
from setuptools import find_packages, setup

# The name of the project
name = "ipycytoscape"

HERE = os.path.dirname(os.path.abspath(__file__))

# Get our version
version = get_version(path.join(name, "_version.py"))

nb_path = path.join(HERE, name, "nbextension", "static")
lab_path = path.join(HERE, name, "labextension")

# Representative files that should exist after a successful build
jstargets = [
    path.join(nb_path, "index.js"),
    path.join(HERE, "lib", "plugin.js"),
]

package_data_spec = {name: ["*"]}

data_files_spec = [
    ("share/jupyter/nbextensions/jupyter-cytoscape", nb_path, "**"),
    ("share/jupyter/labextensions/jupyter-cytoscape", lab_path, "**"),
    ("etc/jupyter/nbconfig/notebook.d", HERE, "jupyter-cytoscape.json"),
]


cmdclass = create_cmdclass(
    "jsdeps", package_data_spec=package_data_spec, data_files_spec=data_files_spec
)
cmdclass["jsdeps"] = combine_commands(
    install_npm(HERE, build_cmd="build:prod"),
    ensure_targets(jstargets),
)

# Read the contents of the README file on Pypi
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup_args = dict(
    name=name,
    description="A Cytoscape widget for Jupyter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    scripts=glob(path.join("scripts", "*")),
    cmdclass=cmdclass,
    packages=find_packages(),
    author="Mariana Meireles",
    author_email="mariana.meireles@quantstack.net",
    url="https://github.com/cytoscape/ipycytoscape",
    license="BSD",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "Widgets", "IPython"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Jupyter",
    ],
    include_package_data=True,
    install_requires=[
        "ipywidgets>=7.6.0",
        "spectate>=1.0.0",
    ],
    extras_require={
        "test": [
            "black==22.1.0",
            "flake8>=4.0.1",
            "flake8-typing-imports>=1.7.0",
            "nbclassic>=0.2.8",
            "nbval",
            "networkx",
            "pandas",
            "pre-commit",
            "pytest>4.6",
            "pytest-cov",
        ],
        "examples": [
            "pandas",
            "py2neo",
            "monotonic",
            # Any requirements for the examples to run
        ],
        "docs": [
            "sphinx",
            "sphinx_rtd_theme",
            "sphinx-autobuild>=2020.9.1",
            "jupyter-sphinx>=0.3.1",
            "sphinx-copybutton",
            "nbsphinx",
            "nbsphinx-link",
            "networkx",
            "pandas",
        ],
        "neo4j": [
            "py2neo",
            "monotonic",
        ],
    },
    entry_points={},
)

if __name__ == "__main__":
    setup(**setup_args)
