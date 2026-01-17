from tutorial_2a import ExternalInput, SingleCase, CharDistribution
from sr2 import Block, Connection, Connections
from sr2.panel import PanelDag

import param
import holoviews as hv
import panel as pn

hv.extension('bokeh', inline=True)
pn.extension(inline=True)

class DisplayCountBars(Block):
    """A block that displays a character distribution barchart."""

    in_len = param.Integer(label='Length', doc='The number of characters in the text')
    in_counter = param.Dict(doc='A dictionary mapping characters to their counts')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                # invert_axes=True,
                xlabel='characters',
                ylabel='count',
                # xticks=list(range(max_count+1))
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

    dag = PanelDag(doc='Count character distribution', title='tutorial_1a')
    dag.connect(external_input, lc, Connection('out_text', 'in_text'), Connection('out_upper', 'in_upper'))
    dag.connect(lc, ld, Connection('out_text', 'in_text'))

    # Use ``Connections`` for a more succint mapping.
    #
    dag.connect(ld, display, Connections({
        'out_len': 'in_len',
        'out_counter': 'in_counter'})
    )

    dag.show()
