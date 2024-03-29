# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

# The full version, including alpha/beta/rc tags
from mplsignal._version import __version__

sys.path.insert(0, os.path.abspath('../mplsignal'))


# -- Project information -----------------------------------------------------

project = 'mplsignal'
copyright = '2022-2023, Oscar Gustafsson'
author = 'Oscar Gustafsson'

release = __version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'numpydoc',
    'matplotlib.sphinxext.plot_directive',
    "sphinx_copybutton",
    "sphinx_gallery.gen_gallery",
    "sphinx.ext.napoleon",
]

sphinx_gallery_conf = {
    "examples_dirs": "../examples",  # path to your example scripts
    "gallery_dirs": "examples",  # path to where to save gallery generated output
    "filename_pattern": "/.*",
    "ignore_pattern": "/_.*",  # https://www.debuggex.com/
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'matplotlib': ('https://matplotlib.org/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_theme_options = {
    "light_logo": "mplsignal_logo.svg",
    "dark_logo": "mplsignal_logo_dark.svg",
}
autosummary_generate = False

# Uncomment to validate numpydoc
# numpydoc_validation_checks = {"all"}
