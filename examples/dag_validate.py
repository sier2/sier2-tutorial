#

# Demonstrate input validation in a block executing in a dag.
#
from sier2 import Block, InputBlock, BlockValidateError, Dag, Connection
import param

class Prime(Block):
    """Output parameter to prime the dag."""

    out_p = param.Number()

class Validate(InputBlock):
    """A validation example."""

    in_p = param.Number()

    def prepare(self):
        if self.in_p<1:
            raise BlockValidateError('Input must be >= 1')

def main():
    p = Prime()
    v = Validate()
    dag = Dag(doc='validate-dag', title='Validate')
    dag.connect(p, v, Connection('out_p', 'in_p'))

    p.out_p = -1
    dag.execute()

if __name__=='__main__':
    main()
