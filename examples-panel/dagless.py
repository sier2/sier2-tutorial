#

# Demonstrate:
# - blocks without a dag
# - block in a card
# - block not in a card
# - custom button
#

from sier2 import Block
import panel as pn
import param

pn.extension(inline=True)

DESCR = '''
This app demonstrates using blocks without a dag.

The block we use here has two inputs and two correspnding outputs.
THe first instance of the block is displayed in a card. Cards supply
their own "Continue" buttons which is bound with ``self.is_input_valid_``;
the button is enabled only when ``self.is_input_valid_`` is True.

The second instance is an output block ,and is used to display the values
from the first block after the "Continue" button is selected.

The "Display result" button is independent of the blocks - it is used to
display the values in the result block.
'''

class DataBlock(Block):
    """Some data."""

    in_str = param.String(label='A string', doc='Must be non-blank')
    in_int = param.Integer(label='Enter a number', doc='A positive integer', default=0)
    out_str = param.String()
    out_int = param.Integer()

    def __init__(self, *, wait_for_input: bool, is_card: bool, doc: str):
        super().__init__(wait_for_input=wait_for_input, is_card=is_card, doc=doc)
        self.is_input_valid_ = False

        # Make sure input is valid.
        #
        pn.bind(self.check, self.param.in_int, self.param.in_str, watch=True)

    def check(self, i, s):
        try:
            valid = int(i)>0
        except ValueError:
            valid = False

        valid = valid and s is not None and len(s)>0
        print(f'"{i}" "{s}" valid: {valid}')
        self.is_input_valid_ = valid

    def execute(self):
        self.out_str = self.in_str
        self.out_int = self.in_int

def main():
    descr = pn.pane.Markdown(DESCR)

    data_in = DataBlock(wait_for_input=True, is_card=True, doc='Enter some valid data (see the help)')
    data_out = DataBlock(wait_for_input=False, is_card=False, doc='Display the data')

    def do_in_to_out(self, event):
        data_out.in_int = data_in.out_int
        data_out.in_str = data_in.out_str

    data_in.on_continue = do_in_to_out.__get__(data_in)

    end_text = pn.widgets.StaticText(name='Result (from second block)', sizing_mode='stretch_width')
    end_button = pn.widgets.Button(name='Display result', button_type='warning')
    def on_end(event):
        end_text.value = f'"{data_out.in_str}", {data_out.in_int}'
    end_button.on_click(on_end)

    pn.Column(
        descr,
        data_in,
        data_out,
        end_button,
        end_text
    ).show(title='dagless')

main()
