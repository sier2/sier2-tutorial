from sr2 import Block
import param

class AddOne(Block):
    """A block that adds one to its input."""

    in_a = param.Integer()
    out_a = param.Integer()

    def execute(self):
        self.out_a = self.in_a + 1

class SingleCase(Block):
    """A Block that upper or lower cases an input string.

    If the input is blank, a default value is used.
    """

    in_str = param.String()
    in_upper = param.Boolean()
    out_str = param.String()

    def prepare(self):
        if not self.in_str:
            self.in_str = 'a default value'

    def execute(self):
        self.out_str = self.in_str.upper() if self.in_upper else self.in_str.lower()

if __name__=='__main__':
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

    #4
    uc = SingleCase()
    print(uc(in_str='Lower Case Words', in_upper=True))
    print(uc(in_str='Lower Case Words', in_upper=False))
    print(uc(in_str=''))

    # output: {'out_str': 'LOWER CASE WORDS'}
    # output: {'out_str': 'lower case words'}
    # output: {'out_str': 'A DEFAULT VALUE'}
    #-
