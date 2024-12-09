# Configuration file for the Sphinx documentation builder.

# Path setup
import os
import sys
sys.path.insert(0, os.path.abspath('C:/Users/Chaves Galo/improvemp final/ImproveMP/ImproveMP'))
import ImproveMP.main

# -- Project information

project = 'ImproveMP'
copyright = '2024, Cauã Schuch, Eduardo Gadelha, Pedro Bueno, Luisa Belentani'
author = 'Cauã Schuch, Eduardo Gadelha, Pedro Bueno e Luisa Belentani'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'