# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'irsl_choreonoid'
copyright = '2023, IRSL-tut'
author = 'IRSL-tut'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
from recommonmark.parser import CommonMarkParser

extensions = [
    'recommonmark',
    'sphinx_markdown_tables',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',
]
autosummary_generate = True
templates_path = ['_templates']

source_parsers = {
    '.md': CommonMarkParser,
}
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'venv', 'README.md']

language = 'ja'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
souce_suffix = ['.rst', '.md']
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
