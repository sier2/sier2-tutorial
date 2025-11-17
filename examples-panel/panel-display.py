#

# Demonstrate different display options for blocks.
#

from sier2 import Block, Dag, Connection
from sier2.panel import PanelDag
import param
import panel as pn

import pandas as pd
import random

pn.extension('tabulator', inline=True)

class LoadDataFrame(Block):
    """Create some data."""

    out_df = param.DataFrame(label='My data', doc='From somewhere')

    def __init__(self, name):
        super().__init__(name=name, block_pause_execution=True, block_doc='Continue to load a (dummy) dataframe.')

    def execute(self):
        df = pd.DataFrame()
        for column in 'ABCDEFGHIJK':
            df[column] = [random.randint(1, 10) for _ in range(3)]
        self.out_df = df

class ColumnSelector(Block):
    """Demonstrate displaying widgets."""

    in_df = param.DataFrame(label='In data', doc='Data from somewhere')
    out_df = param.DataFrame(label='Out data', doc='There it goes')

    columns = param.ListSelector(label='Select columns')

    def __init__(self, name, block_doc, block_widgets=None):
        super().__init__(name=name, block_pause_execution=True, block_doc=block_doc, block_widgets=block_widgets)

    def prepare(self):
        cols = list(self.in_df.columns)
        self.param.columns.objects = [] # Reset the selected values.
        self.param.columns.objects = cols

    def execute(self):
        # print(self.name, 'new cols1', self.columns)
        new_cols = self.columns # self.param.columns.objects
        # print(self.name, 'new cols2', type(new_cols), new_cols)

        self.out_df = self.in_df[self.columns] if self.columns else self.in_df

class Display(Block):
    """Display a dataframe."""

    in_df = param.DataFrame(label='In data', doc='Data from somewhere')

ldf = LoadDataFrame(name='Load dataframe')
c1 = ColumnSelector('Default display', block_doc='The default display - the column selection is not included because it is not an in_ param.')
c2 = ColumnSelector('List of names', block_widgets=['columns'], block_doc='Specify a list of param names')
c3 = ColumnSelector('Dict of mappings', block_widgets={'columns':pn.widgets.CheckBoxGroup}, block_doc='Specify a mapping to a different widget')
c4 = ColumnSelector('Dict of mappings and options', block_widgets={
    'columns': {
        'widget_type': pn.widgets.CheckBoxGroup,
        'inline': True
    }},
    block_doc='Specify a mapping to a widget with options.'
)
d = Display(name='Display dataframe')

dagdoc = '''
# Display widgets

This dag demonstrates the ability to adjust the display of a block
using the `block_widgets` parameter. A single `ColumnSelector` block
displays differently depending on how `block_widgets` is defined.
'''
dag = PanelDag(title='Display', doc=dagdoc)
dag.connect(ldf, c1, Connection('out_df', 'in_df'))
dag.connect(c1, c2, Connection('out_df', 'in_df'))
dag.connect(c2, c3, Connection('out_df', 'in_df'))
dag.connect(c3, c4, Connection('out_df', 'in_df'))
dag.connect(c4, d, Connection('out_df', 'in_df'))

dag.show()
