#!/usr/bin/env python

# Demonstrate different display options for blocks.
#

import random

import pandas as pd
import panel as pn
import param
from sier2 import Block
from sier2.panel import PanelDag

pn.extension('tabulator', inline=True)


class LoadDataFrame(Block):
    """Create some data."""

    out_df = param.DataFrame(label='My data', doc='From somewhere')

    def __init__(self, name):
        super().__init__(
            name=name, wait_for_input=True, doc='Select "Continue" to load a (dummy) dataframe.'
        )

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
        super().__init__(
            name=name,
            wait_for_input=True,
            doc=doc,
            display_options=display_options,
            only_in=only_in,
        )

    def prepare(self):
        cols = list(self.in_df.columns)
        self.param.columns.objects = []  # Reset the selected values.
        self.param.columns.objects = cols

        self.is_input_valid_ = True

    def execute(self):
        # Carry forward the selected columns, or all columns if none were selcted.
        #
        self.out_df = self.in_df[self.columns] if self.columns else self.in_df


class Display(Block):
    """Display a dataframe."""

    in_df = param.DataFrame(label='In data', doc='Data from somewhere')


ldf = LoadDataFrame(name='Load dataframe')
c0 = ColumnSelector(
    'Default display',
    doc='The default display - the column selection is included because only_in is False; it is not used in this block.',
)
c1 = ColumnSelector(
    'Default display with only_in True',
    only_in=True,
    doc='The column selection is not included because only_in is True and it is not an "in_" param.',
)
c2 = ColumnSelector(
    'List of names',
    display_options=['columns'],
    doc='Specify a list of param names - "column" is explicitly specified.',
)
c3 = ColumnSelector(
    'Dict of kwargs - CheckBoxGroup',
    display_options={'parameters': ['columns'], 'widgets': {'columns': pn.widgets.CheckBoxGroup}},
    doc='Specify a mapping to a different widget',
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
            }
        },
    },
    doc='Specify a mapping to a widget with options.',
)
c5 = ColumnSelector(
    'Dict of kwargs - CheckButtonGroup with options',
    display_options={
        'widgets': {
            'columns': {
                'widget_type': pn.widgets.CheckButtonGroup,
                'button_type': 'primary',
                'button_style': 'outline',
                'description': 'Select some columns',
            }
        }
    },
    doc='Using a CheckButtonGroup; no parameters, so non-out params are displayed.',
)
d = Display(name='Display dataframe')

dagdoc = '''
# Display widgets

This dag demonstrates the ability to adjust the display of a block
using the `display_options` parameter. A `param.ListSelector`
displays differently depending on how `display_options` is defined.

Start by selecting several columns, then select fewer each time. The selected
columns carry forward to the next block.
'''
dag = PanelDag(
    [
        (ldf.param.out_df, c0.param.in_df),
        (c0.param.out_df, c1.param.in_df),
        (c1.param.out_df, c2.param.in_df),
        (c2.param.out_df, c3.param.in_df),
        (c3.param.out_df, c4.param.in_df),
        (c4.param.out_df, c5.param.in_df),
        (c5.param.out_df, d.param.in_df),
    ],
    title='Display',
    doc=dagdoc,
)

dag.show()
