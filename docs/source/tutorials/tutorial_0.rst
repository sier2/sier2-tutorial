Tutorial part 0 - Introduction
==============================

This is the first in a series of tutorials that explains blocks and dags,
and how to use them to build applications.

The tutorial Python scripts are in the ``tutorials`` directory.
Open each tutorial script in your favourite editor so you can refer
to the code while reading the tutorial.

Blocks
------

A block is a unit of Python code that performs a specific action:
adding two numbers, querying a database, or displaying a bar chart.

Blocks pass input and output values using a Python library called ``param``
(see `the param web site <https://param.holoviz.org>`_). You don't need to
know the details of how to use params - blocks take care of the complexity.
You just need to know how to declare params as inputs or outputs.

Blocks are implemented as Python classes. A block:

* must be a subclass of ``Block``;
* must have at least one input or output param - input param names must start with ``in_``, output param names must start with ``out_``;
* may have an ``execute()`` method.

The module ``tutorial_0a.py`` contains a simple block that adds one to its input.

.. code-block:: python
    
    from sier2 import Block
    import param

    class AddOne(Block):
        """A block that adds one to its input."""

        in_a = param.Integer()
        out_a = param.Integer()

        def execute(self):
            self.out_a = self.in_a + 1

The class ``AddOne`` is a subclass of ``Block``. It has two params:
an input param called ``in_a`` and an output param called ``out_a``.
Both of these params are declared as type ``param.Integer``; we'll see why this
matters below.

The ``execute()`` method defines what the block does. In this case, the output
param (``self.out_a``) is set to the input param plus one (``self.in_a + 1``).

We can test our block by creating an instance of ``AddOne``, setting the
value of the input param, calling ``execute()``, and printing the value of
the output param.

.. code-block:: python

    a1_block = AddOne()

    # Prime the block with some input, then execute it.
    #
    a1_block.in_a = 3
    a1_block.execute()

The output is:

.. code-block:: python

    a1_block.out_a=4

Blocks provide a short cut that does the same thing. A ``Block`` instance
is callable: calling the instance with keyword parameters corresponding
to the input params will set the input params, call ``execute()``, and return
a dictionary containing the output params and their values.

.. code-block:: python

    print(f'{a1_block(in_a=3)=}')

The output is:

.. code-block:: text

    {'out_a': 4}

.. note::

    To see this dag in action, run ``tutorials/tutorial_0a.py``.

Param types
-----------

An advantage of using ``param`` to define parameters is that they can be
specified with types. If you attempt to assign a non-integer value
to an input parameter, ``param`` will raise an error.

.. code-block:: python

    a1_block.in_a = 'x'

.. code-block:: text

    ValueError: Integer parameter 'AddOne.in_a' must be an integer, not <class 'str'>.

See `Parameter types <https://param.holoviz.org/user_guide/Parameter_Types.html>`_
for a list of pre-defined parameter types.

Input blocks:
--------------

Blocks can be made to wait for user or program input. Typically we'd see this
in a GUI (which we'll get to later).