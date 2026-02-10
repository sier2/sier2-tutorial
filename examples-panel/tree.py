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

def make_binary_tree_dag(dag):
    head = PassBlock(name='head', wait_for_input=True)
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

def make_binary_tree_next_level(dag: PanelDag, level: list[Block]):
    """Given a level of blocks in a list, create the next level of blocks in a binary tree."""

    n2 = len(level)*2
    c = Connection('out_b', 'in_b')
    next_level = []
    for i in range(n2):
        pb = PassBlock(name=f'B{n2}/{i}')
        dag.connect(level[i//2], pb, c)
        next_level.append(pb)

    return next_level

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
    dag = PanelDag(title='Dag title', doc='doc')

    # dag = make_tree_tail_dag(dag)

    pb = [PassBlock(name='B1/0', wait_for_input=True)]
    for _ in range(3):
        pb = make_binary_tree_next_level(dag, pb)

    tail = PassBlock(name='binary tree to a single block')
    c = Connection('out_b', 'in_b')
    for b in pb:
        dag.connect(b, tail, c)

    dag.show()

if __name__=='__main__':
    main()
