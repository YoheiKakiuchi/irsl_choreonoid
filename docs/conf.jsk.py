import sys
import os
import shlex
import subprocess
import xml.etree.ElementTree
from recommonmark.parser import CommonMarkParser
extensions = [
    'recommonmark',
    'sphinx_markdown_tables',
    'sphinx.ext.mathjax',
]
templates_path = ['_templates']
source_parsers = {
    '.md': CommonMarkParser,
}
source_suffix = ['.rst', '.md']
master_doc = 'index'
project = u'jsk_recognition'
copyright = u'2015, JSK Lab'
author = u'Ryohei Ueda, Kei Okada, Youhei Kakiuchi'
language = 'en'
this_dir = os.path.dirname(os.path.abspath(__file__))
package_xml = os.path.join(this_dir, '../jsk_recognition/package.xml')
xml_tree = xml.etree.ElementTree.parse(package_xml).getroot()
version = xml_tree.find('version').text
release = version
exclude_patterns = ['_build', 'venv', 'README.md']
this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, this_dir)
import add_img_tables_to_index
if not subprocess.check_output(['git', 'diff']):
    add_img_tables_to_index.main(exclude_patterns)
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = 'sphinx_rtd_theme'
htmlhelp_basename = 'jsk_recognitiondoc'
latex_elements = {
    # Additional stuff for the LaTeX preamble.
    'preamble': "".join((
        "\\usepackage[utf8]{inputenc}",
        # NO-BREAK SPACE
        '\DeclareUnicodeCharacter{00A0}{ }',
        # BOX DRAWINGS LIGHT VERTICAL AND RIGHT
        '\DeclareUnicodeCharacter{251C}{+}',
        # BOX DRAWINGS LIGHT UP AND RIGHT
        '\DeclareUnicodeCharacter{2514}{+}',
    )),
}
latex_documents = [
  (master_doc, 'jsk_recognition.tex', u'jsk\_recognition Documentation',
   author, 'manual'),
]
man_pages = [
    (master_doc, 'jsk_recognition', u'jsk_recognition Documentation',
     [author], 1)
]
texinfo_documents = [
  (master_doc, 'jsk_recognition', u'jsk_recognition Documentation',
   author, 'jsk_recognition', 'One line description of project.',
   'Miscellaneous'),
]
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']
