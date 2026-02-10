#

# Demonstrate input validation in a block executing in a dag.
#
from sier2 import Block, BlockValidateError, Dag, Connection
import param

class Prime(Block):
    """Output parameter to give the dag something to do."""

    out_p = param.Number()

    def execute(self):
        self.out_p = -1

class Validate(Block):
    """A validation example."""

    in_p = param.Number()
    out_p = param.Number()

    def __init__(self):
        super().__init__(wait_for_input=True)

    def prepare(self):
        if self.in_p<1:
            raise BlockValidateError(block_name=self.name, message='Input must be 1 or greater')

    def execute(self):
        self.out_p = self.in_p

def main():
    p = Prime()
    v = Validate()
    dag = Dag(doc='validate-dag', title='Validate')
    dag.connect(p, v, Connection('out_p', 'in_p'))

    dag.execute()

if __name__=='__main__':
    main()
