from sier2 import Block, InputBlock
import param
import random

class ProvideInteger(InputBlock):
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

    # Use the output of the RandomInteger block as the input of
    # the AddOne block. We'll use the callable shortcut.
    #
    pi = ProvideInteger()
    a1 = AddOne()
    for _ in range(4):
        # Execute the RandomInteger block to get the output dictionary.
        #
        pi.out_int = random.randint(1, 20)
        pi_result = pi()

        # Retrieve the out_int value.
        #
        ri_out = pi_result['out_int']

        # Execute the AddOne block, passing in the input value.
        #
        a1_result = a1(in_a=ri_out)

        # Retrieve the out_a value.
        #
        a1_out = a1_result['out_a']

        print(f'Random number is {ri_out:2}, add one is {a1_out:2}')
