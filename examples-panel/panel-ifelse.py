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
# However, what is actually happening is that all of the "next" blocks are being executed,
# no matter what. This appears to be caused in
# _panel.py line 396 (inside def on_continue(_event)):
#
#   w.param.trigger(*w._block_out_params)
#
# Because all of the out params are being triggered, both sets of connections are being
# triggered, so both block paths are being executed.
#
# Removing that line seems to fix the problem, but who knows what else that changes?
# The comment above that line indicates that we want to do this, but this may be a hangover
# from an earlier version that worked differently. I feel we *don't* want to do this,
# because it breaks this block.
#

from sier2 import Block, Dag, Connection
from sier2.panel import PanelDag
import param

import panel as pn
import holoviews as hv

from datetime import datetime
import sys
import time

hv.extension('bokeh', inline=True)

class IfElseBlock(Block):
    """Demonstrate an if-else block.
    """

    in_if = param.Boolean(label='Go to tail?', doc='Go directly to tail?')
    out_next_if = param.Boolean(label='Out if Next', doc='If Next thing')
    out_tail_if = param.Boolean(label='Out if Tail', doc='If Tail thing')

    in_dt = param.Date(label='In DT', doc='In Datetime')
    out_next_dt = param.Date(label='Out DT Next', doc='Out Datetime Next thing')
    out_tail_dt = param.Date(label='Out DT Tail', doc='Out Datetime Tail thing')

    def __init__(self, name, pause=False):
        super().__init__(name=name, wait_for_input=pause)

    def prepare(self):
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

        if self.name=='tail':
            print('----')

def main():
    # Run with "python panel-ifelse.py p" to use panel, without "p" to use CLI.
    #
    use_panel = True # len(sys.argv)>1 and sys.argv[1]=='p'

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
        dag.connect(b1, b2,
            Connection('out_next_if', 'in_if'),
            Connection('out_next_dt', 'in_dt')
        )

    # Connect the head block to the "next" block and the tail block.
    #
    dag.connect(head, blocks[0], Connection('out_next_if', 'in_if'), Connection('out_next_dt', 'in_dt'))
    dag.connect(head, blocks[-1], Connection('out_tail_if', 'in_if'), Connection('out_tail_dt', 'in_dt'))

    if use_panel:
        print('Show')
        dag.show()
    else:
        print('Execute')
        b = dag.execute()
        head.in_if = True
        dag.execute_after_input(b)

if __name__=='__main__':
     main()
