Tutorial part 1 - Dag
=====================

In this tutorial, we'll start to build a simple application to count
characters in text. We'll see that simple blocks can be joined together to build
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
* A lower- or upper- case block, that converts text to lower case.
* A counting block, that counts each character in the text.

The module ``tutorial_1a.py`` contains the code for this example.

As we saw in the previous tutorial, a block is an instance of a class that
subclasses ``Block``, and uses at least one ``param`` for input and/or output.

First we'll look at the ``ExternalInput`` class. It has two params,
defined using the ``param`` library.
How do we know which are inputs and which are outputs?
Inputs start with in\_, outputs start with out\_.

``ExternalInput`` has two input params ``in_text`` and ``in_upper``, and two
matching output params ``out_text`` and ``out_upper``.

.. literalinclude :: /../../tutorials/tutorial_1a.py
   :language: python
   :linenos:
   :pyobject: ExternalInput

The ``SingleCase`` class has an input string param (the string to be upper or
lower cased), a boolean input param, and an output string param.

.. literalinclude :: /../../tutorials/tutorial_1a.py
   :language: python
   :linenos:
   :pyobject: SingleCase

The ``CharDistribution`` block has one input string param and three
output params:
- out_len: the length of the input text
- out_counter: a dictionary mapping characters to their counts
- out_bars: a bar chart drawn using asterisks

.. literalinclude :: /../../tutorials/tutorial_1a.py
   :language: python
   :linenos:
   :pyobject: CharDistribution

We create an instance of each block, then create a ``Dag`` and
connect the two blocks. The ``Dag.connect()`` method connects source blocks
to destination blocks. The ``Connection()`` arguments indicate
how the blocks are connected; each ``Connection()`` connects an output param
in one block to an input param in another block.

The ``ExternalInput`` block will take the inputs to ``in_text``.
Typically, this would take input from a user, but for now, we'll just
provide some text by setting the ``in_text`` param of ``external_input``
before we execute the dag.

Finally, we call ``dag.execute()`` to run the dag and see the outputs.
The dag will sort the blocks according to their connection; the ``ExternalInput``
output params are connected to the ``SingleCase`` input params, so
``ExternalInput`` is run before ``SingleCase``.

.. literalinclude :: /../../tutorials/tutorial_1a.py
   :language: python
   :linenos:
   :start-at: __main__

The ``out_len`` and ``out_bars`` values resulting from this dag are:

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
