Sier2 Tutorial
==============

This repository contains tutorials for ``sier2``.

Before running the tutorials or examples, install the ``sier2-examples``
library by cd-ing to the root directory of the repository (containing
the ``pyproject.toml`` file) and using the command:

.. code-block:: powershell

    python -m pip install --user -e .

The ``examples`` directory contains plain-text examples of
``sier2`` blocks and dags.

The ``examples-panel`` directory contains Panel-based examples of
``sier2`` blocks and dags.

The ``examples-library`` directory contains examples of
``sier2`` blocks and dags that can be installed and reused.

Documentation
-------------

To build the tutorial documentation from the repository root directory:

.. code-block:: powershell

    docs/make html
