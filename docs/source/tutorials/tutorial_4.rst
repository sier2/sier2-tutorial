Tutorial part 4 - themed application
====================================

In this tutorial, we'll use the blocks we built in the previous tutorial
to create a themed block application. We'll import them and build a dag.

Remember that in the previous tutorial, we made ``UserInput``
an :class:`sier2.InputBlock`. This has three effects.

* When the block is displayed, it has a "Continue" button added. When selected, it calls ``dag.execute()``.
* When the dag executes, it will stop executing when it reaches an ``InputBlock``. This allows the user to provide input, and continue executing the dag (by pressing the "Continue" button).
* If the the block has pending input, the block's ``prepare()`` method will be called before stopping.

Note that when a panel dag is first displayed, it is not executed, so an
``InputBlock`` must be part of the dag.

This time, we'll use the :class:`sier2.panel.PanelDag` class to display the dag.
A ``PanelDag`` is just like a normal "text-only" ``Dag``, but it adds the
necessary plumbing to provide a graphical user interface using the ``panel``
library.

``PanelDag`` first extracts the blocks from the dag in sorted order (see below);
each block is wrapped in a ``panel`` ``Card``, and the cards are displayed in
a column. All of this is displayed in a ``panel`` template.

* The card titles display the block names and a status indicator.
* The sidebar displays a visualisation of the dag, and a stop / unstop switch.

What does "sorted order" mean? A dag is a directed acyclic graph: a graph
where the edges between nodes have directions, and there are no cycles
(aka loops). A consequence of this is that a dag has at least one "start"
block (a block with no inputs) and at least one "end" block (a block with
no outputs). The blocks are displayed in *topological* sort order: blocks
closer to the start are shown above blocks further from the start.

.. note::

    To see this dag in action, run ``tutorials/tutorial_4a.py``.

    Click on the "Continue" button to see the dag in action.

An obvious disadvantage of importing block classes from another module is
that we have to be in the correct directory in order for the imports to work.
