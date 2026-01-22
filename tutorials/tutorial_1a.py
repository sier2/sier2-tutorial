#

# Tutorial that builds a character counting dag.
#
from sier2 import Block, Dag, Connection
import param
from collections import Counter

class ExternalInput(Block):
    """A block that provides data to the dag."""

    in_text = param.String(label='Input text', doc='Input text')
    in_upper = param.Boolean(label='Upper or lower case', doc='Upper if True, lower if False')
    out_text = param.String(label='Output text', doc='Output text')
    out_upper = param.Boolean()

    def execute(self):
        self.out_text = self.in_text
        self.out_upper = self.in_upper

class SingleCase(Block):
    """A block that upper or lower- cases the input text according to the flag."""

    # Inputs.
    #
    in_text = param.String(label='Input text', doc='Text to be lowercased')
    in_upper = param.Boolean(label='Upper or lower case', doc='Upper if True, lower if False')
    out_text = param.String(label='Output text', doc='Upper- or lower- case text')

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

    in_text = param.String(label='Input text', doc='Input text')
    out_len = param.Integer(label='Length', doc='The number of characters in the text')
    out_counter = param.Dict(doc='A dicionary mapping characters to their counts')
    out_bars = param.String(label='Output text', doc='A bar chart')

    def execute(self):
        self.out_len = len(self.in_text)

        counter = Counter(self.in_text)
        data = sorted(counter.items(), key=lambda item:(-item[1], item[0]))
        lines = '\n'.join(f'{k} {v:3} {"*"*v}' for k,v in data)
        self.out_bars = lines
        self.out_counter = dict(counter)

if __name__=='__main__':
    external_input = ExternalInput()
    lc = SingleCase()
    ld = CharDistribution()

    dag = Dag(title='tutorial_1a', doc='Count character distribution')
    dag.connect(external_input, lc, Connection('out_text', 'in_text'), Connection('out_upper', 'in_upper'))
    dag.connect(lc, ld, Connection('out_text', 'in_text'))

    external_input.in_text = 'The CAT sat on the MAT.'
    external_input.in_upper = False
    dag.execute()

    print('----')
    print(f'Input length: {ld.out_len}')
    print(ld.out_bars)
