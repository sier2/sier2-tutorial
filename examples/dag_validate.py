#

# Demonstrate input validation in a block executing in a dag.
#
from sier2 import Block, BlockValidateError, Dag, Connection
import param

class Prime(Block):
    """Output parameter to prime the dag."""

    out_p = param.Number()

class Validate(Block):
    """A validation example."""

    in_p = param.Number()

    def __init__(self):
        super().__init__(block_pause_execution=True)

    def prepare(self):
        if self.in_p<1:
            raise BlockValidateError(block_name=self.name, error='Input must be >= 1')

def main():
    p = Prime()
    v = Validate()
    dag = Dag(doc='validate-dag', title='Validate')
    dag.connect(p, v, Connection('out_p', 'in_p'))

    p.out_p = -1
    dag.execute()

if __name__=='__main__':
    main()
