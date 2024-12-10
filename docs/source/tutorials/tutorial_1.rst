Tutorial part 1 - Dag
=====================

In this tutorial, we'll start to build a simple application to transform text.
We'll see that simple blocks can be joined together to build
a more complex application.

A "dag" is a `directed acyclic graph <https://en.wikipedia.org/wiki/Directed_acyclic_graph>`_. Each connection in the graph has a direction,
so in the graph below, node ``a`` is connected to node ``b``,
but node ``b`` is not connected to node ``a``. In addition, starting at
any given node and following connections will never lead back to that node.

.. image:: Tred-G.svg.png
    :align: center

In particular, we build a graph by connecting blocks. More precisely,
blocks are connected by connecting output params to input params.
Rather than invent a name, we call a dag made up of connected blocks
a "dag".

The dag will contain three blocks.

* An "external input" block to provide data to the dag;
* A text inverter block, that converts text to upper or lower case;
* A vowel inverter block, that converts vowels to upper or lower case;

We suggest that you create a new Python script file and follow along,
so you can see how blocks work, and how changes affect the dag.
If things go wrong, copies of the tutorial scripts are in the ``tutorials``
directory.

As we saw in the previous tutorial, a block is an instance of a class that
subclasses ``Block``, and uses at least one ``param`` for input and/or output.

First we'll look at the ``ExternalInput`` class. There are two parameters,
defined using the ``param`` library. How do we know which are inputs and
which are outputs? Inputs start with ``in_``, outputs start with ``out_``.

``ExternalInput`` has no inputs, and two outputs: a text parameter
containing text to be transformed, and a flag that changes the transformation.

(Below we'll set the values of the outputs manually from Python.
In later tutorials, we'll see how to accept user input via a GUI.)

Note that a ``Block`` class does not ask for user input.
This is because blocks do not take user input or produce user
output; it is up to the application using a block to get input from, and present
output to, users. The only input and output mechanism that blocks use is their
parameters.

The ``InvertLetters`` class has two input params (that correspond to
``ExternalInput``'s output params) and two output params. It also has an
``execute()`` method.
This method is called automatically by the dag after the input values have been set.
(For convenience, ``execute()`` prints its input params so we can see what the input
param values are.)

The ``InvertVowels`` class also has two input params, but only one output param.
It also has an ``execute()`` method.

The ``main()`` function creates an instance of each blocks, then creates a ``Dag`` and
connects the three blocks. The ``Dag.connect()`` method connects source blocks
to destination blocks. The ``Connection()`` arguments indicate
how the blocks are connected.

* ``out_text`` (in the ``ei`` block) is connected to ``in_text`` (in the ``il`` block)
* ``out_flag`` (in the ``ei`` block) is connected to ``in_flag`` (in the ``il`` block)

Similar connections are used to connect the ``il`` and ``iv`` blocks.

Now we can try running the dag. This where we find out why we need an
external input block.

For a dag to execute, at least one output param must be set in a block. If you comment
out setting ``ei.out_text`` and ``ei.out_flag`` before executing the dag,
an execption will be raised: ``sier2._block.BlockError: Nothing to execute``.

We need to prime the dag with some data (hence we can call "``ExternalInput``
a "primer" block). To do this, we assign values to the output params of ``ei``,
and call ``dag.execute()``. Finally, we print the output param of ``iv``.

To run ``tutorial_1a.py``, provide an extra argument, either ``L`` or ``U``,
to demonstrate what effect tha flag has.

The output resulting from this dag when ``L`` is passed is:

.. code-block:: text

    in execute: self.in_flag=False self.in_text='Hello world.'
    iv.out_text='hEllo worlD.'

.. note::

    To see this dag in action, run ``tutorials/tutorial_1a.py``.
