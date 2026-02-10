# Demonstrate that a default __panel__() method is provided
# that only displays the non-"out_" params.
#
# Also, that a single block can be used as an input block and not an input block.
#

from sier2 import Block, Connection
from sier2.panel import PanelDag
import param
import panel as pn

class Data(Block):
    """input values."""

    def __init__(self, name, wait_for_input):
        super().__init__(name=name, wait_for_input=wait_for_input)

    in_nick = param.String(label='NickName', default='Nick Name')
    in_age = param.Integer(label='Age', default=21)
    in_birth = param.Selector(objects=['', 'ACT', 'NSW', 'NT', 'Qld', 'SA', 'Tas', 'Vic', 'WA'])

    extra = param.String(doc='An extra varaible only used by this block')

    out_nick = param.String()
    out_age = param.Integer()
    out_birth = param.Selector(objects=['', 'ACT', 'NSW', 'NT', 'Qld', 'SA', 'Tas', 'Vic', 'WA'])

    def execute(self):
        print(f'{self.in_nick=} {self.in_age=} {self.in_birth=}')
        self.out_nick = self.in_nick
        self.out_age = self.in_age
        self.out_birth = self.in_birth

    def __panel__(self):
        """Use the default implementation in super().__panel__().

        If this is an input block, add instructions.
        """

        p = super().__panel__()
        if self._wait_for_input:
            p = pn.Row(
                p,
                pn.widgets.StaticText(
                    name='Instructions',
                    value='Please fill in the fields.'
                )
            )

        return p

def make_dag():
    data1 = Data('First', True)
    data2 = Data('Second', False)
    data3 = Data('Third', False)

    dag = PanelDag(title='Default panels', doc='Demonstrate using default panels\nThis block demonstrates using a custom panel incorporating the default panel. We allow the `PanelDag` to generate the default widgets, and use the result to build our own custom GUI, adding instructions alongside the displayed fields.')
    dag.connect(data1, data2,
        Connection('out_nick', 'in_nick'),
        Connection('out_age', 'in_age'),
        Connection('out_birth', 'in_birth')
    )
    dag.connect(data2, data3,
        Connection('out_nick', 'in_nick'),
        Connection('out_age', 'in_age'),
        Connection('out_birth', 'in_birth')
    )

    return dag

if __name__=='__main__':
    dag = make_dag()
    dag.show()
