#
#
# Demonstrate drawing a less-than-basic dag in the template sidebar.
#

from sier2 import Block, Connection
from sier2.panel import PanelDag
import param

class PassBlock(Block):
    """A simple block."""
    in_b = param.Boolean(label='inb')
    out_b = param.Boolean(label='outb')

    def execute(self):
        self.out_b = self.in_b

def make_binary_tree_dag(title):
    dag = PanelDag(title=title, doc='doc')
    head = PassBlock(name='head', block_pause_execution=True)
    l2 = PassBlock(name='L2')
    r2 = PassBlock(name='R2')
    ll3 = PassBlock(name='LL3')
    lr3 = PassBlock(name='LR3')
    rl3 = PassBlock(name='RL3')
    rr3 = PassBlock(name='RR3')

    c = Connection('out_b', 'in_b')
    dag.connect(head, l2, c)
    dag.connect(head, r2, c)
    dag.connect(l2, ll3, c)
    dag.connect(l2, lr3, c)
    dag.connect(r2, rl3, c)
    dag.connect(r2, rr3, c)

    return dag

def make_tree_tail_dag():
    tail = PassBlock(name='binary tree to a single block')
    dag = make_binary_tree_dag('binary tree to tail')

    c = Connection('out_b', 'in_b')
    dag.connect(dag.block_by_name('LL3'), tail, c)
    dag.connect(dag.block_by_name('LR3'), tail, c)
    dag.connect(dag.block_by_name('RL3'), tail, c)
    dag.connect(dag.block_by_name('RR3'), tail, c)

    return dag

def main():
    dag = make_tree_tail_dag()
    dag.show()

if __name__=='__main__':
    main()
