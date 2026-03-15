import holoviews as hv
import panel as pn

from sier2 import Block, Connections
from sier2.panel import PanelDag
import param

import pandas as pd
import random

from _panel_widgets import BarchartWidget

DOC = 'This dag does nothing in particular, it just shows off banners.'

hv.extension('bokeh', inline=True)


def color():
    c = lambda: random.randint(1, 255)
    return f'#{c():02x}{c():02x}{c():02x}'


def _banner_text(text, fgcolor='white', bgcolor='red'):
    return f'<span style="display: flex; justify-content: center;color:{fgcolor};background-color:{bgcolor};font-size:12pt;">{text}</span>'


class Choose(Block):
    """Choose the number of bars."""

    in_n = param.Integer(label='Number of bars', allow_None=False, default=10)
    in_title = param.String(label='title', default='Bar chart', allow_None=False)
    out_title = param.String(label='title')
    out_df = param.DataFrame(label='Bar values')

    def __init__(self):
        center = 'display: flex; justify-content: center;'
        top = f'<span style="display: flex; justify-content: center;color:white;background-color:red;font-size:12pt;">The top banner</span>'
        bot = 'The bottom banner'
        super().__init__(
            wait_for_input=True,
            banners=(_banner_text('The top banner'), _banner_text('The bottom banner')),
        )

    def execute(self):
        colors = [color() for _ in range(self.in_n)]
        self.banners((None, _banner_text(self.in_title, colors[0], colors[-1])))
        self.out_df = pd.DataFrame({'Colors': colors, 'Counts': range(1, self.in_n + 1)})
        self.out_title = self.in_title


def main():
    # center = 'display: flex; justify-content: center;'
    # top = f'<span style="{center}color:white;background-color:red;font-size:16pt;">The top banner</span>'
    # bot = 'The bottom banner'
    dag = PanelDag(doc=DOC, site='Example', title='Banner')  # , banner=(top, bot))

    c = Choose()
    b = BarchartWidget()
    dag.connect(c, b, Connections({'out_df': 'in_df', 'out_title': 'in_title'}))
    dag.show()


if __name__ == '__main__':
    main()
