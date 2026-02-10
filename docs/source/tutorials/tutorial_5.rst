Tutorial part 5 - tidier GUI
============================

In the previous tutorial, we completed our character count application.
In  this tutorial, we'll tidy up the display and look at some of the features
that a ``PanelDag`` gives us.

Dag documentation
^^^^^^^^^^^^^^^^^

The card at the top of the page documents the dag. The text is specified using
the ``doc`` parameter of ``PanelDag``. The first line is the (plain text) header;
the remaining text is the (Markdown) description.

Likewise, the ``Block`` class takes a ``doc`` parameter. If specified,
the doc text is displayed next to the "Continue" button.

Visibility
^^^^^^^^^^

The ``SingleCase`` and ``CharDistribution`` blocks do not require a
user interface. They each take input, perform an action, and provide output,
without any interaction.

In the ``__init__()``
method of your block, call ``super().__init__()`` and set the ``visible``
parameter to ``False``.

Block names
^^^^^^^^^^^

Block names are derived from the name of the class. In the ``__init__()``
method of your block, call ``super().__init__()`` and set the ``name``
parameter.

Widget labels and help
^^^^^^^^^^^^^^^^^^^^^^

The labels for the various widgets default to the names of the variables
(without their ``in_`` and ``out_`` prefixes.) This is not very useful.
Use the ``label`` and ``doc`` parameters for the ``param`` to provide
informative labels and help text. This also provides better documentation
when the help icon in the template sidebar is clicked.

Check input for validity
^^^^^^^^^^^^^^^^^^^^^^^^

By default, the "Continue" button is always enabled. We can cause it to be
enabled only when the input values are valid. For the ``ExternalInput`` block,
the input text in ``ExternalInput`` must be non-blank.

The "Continue" button reflects the boolean value ``self.is_input_valid_``.
(Note the trailing underscore.) Setting that value will enable or disable
the button.

Create a method (the name doesn't matter) that checks the validity of the inputs.
Use the ``@param.depends(..., watch=True)`` decorator to watch for changes to
the named variables. In the method, set ``self.is_input_valid_`` accordingly.

Override ``self.prepare()`` to call the "check validity" method. The
``self.prepare()`` method is called by the dag when the block is executed,
and before the dag pauses waiting for user input. By default, the block's
``self.prepare()`` method sets ``self.is_input_valid_`` to True.

Continue button
^^^^^^^^^^^^^^^

Instead of a generic "Continue" label, we change the label to "Count" to
tell the user what will happen when the button is pressed.

Case param
^^^^^^^^^^

Using a boolean flag to indicate upper or lower is not convenient. There is no
reason to make upper True and lower False, or vice versa. Instead, we'll change
this param to be a ``param.Selector``, with allowed values 'U' and 'L'. The default
widget for that is a drop-down Select menu, but since there are only two options,
we'll change that to a RadioBoxGroup.

.. note::

    To see this dag in action, run ``tutorials/tutorial_5a.py``.

    Click on the "Continue" button to see the dag in action.

Logo
^^^^

Add a logo to customise your app. The logo is 30 pixels high.
