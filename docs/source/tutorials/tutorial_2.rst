Tutorial part 2 - an application
================================

In this tutorial, we'll continue building a simple application to count characters
in text.

The ``ExternalInput`` block now uses a short cut to specify it is an input block.
Rather than having to implement a custom ``__init__()``, we can just set
``wait_for_input = True`` as a class variable.

.. literalinclude :: /../../tutorials/tutorial_2a.py
   :language: python
   :linenos:
   :pyobject: ExternalInput

When we execute the dag, we don't pass a pre-defined text value.
Instead, when dag execution reaches ``ExternalInput``, execution pauses
for user input. Because we're in text mode, we use the Python ``input()``
builtin to get a string and set the upper-/lower- case flag.
We then continue executing the dag using ``dag.execute_after_input(b)``.

Previously, we let the dag execute, then manually printed the results. However,
itwould be better to include an output block in the dag.
Therefore, we'll create a ``Display`` block.

``Display`` doesn't actually do anything - it just provides the application
a way of displaying the result of the translation. The application could just
get the results from the output params of the ``CharDistribution`` block as it did
in the previous tutorial, but we want to keep "user input" and "user output"
blocks separate from "work" blocks. This will become useful in the next tutorial.

To add the Display block to the dag, we added some more param tuples.

.. literalinclude :: /../../tutorials/tutorial_2a.py
   :language: python
   :linenos:
   :start-at: __main__

Now we can build our new dag, run it, and see the result. Because we're running
in text mode, we still have to manually ask for inputs and set the relevant params.

.. note::

    To see this dag in action, run ``tutorials/tutorial_2a.py``.
