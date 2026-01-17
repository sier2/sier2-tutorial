Tutorial part 5 - block library
===============================

In this tutorial, we find out how to use the block library.

In the previous tutorial, we saw that because we imported another module,
we had to be in the correct directory. There's nothing unusual about that,
it's just how Python works.

This tutorial will show how to use
plugins and the block library to run a dag from anywhere.

First, let's see how the library works.

.. note::

    To see this dag in action, run ``tutorials/tutorial_5a.py``.

We import the block classes as before, but this time we add the classes
to the block library. Each block class has a unique string key, made up of
the module path and class name.

If there was a mechanism that pre-loaded blocks into the library,
we wouldn't need to import them, or add them to the library -
we could just get them from the library and use them.

Run this command at a command prompt.

.. code:: bash

    python -m sier2 blocks

THis will display ``Block`` classes that have been made available to
the ``sier2`` library. Depending on what else is installed, the may be no blocks.
In particular, ``sier2_tutorial`` should not be there.

Now run the command below.

.. code:: bash

    python -m pip install --user .

This will install a package called ``sier2-tutorial``. The blocks in the
package are accessible by the block library. To see this, after installing
the package, run the ``blocks`` command again.

.. code:: bash

    python -m sier2 blocks

The output should be similar to this. (There will probably be other things present.)

.. code:: text

    In sier2_tutorial v0.1.1
      sier2_tutorial.blocks.UserInput: A text area and flag for input.
      sier2_tutorial.blocks.Invert: Transform text.
      sier2_tutorial.blocks.Display: Display text.

This is a list of ``Block`` classes that the library has discovered.

Now we can use the blocks in the ``sier2_tutorial`` library without importing them,
and without having to be in any specific directory. We can just use
``Library.get_block()`` and let the library figure out how to give it to us.

.. note::

    To see this dag in action, run ``tutorials/tutorial_5b.py``.

That was nice, but we still had to build the dag manually. Fortunately, we can also use the library to retrieve dags.