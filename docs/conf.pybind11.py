extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]
autosummary_generate = True
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
project = "python_example"
copyright = "2016, Sylvain Corlay"
author = "Sylvain Corlay"
version = "0.0.1"
release = "0.0.1"
language = None
exclude_patterns = ["_build"]
pygments_style = "sphinx"
todo_include_todos = False
html_theme = "alabaster"
html_static_path = ["_static"]
htmlhelp_basename = "python_exampledoc"
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #'preamble': '',
    # Latex figure (float) alignment
    #'figure_align': 'htbp',
}
latex_documents = [
    (
        master_doc,
        "python_example.tex",
        "python_example Documentation",
        "Sylvain Corlay",
        "manual",
    ),
]
man_pages = [
    (master_doc, "python_example", "python_example Documentation", [author], 1)
]
texinfo_documents = [
    (
        master_doc,
        "python_example",
        "python_example Documentation",
        author,
        "python_example",
        "One line description of project.",
        "Miscellaneous",
    ),
]
intersphinx_mapping = {"https://docs.python.org/": None}
