Tutorial part 4 - custom panel
==============================

In this tutorial, we'll replace the ``Display`` in the previous tutorial
with a more user-friendly display.

As in the previous tutorial, we'll import the first three blocks as-is.

.. literalinclude :: /../../tutorials/tutorial_4a.py
   :language: python
   :linenos:
   :end-before: class

We create a new block called ``DisplayCountBars`` that contains a method
called ``_panel__()``. When ``panel`` wants to display an object,
this is the method that it calls to get something to display.

The ``execute()`` method builds a barchart from the inputs and inserts it
into a HoloViews pane.

.. literalinclude :: /../../tutorials/tutorial_4a.py
   :language: python
   :linenos:
   :pyobject: DisplayCountBars

As before, we create the blocks and use a ``PanelDag`` to connect them,
then call ``dag.show()``.

.. literalinclude :: /../../tutorials/tutorial_3a.py
   :language: python
   :linenos:
   :start-at: __main__

.. note::

    To see this dag in action, run ``tutorials/tutorial_4a.py``.

    Click on the "Continue" button to see the dag in action.
