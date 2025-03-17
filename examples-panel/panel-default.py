# Demonstrate that a default __panel__() method is provided
# that only displays the in_ params.
#
# Also, that a single block can be used as an input block and not an input block.
#

from sier2 import Block, Connection
from sier2.panel import PanelDag
import param

class Data(Block):
    """input values."""

    def __init__(self, name, block_pause_execution):
        super().__init__(name=name, block_pause_execution=block_pause_execution)

    in_nick = param.String(label='NickName')
    in_age = param.Integer(label='Age')
    in_birth = param.Selector(objects=['', 'ACT', 'NSW', 'NT', 'Qld', 'SA', 'Tas', 'Vic', 'WA'])

    out_nick = param.String()
    out_age = param.Integer()
    out_birth = param.Selector(objects=['', 'ACT', 'NSW', 'NT', 'Qld', 'SA', 'Tas', 'Vic', 'WA'])

    def prepare(self):
        self.in_nick = 'In Prepare'
        self.in_age = 99
        self.in_birth = 'ACT'

    def execute(self):
        self.out_nick = self.in_nick
        self.out_age = self.in_age
        self.out_birth = self.in_birth

def make_dag():
    data1 = Data('First', True)
    data2 = Data('Second', False)
    data3 = Data('Third', False)

    dag = PanelDag(title='Default panels', doc='Demonstrate default panels')
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
