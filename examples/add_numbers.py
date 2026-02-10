#

# This demonstrates that two blocks can provide inputs to a single block.
#
# - NumberBlock outputs a number.
# - AddBlock takes outputs from two instances of NumberBlock and adds them.
#
# AddBlock must allow for either or both of the inputs being None, and only
# continue if both inputs are valid.
#

import random

from sier2 import Block, Dag, Connection
import param

class NumberBlock(Block):
    """Produce a random number."""

    in_n = param.Integer(
        label='An integer',
        doc='An input number',
        default=None
    )
    out_n = param.Integer(
        label='An integer',
        doc='An output number',
        default=None
    )

    def execute(self):
        self.out_n = self.in_n

class AddBlock(Block):
    """Add two numbers.

    The action does not happen if either of the inputs is None.
    """

    in_a = param.Integer(label='First integer', default=None)
    in_b = param.Integer(label='Second integer', default=None)
    out_result = param.Integer(label='Result')

    def execute(self):
        print(f'Action {self.__class__.__name__} {self.in_a=} {self.in_b=}')

        # If some args aren't set, don't do anything.
        #
        if any(arg is None for arg in (self.in_a, self.in_b)):
            print('  Not all args set; ducking out.')
            return

        self.out_result = self.in_a + self.in_b

def main():
    """Pretend to be a block manager."""

    def setup(b: Block):
        r = random.randint(1, 100)
        print(f'{b.name} input is {r}')
        b.in_n = r

    nba = NumberBlock(name='source-of-a')
    nbb = NumberBlock(name='source-of-b')
    add_block = AddBlock()

    dag = Dag(doc='Example: add numbers', title='add numbers')
    dag.connect(nba, add_block, Connection('out_n', 'in_a'))
    dag.connect(nbb, add_block, Connection('out_n', 'in_b'))

    print(f'\nSet block {nba}')
    setup(nba)

    print(f'\nSet block {nbb}')
    setup(nbb)

    print()
    dag.execute()

    print(f'Result: {add_block.out_result}')

if __name__=='__main__':
    main()
