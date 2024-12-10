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

class Invert(Block):
    """A block that transforms text.

    The text is converted to upper or lower case, depending on the flag.
    Then vowels are converted to lower or upper case,depending on the flag.
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
        text = self.in_text.upper() if self.in_flag else self.in_text.lower()

        t = UPPER_VOWELS if not self.in_flag else LOWER_VOWELS
        text = text.translate(t)

        self.out_text = text
        self.out_flag = not self.in_flag

class Display(Block):
    """A block that displays text."""

    in_text = param.String(label='Text', doc='Display text')

def main(flag: bool):
    ei = ExternalInput()
    tr = Invert()
    di = Display()

    dag = Dag(doc='Transform', title='tutorial_1a')
    dag.connect(ei, tr, Connection('out_text', 'in_text'), Connection('out_flag', 'in_flag'))
    dag.connect(tr, di, Connection('out_text', 'in_text'))

    text = 'Hello world.'
    print('Input text:')
    print(text)
    print()

    # Set output params of the Primer block.
    #
    ei.out_text = text
    ei.out_flag = flag

    dag.execute()

    print('Output text:')
    print(di.in_text)
    print()

if __name__=='__main__':
    if len(sys.argv)>1:
        if (arg:=sys.argv[1].upper()[:1]) not in 'UL':
            print('Command line argument must be U or L')
        else:
            flag = arg=='U'
            main(flag)
    else:
        print('Specify U or L as a command line argument')
