#

# Tutorial that builds a translation dag.
#
from sier2 import Block, Dag, Connection
import param
import sys

UPPER_VOWELS = str.maketrans('abcde', 'ABCDE')
LOWER_VOWELS = str.maketrans('ABCDE', 'abcde')

class ExternalInput(Block):
    """A block that provides data to the dag."""
    
    out_text = param.String(label='Output text', doc='Output text')
    out_flag = param.Boolean(label='Transform flag', doc='How text is transformed')


class InvertLetters(Block):
    """A block that transforms text.

    The text is converted to upper or lower case, depending on the flag.
    """

    # Inputs.
    #
    in_text = param.String(label='Input text', doc='Text to be transformed')
    in_flag = param.Boolean(label='Transform flag', doc='Upper case if True, else lower case.')

    # Outputs.
    #
    out_text = param.String(label='Output text', doc='Transformed text')
    out_flag = param.Boolean(label='Inverse transform flag', doc='The opposite of the input flag')

    def execute(self):
        print(f'in execute: {self.in_flag=} {self.in_text=}')
        text = self.in_text.upper() if self.in_flag else self.in_text.lower()

        self.out_text = text
        self.out_flag = not self.in_flag

class InvertVowels(Block):
    """A block that inverts the case of vowels."""

    in_text = param.String(label='Input text', doc='Text that will have its vowels mangled')
    in_flag = param.Boolean(label='Transform flag', doc='Upper case if True, else lower case.')
    out_text = param.String(label='Output text', doc='Transformed text')

    def execute(self):
        t = UPPER_VOWELS if self.in_flag else LOWER_VOWELS
        self.out_text = self.in_text.translate(t)


def main(flag: bool):
    external_input = ExternalInput()
    invert_letters = InvertLetters()
    invert_vowels = InvertVowels()

    dag = Dag(doc='Transform', title='tutorial_1a')
    dag.connect(external_input, invert_letters, Connection('out_text', 'in_text'), Connection('out_flag', 'in_flag'))
    dag.connect(invert_letters, invert_vowels, Connection('out_text', 'in_text'), Connection('out_flag', 'in_flag'))

    # Set output params of the Primer block.
    #
    external_input.out_text = 'Hello world.'
    external_input.out_flag = flag

    dag.execute()

    print(f'{invert_vowels.out_text=}')

if __name__=='__main__':
    if len(sys.argv)>1:
        if (arg:=sys.argv[1].upper()[:1]) not in 'UL':
            print('Command line argument must be U or L')
        else:
            flag = arg=='U'
            main(flag)
    else:
        print('Specify U or L as a command line argument')
