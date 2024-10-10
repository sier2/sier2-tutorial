from sier2 import Block, Dag, Connection
import param
import random

class ProvideInteger(Block):
    """Provide an integer output.

    Note that there is no execute() method; this is a user-input block.
    """

    out_int = param.Integer()

class AddOne(Block):
    """A block that adds one to its input."""

    in_a = param.Integer()
    out_a = param.Integer()

    def execute(self):
        self.out_a = self.in_a + 1

if __name__=='__main__':
    random.seed(12)

    # Build a dag to do the work for us.
    #
    pi = ProvideInteger()
    a1 = AddOne()

    dag = Dag(title='Tutorial 0', doc='Demonstrate building and executing a dag')
    dag.connect(pi, a1, Connection('out_int', 'in_a'))

    for _ in range(4):
        pi.out_int = random.randint(1, 20)
        dag.execute()

        ri_out = pi.out_int
        a1_out = a1.out_a
        print(f'Random number is {ri_out:2}, add one is {a1_out:2}')
