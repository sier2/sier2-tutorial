#

# Tutorial: blocks with panel widgets.
#
from sier2 import Block, Dag, Connection
import param

import random
import re
import time

import panel as pn
pn.extension(inline=True)

UPPER_VOWELS = str.maketrans('abcde', 'ABCDE')
LOWER_VOWELS = str.maketrans('ABCDE', 'abcde')

class UserInput(Block):
    """A block that provides user input."""

    out_text = param.String(label='Input text', doc='Text to be translated')
    out_flag = param.Boolean(label='Upper case', doc='Changes how text is transformed')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, wait_for_input=True, **kwargs)
        self.out_text = 'The quick brown fox jumps over the lazy dog.'

    def __panel__(self):
        text_widget = pn.widgets.TextAreaInput.from_param(
            self.param.out_text,
            name='Input text',
            placeholder='Enter text here',
            auto_grow=True,
            rows=8,
            resizable='both',
            sizing_mode='stretch_width'
        )

        return pn.Column(
            text_widget,
            pn.Row(pn.HSpacer(), self.param.out_flag, sizing_mode='stretch_width'),
            sizing_mode='stretch_width'
        )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.progress = pn.indicators.Progress(
            name='Translation progress',
            bar_color='primary',
            active=False,
            value=-1
        )

    def execute(self):
        self.progress.active = True

        text = self.in_text.upper() if self.in_flag else self.in_text.lower()

        t = UPPER_VOWELS if not self.in_flag else LOWER_VOWELS
        text = text.translate(t)

        # Emulate work being done.
        #
        time.sleep(random.random() * 2.0)

        self.out_text = text
        self.out_flag = not self.in_flag

        self.progress.active = False

    def __panel__(self):
        return self.progress

class Display(Block):
    """A block that displays text."""

    in_text = param.String(label='Text', doc='Display text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text_widget = pn.widgets.TextAreaInput(
            name='Output text',
            placeholder='Translated text goes here',
            auto_grow=True,
            rows=8,
            resizable='both',
            sizing_mode='stretch_width',
            disabled=True,
            stylesheets=['.bk-input[disabled]{background-color:var(--current-background-color);color:var(--panel-on-secondary-color);opacity:1.0;cursor:text}']
        )

    def execute(self):
        self.text_widget.value = self.in_text

    def __panel__(self):
        return self.text_widget

if __name__=='__main__':
    ui = UserInput(name='User input')
    tr = Invert(name='Transform')
    di = Display(name='Display output')

    dag = Dag(doc='Transformation', title='Transform text')
    dag.connect(ui, tr, Connection('out_text', 'in_text'), Connection('out_flag', 'in_flag'))
    dag.connect(tr, di, Connection('out_text', 'in_text'))

    pn.Column(ui, tr, di).show()
