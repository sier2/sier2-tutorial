Tutorial part 7 - dag library
=============================

In this tutorial, we find out how to use the dag library to
run a pre-defined dag.

In the previous tutorial, we installed the ``sier2-tutorial`` package,
which defined some blocks we used in our dag. The package also contains
a pre-defined dag, which we can run directly without writing any Python code.

To see the dags that the dag library knows about, run the command below.

.. code:: bash

    python -m sier2 dags

The output should be similar to:

.. code:: text

    In sier2_tutorial v0.1.1
      sier2_tutorial.dags.transform_dag: Transformation app

This is a list of functions that return a dag. In this case, the ``transform_dag``
function is the same function used in the previous tutorials; the only difference is
that it is made available by the ``sier2_tutorial`` package.

To run the dag, we use the ``sier2`` ``run`` command, specifying the
name of the dag. We can just use the last part of the dag name; we only
need to use the full name if another library defines a dag called
``transform_dag``.

.. code:: bash

    python -m sier2 run transform_dag
