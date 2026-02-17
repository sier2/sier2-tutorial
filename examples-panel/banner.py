import holoviews as hv
import panel as pn

from sier2 import Block, Connection
from sier2.panel import PanelDag
import param

import pandas as pd
import random

from _panel_widgets import BarchartWidget

DOC = 'This dag does nothing in particular, it just shows off banners.'

hv.extension('bokeh', inline=True)

def color():
    c = lambda : random.randint(1, 255)
    return f'#{c():02x}{c():02x}{c():02x}'

class Choose(Block):
    """Choose the number of bars."""

    in_n = param.Integer(label='Number of bars', allow_None=False, default=10)
    out_df = param.DataFrame(label='Bar values')

    def __init__(self):
        super().__init__(wait_for_input=True)

    def execute(self):
        self.out_df = pd.DataFrame({
            'Colors': [color() for _ in range(self.in_n)],
            'Counts': range(1, self.in_n+1)
        })

def main():
    center = 'display: flex; justify-content: center;'
    top = f'<span style="{center}color:white;background-color:red;font-size:16pt;">The top banner</span>'
    bot = 'The bottom banner'
    dag = PanelDag(doc=DOC, site='Example', title='Banner', banner=(top, bot))

    c = Choose()
    b = BarchartWidget()
    dag.connect(c, b, Connection('out_df', 'in_df'))
    dag.show()

if __name__=='__main__':
    main()
