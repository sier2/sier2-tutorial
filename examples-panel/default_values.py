#!/usr/bin/env python

import os
from pathlib import Path

import panel as pn
import param
from sier2 import Block
from sier2.panel import PanelDag


class Types(Block):
    """Demonstrate loading default values."""

    in_int = param.Integer()
    in_num = param.Number()
    in_str = param.String()
    in_bool = param.Boolean()
    in_list = param.ListSelector(objects=['red', 'green', 'blue'])
    in_color = param.Color()
    in_tuple = param.Tuple(length=3, default=(None, None, None))
    in_dt = param.Date()
    in_dtz = param.Date()
    in_dtr = param.DateRange()

    out_str = param.String()

    def execute(self):
        self.out_str = self.in_str

    def __panel__(self):
        return pn.Param(
            self,
            widgets={
                'in_bool': {'widget_type': pn.widgets.Switch, 'name': 'The bool'},
                'in_list': {'widget_type': pn.widgets.MultiChoice, 'name': 'The list'},
                'in_tuple': {'widget_type': pn.widgets.LiteralInput, 'name': 'The tuple'},
                'in_dt': {'widget_type': pn.widgets.DatePicker, 'name': 'The date'},
                'in_dtz': {'widget_type': pn.widgets.DatePicker, 'name': 'The UTC date'},
                'in_dtr': {'widget_type': pn.widgets.DateRangePicker, 'name': 'The date range'},
            },
            parameters=self.pick_params(),
            sizing_mode='stretch_width',
        )


class Result(Block):
    """Display a result."""

    in_str = param.String()


if __name__ == '__main__':
    # This is typically done outside the code.
    # Windows (PowerShell):
    # PS> $env:SIER2_DAG_DEFAULTS = 'path/tp/default_values.toml'
    # PS> python default_values.py
    #
    # Linux:
    # $ SIER2_DAG_DEFAULTS=path/tp/default_values.toml ./default_values.py
    #
    p = Path(__file__).with_suffix('.toml')
    os.environ[PanelDag.SIER2_DAG_DEFAULTS] = str(p)

    # Back to the actual code.
    #
    t = Types(name='Demo Values Block')
    r = Result()

    dag = PanelDag(
        [(t.param.out_str, r.param.in_str)],
        site='Defaults',
        title='Default Values',
        doc='Demonstrate loading default values',
    )

    dag.show()
