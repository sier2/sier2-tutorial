import random
from pathlib import Path

import holoviews as hv
import pandas as pd
import param
from _panel_widgets import BarchartWidget
from sier2 import Block, Connections
from sier2.panel import PanelDag

DOC = 'This dag does nothing in particular, it just shows off banners a logo, and a favicon.'

hv.extension('bokeh', inline=True)


def color():
    c = lambda: random.randint(1, 255)  # noqa: E731
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
    logo_dir = Path(__file__).parent

    dag = PanelDag(
        doc=DOC,
        site='Example',
        title='Banner',
        logo=str(logo_dir / 'logo_horizontal_dark_theme.png'),
        favicon=str(logo_dir / 'py.svg'),
    )

    c = Choose()
    b = BarchartWidget()
    dag.connect(c, b, Connections({'out_df': 'in_df', 'out_title': 'in_title'}))
    dag.show()


if __name__ == '__main__':
    main()
