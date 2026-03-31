import os
from pathlib import Path

import param
from sier2 import Block
from sier2.panel import PanelDag


class Types(Block):
    """Demonstrate loading default values."""

    in_int = param.Integer()
    in_num = param.Number()
    in_str = param.String()
    in_bool = param.Boolean()
    in_list = param.List()
    in_color = param.Color()
    in_tuple = param.Tuple(length=3, default=(None, None, None))
    in_dt = param.Date()
    in_dtz = param.Date()
    in_dtr = param.DateRange()

    out_str = param.String()

    def execute(self):
        self.out_str = self.in_str


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
    os.environ['SIER2_DAG_DEFAULTS'] = str(p)

    # Back to the actual code.
    #
    t = Types(name='Demo Values Block')
    r = Result()

    dag = PanelDag(
        site='Defaults', title='Default Values', doc='Demonstrate loading default values'
    )
    dag.build([(t.param.out_str, r.param.in_str)])

    dag.show()
