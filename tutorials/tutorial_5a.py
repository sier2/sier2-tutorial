from tutorial_2a import ExternalInput, SingleCase, CharDistribution
from sr2 import Block, Connection, Connections
from sr2.panel import PanelDag

import param
import holoviews as hv
import panel as pn

from collections import Counter

hv.extension('bokeh', inline=True)
pn.extension(inline=True)

class ExternalInput(Block):
    """A block that provides data to the dag."""

    in_text = param.String(label='Input text', doc='Must be non-empty')
    in_case = param.Selector(objects={'Upper':'U', 'Lower':'L'}, label='Case', doc='U for upper case, L for lower case')
    out_text = param.String(doc='Non-empty text')
    # out_upper = param.Boolean(doc='Upper if True, lower if False')
    out_case = param.Selector(objects={'Upper':'U', 'Lower':'L'}, label='Case', doc='U for upper case, L for lower case')

    def __init__(self):
        super().__init__(
            name='User input',
            doc='Enter a non-blank string.',
            wait_for_input=True,
            continue_label='Count',
            display_options={
            'parameters': ['in_text', 'in_case'],
            'widgets': {
                'in_case': {
                    'widget_type': pn.widgets.RadioBoxGroup,
                    'inline': True,
                    'name': 'Select a case'
                }
            }
        })

    @param.depends('in_text', watch=True)
    def _check_valid(self):
        self.is_input_valid_ = self.in_text!=''

    def prepare(self):
        self._check_valid()

    def execute(self):
        self.out_text = self.in_text
        self.out_case = self.in_case

class SingleCase(Block):
    """A block that upper or lower cases the input text according to the flag."""

    # Inputs.
    #
    in_text = param.String(label='Input text', doc='Text to be lowercased')
    in_case = param.Selector(objects={'Upper':'U', 'Lower':'L'}, doc='U for upper case, L for lower case')
    out_text = param.String(label='Output text', doc='Upper or lower case text')

    def __init__(self):
        super().__init__(visible=False)

    def execute(self):
        self.out_text = self.in_text.upper() if self.in_case=='U' else self.in_text.lower()

class CharDistribution(Block):
    """A block that counts the number of times each character occurs in a string.

    The results are:
    - out_len: the length of the input text
    - out_counter: a dictionary containing the character counts
    - out_bars: a string representing a bar chart of the counts
    """

    in_text = param.String(label='Input text', doc='Input text')
    out_len = param.Integer(label='Length', doc='The number of characters in the text')
    out_counter = param.Dict(doc='A dictionary mapping characters to their counts')
    out_bars = param.String(label='Output text', doc='A bar chart')

    def __init__(self):
        super().__init__(visible=False)

    def execute(self):
        self.out_len = len(self.in_text)

        counter = Counter(self.in_text)
        self.out_counter = dict(counter)

class DisplayCountBars(Block):
    """A block that displays a character distribution barchart."""

    in_len = param.Integer(label='Length', doc='The number of characters in the text')
    in_counter = param.Dict(doc='A dictionary mapping characters to their counts')

    def __init__(self, *args, **kwargs):
        super().__init__(name='Character count results', *args, **kwargs)

        self.hv_pane = pn.pane.HoloViews(sizing_mode='stretch_width')

    def execute(self):
        if self.in_counter:
            # - Convert the counter dictionary to tuples of (char, count).
            # - Sort the tuple by descending count, ascending character.
            # - Find the maximum count.
            #
            items = tuple(self.in_counter.items())
            items = sorted(items, key=lambda item:(-item[1], item[0]))
            max_count = max(count for char,count in items)

            bars = hv.Bars(items).opts(
                title=f'Character counts (length {self.in_len})',
                line_color=None,
                xlabel='characters',
                ylabel='count',
                yticks=list(range(max_count+1))
            )
        else:
            bars = hv.Bars([])

        self.hv_pane.object = bars

    def __panel__(self):
        """A custom pane.

        We get the default pane and add a bar chart.
        """

        panel = super().__panel__()

        return pn.Column(
            panel,
            self.hv_pane,
            sizing_mode='stretch_width'
        )

if __name__=='__main__':
    external_input = ExternalInput()
    lc = SingleCase()
    ld = CharDistribution()
    display = DisplayCountBars()

    doc = '''Count character distribution
This app takes an input string, converts it to either upper or lower case,
and counts the number of occurences of each character in the string.

The result is displayed as a _HoloViews_ bar chart.'''

    dag = PanelDag(title='Character counts', doc=doc, logo='logo.png')
    dag.connect(external_input, lc, Connections({
        'out_text': 'in_text',
        'out_case': 'in_case'
    }))
    dag.connect(lc, ld, Connection('out_text', 'in_text'))

    dag.connect(ld, display, Connections({
        'out_len': 'in_len',
        'out_counter': 'in_counter'})
    )

    dag.show()
