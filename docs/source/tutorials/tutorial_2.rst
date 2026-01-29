Tutorial part 2 - an application
================================

In this tutorial, we'll continue building a simple application to count characters
in text.

Previously, we used the ``ExternalInput`` block to get user input.
However, rather than the block accepting input, we gave it some value beforehand.
In this tutorial, the block will pause execution of the dag to get input,
after which we continue dag execution.

.. literalinclude :: /../../tutorials/tutorial_2a.py
   :language: python
   :linenos:
   :pyobject: ExternalInput

We've modified ``ExternalInput`` to wait for input by adding an ``__init__()``
method and passing ``wait_for_input=True`` to ``super().__init__()``.

When we execute the dag, we don't pass a pre-defined text value.
Instead, when dag execution reaches ``ExternalInput``, execution pauses
for user input. because we're in text mode, we use the Python ``input()``
builtin to get a string and set the upper-/lower- case flag.
We then continue executing the dag using ``dag.execute_after_input(b)``.

Therefore, we'll create a ``Display`` block. Like the ``ExternalInput`` block,
``Display`` doesn't actually do anything - it just provides the application
a way of displaying the result of the translation. The application could just
get the results from the output params of the final block as it did
in the previous tutorial, but we want to keep "user input" and "user output"
blocks separate from "work" blocks. This will become useful in the next tutorial.

To add the Display block to the dag, we've used ``Connections`` and specified
a dictionary mapping output params to input params.

.. literalinclude :: /../../tutorials/tutorial_2a.py
   :language: python
   :linenos:
   :start-at: __main__

Now we can build our new dag, run it, and see the result.

.. note::

    To see this dag in action, run ``tutorials/tutorial_2a.py``.
