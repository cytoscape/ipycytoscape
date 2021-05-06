#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function
from glob import glob
import os
from os import path

from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    ensure_python,
    get_version,
)

from setuptools import setup, find_packages


# The name of the project
name = "ipycytoscape"

HERE = os.path.dirname(os.path.abspath(__file__))

# Ensure a valid python version
ensure_python(">=3.4")

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
    install_npm(HERE, build_cmd="build"),
    ensure_targets(jstargets),
)

# Read the contents of the README file on Pypi
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup_args = dict(
    name=name,
    description="Python implementation of the graph visualization tool Cytoscape.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    scripts=glob(path.join("scripts", "*")),
    cmdclass=cmdclass,
    packages=find_packages(),
    author="Mariana Meireles",
    author_email="mariana.meireles@quantstack.net",
    url="https://github.com/Quantstack/ipycytoscape",
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
        "Framework :: Jupyter",
    ],
    include_package_data=True,
    install_requires=[
        "ipywidgets>=7.6.0",
        "spectate>=1.0.0",
        "networkx",
        "py2neo",
        "neotime",
    ],
    extras_require={
        "test": ["pytest>4.6", "pytest-cov", "nbval", "pandas"],
        "examples": [
            "pandas"
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
    },
    entry_points={},
)

if __name__ == "__main__":
    setup(**setup_args)
