#

# Demonstrate dumping and loading dags.
#

from pprint import pprint
import random

from sier2 import Library, Block, Dag, Connection
# from sier2.provided import AddBlock, ConstantNumberBlock

def main():
    n1 = random.randint(1, 100)
    n2 = random.randint(1, 100)

    cn_block = Library.get_block('sier2_tutorial.blocks:ConstantNumberBlock')
    a2_block = Library.get_block('sier2_tutorial.blocks:AddBlock')

    r1 = cn_block(n1)
    r2 = cn_block(n2)
    a2 = a2_block(name='adder')

    # Remember the names of the two number blocks.
    #
    r1name = r1.name
    r2name = r2.name
    agname = a2.name

    dag_a = Dag(doc='Example: dump dag', title='dump dag')
    dag_a.connect(r1, a2, Connection('out_constant', 'in_a'))
    dag_a.connect(r2, a2, Connection('out_constant', 'in_b'))

    print('Run the dag')
    r1.prime()
    r2.prime()
    dag_a.execute()
    result_a = a2.out_result
    print(f'{result_a=}')

    dump_a = dag_a.dump()
    print('\nThe dumped dag:')
    pprint(dump_a)

    dag_b = Library.load_dag(dump_a)

    # Dumping the new dag should give us the same dump as the original dag.
    #
    dump_b = dag_b.dump()
    print(f'\ndump_b == dump_a: {dump_b==dump_a}')

    # We now have a new dag that is the same as the old dag.
    # If we had a GUI, the user could now provide input to run the dag.
    # Instead, we'll do it manually. Technically this is cheating, because
    # we shouldn't know what the blocks are, but since we hard-coded them,
    # we can do it.
    #
    print('\nRun the dag loaded from the dump.')

    # The number blocks will have the same names as in the original dag.
    #
    r1 = dag_b.block_by_name(r1name)
    r2 = dag_b.block_by_name(r2name)
    ag = dag_b.block_by_name(agname)

    r1.prime()
    r2.prime()
    dag_b.execute()
    result_b = a2.out_result

    print(f'Results should be the same: {result_a=}, {result_b=}')

if __name__=='__main__':
    main()
