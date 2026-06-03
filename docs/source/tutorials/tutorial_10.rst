Tutorial part 10 - setting params
=================================

As we've seen, assigning a value to an ``out_`` param causes any blocks that the param
is connected to to (eventually) execute.

Consider this dag.

.. literalinclude:: /../../tutorials/tutorial_10a.py
   :language: python
   :linenos:

We execute the dag twice. What we want to happen is that the first block generates
a dictionary containing the key 1, which is displayed by the display block. When
executed again, the first block generates a dictionary with the key 2, which is then displayed.

However, when this dag executes:

.. code-block:: text

    ---- Execute the dag.
    execute First00002: 1
    collection: {1: 'X'}

    ---- Execute the dag again.
    execute First00002: 2
    collection: {1: 'X', 2: 'XX'}

The first block executes, but the display block doesn't. And instead of a new dictionary
each time, the same dictionary is reused. What happened?

A block is only queued for execution when an ``out_`` param that is connected to it
is assigned a value. The first block never assigns a value to ``self.out_collection``;
it only mutates the default value. Therefore, the display block is never queued.

The solution is to create a local dictionary, mutate that, and assign it to
``self.out_collection``.

.. literalinclude:: /../../tutorials/tutorial_10b.py
   :language: python
   :linenos:

Now when the dag is executed twice:

.. code-block:: text

    ---- Execute the dag.
    execute First00002: 1
    collection: {1: 'X'}

    execute Display00005
    Key: 1, Value: X

    ---- Execute the dag again.
    execute First00002: 2
    collection: {2: 'XX'}

    execute Display00005
    Key: 2, Value: XX

Now the display block is executed, and the dictionary is reset each time.
