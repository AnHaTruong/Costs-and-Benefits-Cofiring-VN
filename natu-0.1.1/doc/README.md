Documentation for natu
----------------------

This is the top-level build directory for natu documention.  All of the
documentation is written using [Sphinx], a [Python] documentation system based
on [reST].  This folder contains:
  - [make.py](make.py) - Script to clean, build, and release the HTML docs
  - [conf.py](conf.py) - The [Sphinx] configuration
  - [index.rst](index.rst) - The top-level source document
  - [loadres.rst](loadres.rst) - Documentation for the **loadres** script
  - other \*.rst files - Placeholders to automatically generate the documentation
  - [extra](extra) - Additional files added to the base folder of the built
    documentation
  - [_static](_static) - Folder of static files used by [Sphinx]
  - [_templates](_templates) - Folder of HTML templates used by [Sphinx]
  - [.natu.pws](.natu.pws) - [aspell] dictionary of additional natu words used
    in spellchecking the HTML documentation

To build the documentation, install [Sphinx] and run the following command in
this directory:

    python make.py html

The top file of the results will be build/html/index.html.


[Sphinx]: http://sphinx-doc.org/
[Python]: http://www.python.org
[reST]: http://docutils.sourceforge.net/rst.html
[aspell]: http://aspell.net/
