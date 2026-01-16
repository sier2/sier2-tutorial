Tutorial part 1 - Dag
=====================

In this tutorial, we'll start to build a simple application to transform text.
We'll see that simple blocks can be joined together to build
a more complex application.

A "dag" is a `directed acyclic graph <https://en.wikipedia.org/wiki/Directed_acyclic_graph>`_. Each connection in the graph has a direction,
so in the graph below, node ``a`` is connected to node ``b``,
but node ``b`` is not connected to node ``a``. In addition, starting at
any given node and following connections will never lead back to the starting node.

.. image:: Tred-G.svg.png
    :align: center

In particular, we build a graph by connecting blocks. More precisely,
blocks are connected by connecting output params to input params.
Rather than invent a clever name, we call a dag made up of connected blocks
a "dag".

Our example dag will contain three blocks.

* An "external input" block to provide data to the dag.
* A lowercase block, that converts text to lower case.
* A counting block, that counts each character in the text.

The module ``tutorial_1a.py`` contains the code for this example.

As we saw in the previous tutorial, a block is an instance of a class that
subclasses ``Block``, and uses at least one ``param`` for input and/or output.

First we'll look at the ``ExternalInput`` class. It has two params,
defined using the ``param`` library.
How do we know which are inputs and which are outputs?
Inputs start with in\_, outputs start with out\_.

``ExternalInput`` has an input param ``in_text`` and an output param ``out_text``.

.. literalinclude :: /../../tutorials/tutorial_1a.py
   :language: python
   :linenos:
   :pyobject: ExternalInput

Next, we'll look at the ``LowerCase`` class. It has an input string param
and an output string param.

.. literalinclude :: /../../tutorials/tutorial_1a.py
   :language: python
   :linenos:
   :pyobject: LowerCase

The third block ``CharDistribution`` has one input string param and two
output params, a string (a representation of a bar chart) and an integer
(the length of the input string).

.. literalinclude :: /../../tutorials/tutorial_1a.py
   :language: python
   :linenos:
   :pyobject: CharDistribution

The ``main()`` function creates an instance of each block, then creates a ``Dag`` and
connects the two blocks. The ``Dag.connect()`` method connects source blocks
to destination blocks. The ``Connection()`` arguments indicate
how the blocks are connected.

For a dag to execute, at least one output param must be set in a block.
The ``ExternalInput`` block will take the inputs to ``in_text``.
Typically, this would take input from a user, but we'll just provide some text
by setting the ``in_text`` param of ``external_input``.

Finally, we call ``dag.execute()`` to run the rest of the dag and see the outputs.

.. literalinclude :: /../../tutorials/tutorial_1a.py
   :language: python
   :linenos:
   :pyobject: main

The output resulting from this dag is:

.. code-block:: text

        Input length: 23
            5 *****
        t   5 *****
        a   3 ***
        e   2 **
        h   2 **
        .   1 *
        c   1 *
        m   1 *
        n   1 *
        o   1 *
        s   1 *
