Tutorial part 7 - exporting blocks and dags
===========================================

In the previous couple of tutorials, we used blocks and dags that are provided
by the ``sier2_tutorial`` package. How does that work?

The ``sier2`` library uses the Python plugin mechanism described at
https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#using-package-metadata. We use the ``sier2_tutorial`` package as an example.

``pyproject.toml``
------------------

The package's ``pyproject.toml`` contains this section.

.. code-block:: text

    [tool.poetry.plugins."sier2.library"]
    export = "sier2_tutorial.shelf"

The ``"sier2.library"`` is the group name for this plugin. The ``sier2`` ``Library``
looks up packages using this name.

``sier2_tutorial.shelf`` is the package with the ``sier2_tutorial`` library that
contains the export functions. There are two functions.

* ``blocks()`` returns a list of keys corresponding to ``Block`` classes, and their descriptions.
* ``dags()`` returns a list of keys corrsponding to functions that return ``Dag`` instances, and their descriptions.

A couple of important things about the keys.

Key == import name
------------------------

The key is used by the library to import a ``Block`` class or a ``Dag`` function,
so if a key is ``sier2_tutorial.blocks.Display``, it must be possible
to ``from sier2_tutorial.blocks import Display``.

No introspection
----------------

When exposing a block or a dag to the library, it is tempting to use introspection to
create the list of keys. If you do this, then the modules containing your blocks
will be executed, which can potentially take a long time due to library imports.
(For example, importing pandas can be quite slow.) Since every block and dag
is discovered, not using introspection is quicker for everyone.

To see how this is done, look at the source code for
``sier2_tutorial.shelf.__init__.py``.
