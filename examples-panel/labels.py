# Demonstrate that "default" labels do not have the "in_" prefix.
#

from sier2 import Block, Connection
from sier2.panel import PanelDag

import param

class Inputs(Block):
    """A bunch of inputs to be displayed by Panel."""

    in_age_in_years = param.Integer(doc='An integer number of years', bounds=(0, 100))
    in_age_in_years_label = param.Integer(doc='A labelled integer number of years', bounds=(0, 100), label='A custom label; do not alter')
    in_full_name = param.String(doc='Your full name')
    in_australian_citizen = param.Boolean(doc='Are you an Australian citizen?')
    in_australian_domicile_labelled = param.Boolean(doc='Are you living in Australia?', label='In Australia? (custom label starting with "In ")')
    in_favourite_country = param.Selector(objects=['Australia', 'Canada', 'Great Britain', 'New Zealand', 'United States of America'], doc='Pick a country')
    in_favourite_color = param.Color(doc='Your favourite color')

    out_string = param.String(doc='Output')

    def __init__(self):
        super().__init__(name='params with labels', block_pause_execution=True, continue_label='Execute')

    def execute(self):
        print(f'{self.in_favourite_country}')
        print(f'{self.in_favourite_color}')
        self.out_string = self.in_full_name

class Null(Block):
    """A null block."""
    in_dummy = param.String(doc='Nothing')

    def __init__(self):
        super().__init__(block_visible=False)

if __name__=='__main__':

    dag = PanelDag(title='Label demo', doc='## Demonstrate Panel labels with "in_"')
    dag.connect(Inputs(), Null(), Connection('out_string', 'in_dummy'))
    dag.show()
