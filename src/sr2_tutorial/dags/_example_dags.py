from sier2 import Dag, Connection, Library

import param

def example_add_dag():
    """A dag that adds two random bnumbers.

    The result is provided by the AddBlock named ``result`` in out_result.
    """
    rn_block = Library.get_block('sier2_tutorial.blocks:RandomNumberBlock')
    add_block = Library.get_block('sier2_tutorial.blocks:AddBlock')
    rnga = rn_block()
    rngb = rn_block()
    add = add_block(name='result')

    dag = Dag(doc='Demonstrate adding random numbers', site='Example', title='Addition')
    dag.connect(rnga, add, Connection('out_n', 'in_a'))
    dag.connect(rngb, add, Connection('out_n', 'in_b'))

    rnga.prime()
    rngb.prime(100)

    return dag
