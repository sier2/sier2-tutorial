#

# Test an if:else branch.
#
# If in_if is True, the next block to be executed is the final (tail) block - only
# two blocks are executed, the head and tail.
#
# If in_if is False, the "next" and successive blocks are executed.
#
# This works by only setting the out params connected to the appropriate block.
#

import time
from datetime import datetime

import holoviews as hv
import param
from sier2 import Block, Connection, Dag
from sier2.panel import PanelDag

hv.extension('bokeh', inline=True)


class IfElseBlock(Block):
    """Demonstrate an if-else block."""

    in_if = param.Boolean(label='Go to tail?', doc='Go directly to tail?')
    out_next_if = param.Boolean(label='Out if Next', doc='If Next thing')
    out_tail_if = param.Boolean(label='Out if Tail', doc='If Tail thing')

    in_dt = param.Date(label='In DT', doc='In Datetime')
    out_next_dt = param.Date(label='Out DT Next', doc='Out Datetime Next thing')
    out_tail_dt = param.Date(label='Out DT Tail', doc='Out Datetime Tail thing')

    def __init__(self, name, pause=False):
        super().__init__(name=name, wait_for_input=pause)

    def prepare(self):
        self.is_input_valid_ = True
        if not self.in_dt:
            self.in_dt = datetime.now()

    def execute(self):
        # Sleep so we can see the lights doing their thing.
        #
        time.sleep(1)

        print(f'{self.name=} {self.in_dt=} {self.in_if=}')
        if self.in_if:
            print('to tail')
            self.out_tail_if = self.in_if
            self.out_tail_dt = self.in_dt
        else:
            print('to next')
            self.out_next_if = self.in_if
            self.out_next_dt = self.in_dt

        if self.name == 'tail':
            print('----')


def main_connect():
    # Run with "python panel-ifelse.py c" to use CLI, without "c" to use Panel
    #
    use_panel = True  # len(sys.argv)<1 or sys.argv[1]=='p'

    # Create a starting (head) block, and a list of successive blocks.
    # The last one in the list is the tail block.
    #
    head = IfElseBlock(name='head', pause=True)
    names = [f'IEB{i}' for i in range(1, 4)]
    names[-1] = 'tail'
    blocks = [IfElseBlock(name=name) for name in names]

    if use_panel:
        dag = PanelDag(doc='a dag', site='My site', title='if-else')
    else:
        dag = Dag(title='If-Else', doc='If-Else demo')

    for b1, b2 in zip(blocks, blocks[1:]):
        dag.connect(b1, b2, Connection('out_next_if', 'in_if'), Connection('out_next_dt', 'in_dt'))

    # Connect the head block to the "next" block and the tail block.
    #
    dag.connect(
        head, blocks[0], Connection('out_next_if', 'in_if'), Connection('out_next_dt', 'in_dt')
    )
    dag.connect(
        head, blocks[-1], Connection('out_tail_if', 'in_if'), Connection('out_tail_dt', 'in_dt')
    )

    if use_panel:
        print('Show')
        dag.show()
    else:
        print('Execute')
        b = dag.execute()
        head.in_if = True
        dag.execute_after_input(b)


def main_cxns():
    # Run with "python panel-ifelse.py c" to use CLI, without "c" to use Panel
    #
    use_panel = True  # len(sys.argv)<1 or sys.argv[1]=='p'

    # Create a starting (head) block, and a list of successive blocks.
    # The last one in the list is the tail block.
    #
    head = IfElseBlock(name='head', pause=True)
    names = [f'IEB{i}' for i in range(1, 4)]
    names[-1] = 'tail'
    blocks = [IfElseBlock(name=name) for name in names]

    cxns = []

    for b1, b2 in zip(blocks, blocks[1:]):
        # dag.connect(b1, b2, Connection('out_next_if', 'in_if'), Connection('out_next_dt', 'in_dt'))
        cxns.append((b1.param.out_next_if, b2.param.in_if))
        cxns.append((b1.param.out_next_dt, b2.param.in_dt))

    # Connect the head block to the "next" block and the tail block.
    #
    # dag.connect(
    #     head, blocks[0], Connection('out_next_if', 'in_if'), Connection('out_next_dt', 'in_dt')
    # )
    # dag.connect(
    #     head, blocks[-1], Connection('out_tail_if', 'in_if'), Connection('out_tail_dt', 'in_dt')
    # )
    cxns.append((head.param.out_next_if, blocks[0].param.in_if))
    cxns.append((head.param.out_next_dt, blocks[0].param.in_dt))
    cxns.append((head.param.out_tail_if, blocks[-1].param.in_if))
    cxns.append((head.param.out_tail_dt, blocks[-1].param.in_dt))

    if use_panel:
        dag = PanelDag(doc='a dag', site='My site', title='if-else')
    else:
        dag = Dag(title='If-Else', doc='If-Else demo')

    dag.connections(cxns)

    if use_panel:
        print('Show')
        dag.show()
    else:
        print('Execute')
        b = dag.execute()
        head.in_if = True
        dag.execute_after_input(b)


if __name__ == '__main__':
    main_cxns()
