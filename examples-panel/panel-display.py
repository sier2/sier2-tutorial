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
        super().__init__(name=name, wait_for_input=True, doc='Select "Continue" to load a (dummy) dataframe.')

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

    def __init__(self, name, doc, only_in=False, display_options=None):
        super().__init__(name=name, wait_for_input=True, doc=doc, display_options=display_options, only_in=only_in)

    def prepare(self):
        cols = list(self.in_df.columns)
        self.param.columns.objects = [] # Reset the selected values.
        self.param.columns.objects = cols

    def execute(self):
        new_cols = self.columns # self.param.columns.objects

        self.out_df = self.in_df[self.columns] if self.columns else self.in_df

class Display(Block):
    """Display a dataframe."""

    in_df = param.DataFrame(label='In data', doc='Data from somewhere')

ldf = LoadDataFrame(name='Load dataframe')
c0 = ColumnSelector('Default display', doc='The default display - the column selection is included because only_in is False; it is not used in this block.')
c1 = ColumnSelector('Default display with only_in True', only_in=True, doc='The column selection is not included because only_in is True and it is not an "in_" param.')
c2 = ColumnSelector('List of names', display_options=['columns'], doc='Specify a list of param names - "column" is explicitly specified.')
c3 = ColumnSelector(
    'Dict of kwargs - CheckBoxGroup',
    display_options={
        'parameters': ['columns'],
        'widgets': {'columns': pn.widgets.CheckBoxGroup}
    },
    doc='Specify a mapping to a different widget'
)
c4 = ColumnSelector(
    'Dict of kwargs - CheckBoxGroup with options',
    display_options={
        'parameters': ['columns'],
        'widgets': {
            'columns': {
                'widget_type': pn.widgets.CheckBoxGroup,
                'inline': True,
                'styles': {'background': 'teal'},
        }}
    },
    doc='Specify a mapping to a widget with options.'
)
c5 = ColumnSelector(
    'Dict of kwargs - CheckButtonGroup with options',
    display_options={
        'widgets': {
            'columns': {
                'widget_type': pn.widgets.CheckButtonGroup,
                'button_type': 'default',
                'description': 'Select some columns'
            }
        }
    },
    doc='Using a CheckButtonGroup; no parameters, so non-out params are displayed.'
)
d = Display(name='Display dataframe')

dagdoc = '''
# Display widgets

This dag demonstrates the ability to adjust the display of a block
using the `display_options` parameter. A single `ColumnSelector` block
displays differently depending on how `display_options` is defined.
'''
dag = PanelDag(title='Display', doc=dagdoc)
c = Connection('out_df', 'in_df')
dag.connect(ldf, c0, c)
dag.connect(c0, c1, c)
dag.connect(c1, c2, c)
dag.connect(c2, c3, c)
dag.connect(c3, c4, c)
dag.connect(c4, c5, c)
dag.connect(c5, d, c)

dag.show()
