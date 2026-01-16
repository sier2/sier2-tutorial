#

# Tutorial that builds a translation dag.
#
from sr2 import Block, Dag, Connection
import param
import sys
from collections import Counter

UPPER_VOWELS = str.maketrans('abcde', 'ABCDE')
LOWER_VOWELS = str.maketrans('ABCDE', 'abcde')

class ExternalInput(Block):
    """A block that provides data to the dag."""

    in_text = param.String(label='Input text', doc='Input text')
    out_text = param.String(label='Output text', doc='Output text')

    def execute(self):
        self.out_text = self.in_text

class LowerCase(Block):
    """A block that lowercases an input string."""

    # Inputs.
    #
    in_text = param.String(label='Input text', doc='Text to be lowercased')
    out_text = param.String(label='Output text', doc='Lowercase text')

    def execute(self):
        self.out_text = self.in_text.lower()

class CharDistribution(Block):
    """A block that counts the number of times each character occurs in a string."""

    in_text = param.String(label='Input text', doc='Input text')
    out_text = param.String(label='Output text', doc='A bar chart')
    out_len = param.Integer(label='Length', doc='The number of characters in the text')

    def execute(self):
        self.out_len = len(self.in_text)

        counter = Counter(self.in_text)
        data = sorted(counter.items(), key=lambda item:(-item[1], item[0]))
        lines = '\n'.join(f'{k} {v:3} {"*"*v}' for k,v in data)
        self.out_text = lines

def main():
    external_input = ExternalInput()
    lc = LowerCase()
    ld = CharDistribution()

    dag = Dag(doc='Count character distribution', title='tutorial_1a')
    dag.connect(external_input, lc, Connection('out_text', 'in_text'))
    dag.connect(lc, ld, Connection('out_text', 'in_text'))

    external_input.in_text = 'The CAT sat on the MAT.'
    dag.execute()

    print(f'Input length: {ld.out_len}')
    print(ld.out_text)

if __name__=='__main__':
    main()
