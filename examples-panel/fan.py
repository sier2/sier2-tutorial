#

# Demonstrate that the dag chart has a consistent ordering.
#

import random
import time

import param
from sier2 import Block, Connection
from sier2.panel import PanelDag


class PassBlock(Block):
    """A simple block."""

    in_b = param.Boolean(label='inb')
    out_b = param.Boolean(label='outb')

    def execute(self):
        print(f'Execute in block {self.name}')

        if not self._wait_for_input:
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


def make_fan_in_dag_cxns(title):
    head = PassBlock(name='head', wait_for_input=True)
    tail = PassBlock(name='tail')

    names = [f'Block-{i:02}' for i in range(8)]
    random.shuffle(names)

    cxns = []
    for name in names:
        b = PassBlock(name=name)
        cxns.append((head.param.out_b, b.param.in_b))
        cxns.append((b.param.out_b, tail.param.in_b))

    dag = PanelDag(title=title, doc='doc')
    dag.connections(cxns)

    return dag


def main():
    dag = make_fan_in_dag_cxns('fan in')
    dag.show()


if __name__ == '__main__':
    main()
