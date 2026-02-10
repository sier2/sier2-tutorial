from sier2 import Block, Dag, Connection
import param

# Demonstrate an if-else branch.
#
# The ``IfEvenElseOdd`` block is connected to two output blocks by two different
# output params. Only one of the output params is updated, so only the block
# connected via that param will execute next.

class IfEvenElseOdd(Block):
    """Demonstrate an if-else branch.

    This block has one integer input and two integer outputs, one for even inputs
    and one for odd outputs.

    Because this is an input block, execution pauses after ``prepare()`` runs
    to get input from the user. When execution resumes at ``execute()``,
    either ``out_even`` or ``out_odd`` is set depending on the value of ``in_value``.
    """

    in_value = param.Integer()
    out_even = param.Integer()
    out_odd = param.Integer()

    def __init__(self, name):
        super().__init__(name=name, wait_for_input=True)

    def prepare(self):
        """Use prepare to emulate an input widget."""

        print(f'{self.name} prepare() for input')

    def execute(self):
        if self.in_value%2==0:
            self.out_even = self.in_value
        else:
            self.out_odd = self.in_value

class Notify(Block):
    """Display a message."""

    in_value = param.Integer()

    def __init__(self, *, name, msg):
        super().__init__(name=name)
        self.msg = msg

    def execute(self):
        print(f'In block {self.name}: value {self.in_value} is {self.msg}')

if_else = IfEvenElseOdd('IfElse')
is_even = Notify(name='EvenBlock', msg='even')
is_odd = Notify(name='OddBlock', msg='odd')

dag = Dag(doc='Example: run a branch depending on a value', title='run a branch depending on a value')
dag.connect(if_else, is_even,
    Connection('out_even', 'in_value')
)
dag.connect(if_else, is_odd,
    Connection('out_odd', 'in_value')
)

input_block = dag.execute()
assert input_block is if_else

i = int(input('Enter an integer: '))
input_block.in_value = i

print('Restart\n')
dag.execute_after_input(input_block)
