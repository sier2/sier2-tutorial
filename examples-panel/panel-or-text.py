#

# This example demonstrates that a dag can be run in textual context
# and panel context.
#
# The Calc block just sets its output from its inputs via a lengthy
# calculation, and does not implement a __panel__() method.
# In text context, nothing happens, but in Panel context,
# a default __panel__() method containing an indefinite progress bar
# is provided, and made active while the block is executing.
#

from sier2 import Block, Dag, Connection
from sier2.panel import PanelDag
import param
import panel as pn
import sys
import time

class In(Block):
    """Input values."""

    in_a = param.Number(label='a')
    in_b = param.Number(label='b')
    out_a = param.Number(label='a')
    out_b = param.Number(label='b')

    def execute(self):
        self.out_a = self.in_a
        self.out_b = self.in_b

    def __panel__(self):
        aw = pn.widgets.FloatInput.from_param(
            self.param.in_a,
            name='input a'
        )
        bw = pn.widgets.FloatInput.from_param(
            self.param.in_b,
            name='input b'
        )

        return pn.Row(aw, bw)

class Calc(Block):
    """Calculate values.

    This block deliberately does not implement a __panel__() method.

    The print calls in execute() are purely for indicative purposes.
    """

    in_a = param.Number(label='a')
    in_b = param.Number(label='b')
    out_result = param.Number(label='result')

    def execute(self):
        print(f'calc {self.in_a=} {self.in_b=}')

        delay = 2
        print(f'Pretend to work ... sleep({delay})')
        time.sleep(delay)

        self.out_result = self.in_a + self.in_b
        print('calc end')

class Out(Block):
    """Display result."""

    in_result = param.Number(label='result')

    def __panel__(self):
        rw = pn.widgets.FloatInput.from_param(
            self.param.in_result,
            name='Result'
        )

        return pn.Row(rw)

def make_dag(DagType):
    in_block = In(name='do inputs', wait_for_input=True)
    calc_block = Calc(name='do calc')
    out_block = Out(name='do result')

    dag = DagType(title='The dag', doc='Demonstrate panel-less blocks.')
    dag.connect(
        in_block, calc_block,
        Connection('out_a', 'in_a'),
        Connection('out_b', 'in_b')
    )
    dag.connect(
        calc_block, out_block,
        Connection('out_result', 'in_result')
    )

    return dag

def main(context):
    is_text = context=='text'

    dag = make_dag(Dag if is_text else PanelDag)

    # Fetch the input block by name.
    #
    inb = dag.block_by_name('do inputs')
    inb.in_a = 8
    inb.in_b = 9

    if is_text:
        # The first block is an input block, so we have to
        # provide input and resume executing the dag.
        #
        print('Execute dag and provide input ...')
        b = dag.execute()
        assert b is inb # Checking that the block is what we think it is.
        inb.in_a = 8
        inb.in_b = 9
        dag.execute_after_input(b)

        r = dag.block_by_name('do result').in_result
        print(f'Result: {r}')
    else:
        dag.show()

if __name__=='__main__':
    context = sys.argv[1] if len(sys.argv)>1 else None
    if context in ('text', 'panel'):
        main(context)
    else:
        print('Specify "text" or "panel" as an argument.')
