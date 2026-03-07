# Configuration file for the Sphinx documentation builder.

project = 'NetworkSampler'
copyright = '2021-2026, Emiliano del Gobbo'
author = 'Emiliano del Gobbo'

# Indicates the Package is in the parent directory for autodoc
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from networksampler import __version__
release = __version__

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
autodoc_warningiserror = True