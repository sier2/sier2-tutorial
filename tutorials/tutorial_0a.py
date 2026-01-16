from sr2 import Block
import param

class AddOne(Block):
    """A block that adds one to its input."""

    in_a = param.Integer()
    out_a = param.Integer()

    def execute(self):
        self.out_a = self.in_a + 1

#1
a1_block = AddOne()

# Set the input value, then execute it.
#
a1_block.in_a = 1
a1_block.execute()
print(f'{a1_block.out_a=}')

# output: a1_block.out_a=2
#-

#2
# Use the short cut to call execute.
#
print(f'{a1_block(in_a=4)=}')

# output: a1_block(in_a=4)={'out_a': 5}
#-

#3
# Another way of using the short cut: using Python's kwargs.
#
arguments = {'in_a': 7}
print(f'{a1_block(**arguments)=}')

# output:
# a1_block(**arguments)={'out_a': 8}
#-

class UpperCase(Block):
    """A Block that uppercases an input string.

    If the input is blank, a default value is used.
    """

    in_str = param.String()
    out_str = param.String()

    def prepare(self):
        if not self.in_str:
            self.in_str = 'a default value'

    def execute(self):
        self.out_str = self.in_str.upper()

#4
uc = UpperCase()
print(uc(in_str='lower case words'))
print(uc(in_str=''))

# output: {'out_str': 'LOWER CASE WORDS'}
# output: {'out_str': 'A DEFAULT VALUE'}
#-
