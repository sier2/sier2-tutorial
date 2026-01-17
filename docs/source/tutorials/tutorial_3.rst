Tutorial part 3 - GUI
=====================

In this tutorial, we'll convert the dag in the previous tutorial to use a GUI.

We'll be using `Panel <https://panel.holoviz.org/>`_, an open-source Python library
designed to streamline the development of robust tools, dashboards,
and complex applications entirely within Python.

We import the blocks we created in the prevous tutorial. We'll be using them
as-is, with no changes.

.. literalinclude :: /../../tutorials/tutorial_3a.py
   :language: python
   :linenos:
   :end-before: __main__

To add a panel GUI to your block, you don't need to do anything.
When you start a dag using Panel, the dag will automatically turn your
`in_` params into Panel widgets.

As before, we create the blocks and use a dag to connect them, except
instead of using ``Dag``, we use ``PanelDag``. Then instead of calling
``dag.execute()``, we call ``dag.show()``.

.. literalinclude :: /../../tutorials/tutorial_3a.py
   :language: python
   :linenos:
   :start-at: __main__

.. note::

    To see this dag in action, run ``tutorials/tutorial_3a.py``.

With minimal effort (``PanelDag`` instead of ``Dag``, ``show()`` instead of
``execute()``), we have a GUI version of our dag. The GUI automatically
displays the input params, and adds a "Continue" button where required
(due to the ``wait_for_input`` in ``ExternalInput``).
We could make it tidier, but it works as-is.

In the previous tutorial, we had to do our own input and restart the
dag execution. The ``PanelDag`` does that for us. Enter some text and select
upper or lower case, then click the "Continue" button; the ``Display`` block
will display the result.

How does ``panelDag`` know what order to display the blocks in?
A dag is a directed acyclic graph: a graph
where the edges between nodes have directions, and there are no cycles
(aka loops). A consequence of this is that a dag has at least one "start"
block (a block with no inputs) and at least one "end" block (a block with
no outputs). The blocks are displayed in *topological* sort order: blocks
closer to the start are shown above blocks further from the start.
