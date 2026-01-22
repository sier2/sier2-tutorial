#

# Tutorial that builds a character counting dag with user input.
#
from sier2 import Block, Dag, Connection, Connections
import param
from collections import Counter

class ExternalInput(Block):
    """A block that provides data to the dag."""

    in_text = param.String()
    in_upper = param.Boolean()
    out_text = param.String()
    out_upper = param.Boolean()

    def __init__(self):
        super().__init__(wait_for_input=True)

    def execute(self):
        self.out_text = self.in_text
        self.out_upper = self.in_upper

class SingleCase(Block):
    """A block that upper or lower- cases the input text according to the flag."""

    # Inputs.
    #
    in_text = param.String()
    in_upper = param.Boolean()
    out_text = param.String()

    def execute(self):
        self.out_text = self.in_text.upper() if self.in_upper else self.in_text.lower()
        self.out_upper = self.in_upper

class CharDistribution(Block):
    """A block that counts the number of times each character occurs in a string.

    The results are:
    - out_len: the length of the input text
    - out_counter: a dictionary containing the character counts
    - out_bars: a string representing a bar chart of the counts
    """

    in_text = param.String()
    out_len = param.Integer()
    out_counter = param.Dict()
    out_bars = param.String()

    def execute(self):
        self.out_len = len(self.in_text)

        counter = Counter(self.in_text)
        self.out_counter = dict(counter)

class Display(Block):
    """A block that displays a character distribution."""

    in_len = param.Integer()
    in_counter = param.Dict()

    def execute(self):
        print('----')
        print(f'Input length: {self.in_len}')

        data = sorted(self.in_counter.items(), key=lambda item:(-item[1], item[0]))
        lines = '\n'.join(f'{k} {v:3} {"*"*v}' for k,v in data)
        print(lines)

if __name__=='__main__':
    external_input = ExternalInput()
    lc = SingleCase()
    ld = CharDistribution()
    display = Display()

    dag = Dag(title='tutorial_2a', doc='Count character distribution')
    dag.connect(external_input, lc, Connection('out_text', 'in_text'), Connection('out_upper', 'in_upper'))
    dag.connect(lc, ld, Connection('out_text', 'in_text'))

    # Use ``Connections`` for a more succint mapping.
    #
    dag.connect(ld, display, Connections({
        'out_len': 'in_len',
        'out_counter': 'in_counter'})
    )

    # b is the block that the dag paused at.
    #
    b = dag.execute()
    print(f'Input for block {b}')
    text = input('Enter a string: ')
    b.in_text = text

    while True:
        ul = input('(U)pper, (L)ower, (D)efault: ').upper()
        if ul in list('ULD'):
            if ul!='D':
                b.in_upper = ul=='U'

            break

    # Resume dag execution at block b.
    #
    dag.execute_after_input(b)
