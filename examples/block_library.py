#

# An example of loading blocks from the block library to make a dag.
# Use
# $ python -m sier2 blocks
# to get a list of available blocks.
#

import random

from sier2 import Library, Dag, Connection

def main():
    n1 = random.randint(1, 100)
    n2 = random.randint(1, 100)
    print(f'Adding {n1} and {n2}.')

    cn_block = Library.get_block('sier2_tutorial.blocks.ConstantNumberBlock')
    a2_block = Library.get_block('sier2_tutorial.blocks.AddBlock')

    r1 = cn_block(n1)
    r2 = cn_block(n2)
    a2 = a2_block(name='adder')

    dag_a = Dag(doc='Example: dump dag', title='dump dag')
    dag_a.connect(r1, a2, Connection('out_constant', 'in_a'))
    dag_a.connect(r2, a2, Connection('out_constant', 'in_b'))

    # Prime the dag.
    #
    r1.prime()
    r2.prime()

    print('Run the dag')
    dag_a.execute()

    print(f'{r1.out_constant} + {r2.out_constant} = {a2.out_result}')

if __name__=='__main__':
    main()
