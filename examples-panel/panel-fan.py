#

# Demonstrate that the dag chart has a consistent ordering.
#

from sr2 import Block, Connection
from sr2.panel import PanelDag
import param
import random
import time

class PassBlock(Block):
    """A simple block."""
    in_b = param.Boolean(label='inb')
    out_b = param.Boolean(label='outb')

    def execute(self):
        print(f'Execute in block {self.name}')

        # Simulate some work.
        #
        time.sleep(1.0)

        self.out_b = self.in_b

def make_fan_in_dag(title):
    dag = PanelDag(title=title, doc='doc')
    c = Connection('out_b', 'in_b')
    head = PassBlock(name='head', wait_for_input=True)
    tail = PassBlock(name='tail')
    names = [f'Block-{i:02}' for i in range(8)]
    random.shuffle(names)
    for name in names:
        b = PassBlock(name=name)
        dag.connect(head, b, c)
        dag.connect(b, tail, c)

    return dag

def main():
    dag = make_fan_in_dag('fan in')
    dag.show()

if __name__=='__main__':
    main()
