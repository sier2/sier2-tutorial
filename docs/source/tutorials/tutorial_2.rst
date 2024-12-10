Tutorial part 2 - an application
================================

In this tutorial, we'll continue building a simple application to translate text.

Previously, we used an ``ExternalInput`` block to prime the dag.
However, we extracted the result directly from the ``InvertVowels`` instance.

This is fine in a short Python script, but in an application, particularly
a GUI-based application, we want the result to end up somewhere that the user
can see it.

Therefore, we'll create a ``Display`` block. Like the ``ExternalInput`` block,
``Display`` doesn't actually do anything - it just provides the application
a way of getting the result of the translation. The application could just
get the transformed text from the output param of the final block as it did
in the previous tutorial, but we want to keep "user input" and "user output"
blocks separate from "work" blocks. This will become useful in the next tutorial.

We'll also simplify the dag slightly by combining the previous ``InvertLetters`` and
``InvertVowels`` blocks into a single ``Invert`` block.

Now we can build our new dag, run it, and see the result.

The output (when ``L`` is passed in) is:

.. code-block:: text

    Input text:
    Hello world.

    Output text:
    hEllo worlD.

.. note::

    To see this dag in action, run ``tutorials/tutorial_2a.py``.
