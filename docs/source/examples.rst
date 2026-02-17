Examples
========

The ``examples`` and ``examples-panel`` directories provide examples
of various aspects of blocks and dags.

Textual Examples
----------------

add_numbers
^^^^^^^^^^^

A dag containing two input blocks connecting to a single execution block.

barchart
^^^^^^^^

A dag containing a query block, a grouping block, and a barchart drawing block.

dag_stop_unstop
^^^^^^^^^^^^^^^

Dag execution can be stopped and unstopped.

if_else_pause
^^^^^^^^^^^^^

An if - then - else block, causing only one of two downstream blocks to be executed.

pause
^^^^^

Demonstrate what happens when an input block is executed.

raise_exception
^^^^^^^^^^^^^^^

Demonstrates what happens when a block raises an exception.

simple_dag
^^^^^^^^^^

A simple dag.

validate
^^^^^^^^

Demonstrate validating inputs.

Panel examples
--------------

banner
^^^^^^

Demonstrate adding a top and bottom banner.

bars
^^^^

Passing a ``pandas`` dataframe to blocks that use ``HoloViews`` to display a chart.

block_logging.py
^^^^^^^^^^^^^^^^

Demonstrate logging from a block to the sidebar. Also, when there are multiple
head blocks in a dag, only one of them is executed at a time.

block_visibility
^^^^^^^^^^^^^^^^

Blocks can be made non-visible in the GUI.

dagless
^^^^^^^

Blocks without a dag; the use of ``self.is_input_valid_`` to enable the "Continue"
button in a card.

default
^^^^^^^

Allow ``PanelDag`` to build a default panel, and incorporate it into our own
custom panel. THe same block is used an an input block and execution block.

display
^^^^^^^

Demonstrates the ability to adjust the display of a block
using the `display_options` parameter. A `param.ListSelector`
displays differently depending on how `display_options` is defined.

fan
^^^

Demonstrate that the dag chart in the app's sidebar has a consistent ordering.
However, the order of execution of the blocks is still indeterminate.

if_else
^^^^^^^

An if - then - else block, causing only one of two downstream blocks to be executed.
The dag chart shows which branch is taken.

labels
^^^^^^

Shows how params are displayed using Panel.

panel-or-text
^^^^^^^^^^^^^

Demonstrates that a dag can be run in textual context and panel context
with out changing the dag code.

stop-unstop
^^^^^^^^^^^

Stopping and unstopping a dag in panel (`dag.stop()` and `dag.unstop()`).

tree
^^^^

Show off a binary tree chart.
