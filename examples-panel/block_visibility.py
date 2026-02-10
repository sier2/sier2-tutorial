# A Panel dag containing a block with no GUI.
#

from sier2 import Block, Dag, Connection
from sier2.panel import PanelDag
import param

import holoviews as hv
import panel as pn
import random

hv.extension('bokeh')

class Input(Block):
    """Get a number from the user."""

    in_number = param.Integer(doc='Input number', bounds=(1,10), default=10)
    out_number = param.Integer(doc='An integer')

    def __init__(self, *args, **kwargs):
        super().__init__(wait_for_input=True, *args, **kwargs)

    def execute(self):
        self.out_number = self.in_number

class Modify(Block):
    """Multiply a number by -1."""

    in_number = param.Integer(doc='Some input')
    out_number = param.Integer(doc='Negate')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self):
        self.out_number = self.in_number * -1

class Chart(Block):
    """Draw a bar chart with random bars up to the given height."""

    in_number = param.Integer(doc='Maximum bar height')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hv_pane = pn.pane.HoloViews(sizing_mode='stretch_width')

    def execute(self):
        n = 8
        heights = [random.random() * self.in_number for _ in range(n)]
        bars = hv.Bars(heights).opts(color='x')

        self.hv_pane.object = bars

    def __panel__(self):
        return self.hv_pane

if __name__=='__main__':
    input_block = Input(name='Max bar height', continue_label='Draw chart', doc='Maximum bar height')
    modify_block = Modify(name='Negate', visible=False)
    chart_block = Chart(name='Draw modified numbers')

    dag = PanelDag(doc='Contains an invisible block', site='Example', title='Block visibility')
    dag.connect(input_block, modify_block, Connection('out_number', 'in_number'))
    dag.connect(modify_block, chart_block, Connection('out_number', 'in_number'))

    dag.show()
