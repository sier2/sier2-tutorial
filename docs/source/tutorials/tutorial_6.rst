Tutorial part 6 - execution paths
=================================

In this tutorial, we'll look more closely at what causes blocks to be executed.

The ``IfEvenElseOdd`` block has two different outputs. Only one of the outputs is set,
depending on the input value being even or odd.

.. literalinclude:: /../../tutorials/tutorial_6a.py
   :language: python
   :linenos:
   :pyobject: IfEvenElseOdd

The ``Annotate`` block annotates the value by embedding it in a string.
The default value for ``in_value`` is ``None``.

.. literalinclude:: /../../tutorials/tutorial_6a.py
   :language: python
   :linenos:
   :pyobject: Annotate

The ``Display`` block displays the annotation.

.. literalinclude:: /../../tutorials/tutorial_6a.py
   :language: python
   :linenos:
   :pyobject: Display

Finally, we build the dag and execute it.

.. literalinclude:: /../../tutorials/tutorial_6a.py
   :language: python
   :linenos:
   :start-at: __main__

The dag has a diamond shape, but only one of the paths through ``even`` or ``odd`` is taken
when the dag executes. We can see this by printing the ``in_value`` for each of the
``even`` and ``odd`` blocks after the dag has executed.

.. code-block:: text

    $ python .\tutorial_6a.py
    Enter an integer: 1
    **** The number 1 is odd. ****

    note_even.in_value=None
    note_odd.in_value=1
    $ python .\tutorial_6a.py
    Enter an integer: 2
    **** The number 2 is even. ****

    note_even.in_value=2
    note_odd.in_value=None

When the user input is 1, ``even.in_value`` still has its default value, showing
that the ``even`` block has not executed. Likewise, when the user input is 2,
``odd.in_value`` still has its default value, showing that the ``odd`` block
has not executed. How does that work?

The dag keeps track of the connections between ``out_`` params and ``in_`` params.
When an ``out_`` param's value is set in ``execute()``, the dag looks up the blocks
containing the ``in_`` params that the ``out_`` param is connected to, and adds
those blocks to an internal run queue.

When ``execute()`` ends, the dag takes the first block from the queue (if there is one),
sets the ``in_`` params to their new values, and executes that block.

In the dag above, the ``ifelse`` block only sets one of the two ``out_`` params;
therefore, only one of the ``even`` or ``odd`` blocks will execute after the ``ifelse``
block.

In particular, even though the display block has two input params, only one param
being set is sufficient to cause the block to be executed. The block does not wait for
all of the input params to be set.

If you'd like to reinforce this concept, modify the ``Annotate`` block to print
something when it executes, and see what prints when the dag runs.
