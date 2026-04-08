import holoviews as hv
import panel as pn
import param
from sier2 import Block
from sier2.panel import PanelDag
from tutorial_2a import CharDistribution, ExternalInput, SingleCase

hv.extension('bokeh', inline=True)
pn.extension(inline=True)


class DisplayCountBars(Block):
    """A block that displays a character distribution barchart."""

    in_len = param.Integer()
    in_counter = param.Dict()

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
            items = sorted(items, key=lambda item: (-item[1], item[0]))
            max_count = max(count for char, count in items)

            bars = hv.Bars(items).opts(
                title=f'Character counts (length {self.in_len})',
                line_color=None,
                invert_axes=True,
                xlabel='characters',
                ylabel='count',
                yticks=list(range(max_count + 1)),
            )
        else:
            bars = hv.Bars([])

        self.hv_pane.object = bars

    def __panel__(self):
        """A custom pane.

        We get the default pane and add a bar chart.
        """

        panel = super().__panel__()

        return pn.Column(panel, self.hv_pane, sizing_mode='stretch_width')


if __name__ == '__main__':
    external_input = ExternalInput()
    lc = SingleCase()
    ld = CharDistribution()
    display = DisplayCountBars()

    dag = PanelDag(
        [
            (external_input.param.out_text, lc.param.in_text),
            (external_input.param.out_upper, lc.param.in_upper),
            (lc.param.out_text, ld.param.in_text),
            (ld.param.out_len, display.param.in_len),
            (ld.param.out_counter, display.param.in_counter),
        ],
        doc='Count character distribution',
        title='tutorial_4a',
    )

    dag.show()
