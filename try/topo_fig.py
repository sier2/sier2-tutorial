#

# Draw the dag as a topologically sorted line of blocks,
# with lines / curves connecting sources and destinations.
#
# The tree drawing algorithm we curently use just doesn't work.
# It isn't difficult to create dags that do not draw correctly.
#
# This is my controversial alternative. Dags are always drawn top-left to
# bottom-right. The order of the blocks is the topological sort
# (see Dag.get_sorted()), with lines connecting blocks that are next to
# each other, and (bezier) curves connecting more distance blocks.
# The direction of the lines / curves is always toward bottom-right,
# so arrowheads aren't required.
#
# I suspect that the amount of effort required to make the current layout
# work is much more than we want to do. This alternative may or may not be
# more or less readable, but it is correct as far as I can tell,
# so by definition it's better.
#
# To draw your own dag, add a `make_my_dag` function that returns a dag,
# then update the plots list at the end.
#
# Since this in done using bokeh, it should be possible to update the block
# colors as the dag executes.
#

from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.core.enums import RenderLevel
from bokeh.models.annotations.arrows import ArrowHead
from bokeh.layouts import column
import bokeh.palettes as pals

import math
import random

from sier2 import Block, Dag, Connection
import param

import tempfile
output_file(f'{tempfile.gettempdir()}/sier2_plot.html', mode='inline')

##########
# Example dags.
##########

class PassBlock(Block):
    """A simple block."""
    in_b = param.Boolean(label='inb')
    out_b = param.Boolean(label='outb')

    def execute(self):
        self.out_b = self.in_b

def make_boring_dag():
    dag = Dag(title='boring', doc='boring')
    h = PassBlock(name='head')
    t = PassBlock(name='tail')
    dag.connect(h, t, Connection('out_b', 'in_b'))

    return dag

def make_if_else_dag():

    # Create a starting (head) block, and a list of successive blocks.
    # The last one in the list is the tail block.
    #
    head = PassBlock(name='head')
    names = [f'IEB{i}' for i in range(1, 4)]
    names[-1] = 'tail'
    blocks = [PassBlock(name=name) for name in names]

    dag = Dag(title='If-Else', doc='If-Else demo')

    for b1, b2 in zip(blocks, blocks[1:]):
        dag.connect(b1, b2,
            Connection('out_b', 'in_b')
        )

    # Connect the head block to the "next" block and the tail block.
    #
    dag.connect(head, blocks[0], Connection('out_b', 'in_b'))
    dag.connect(head, blocks[-1], Connection('out_b', 'in_b'))

    return dag

def make_multi_tail_dag():
    dag = Dag(title='multi-tail', doc='single head, fan out tail')
    head = PassBlock(name='head')
    for i in range(5):
        m = PassBlock(name=f'tail{i}')
        dag.connect(head, m, Connection('out_b', 'in_b'))

    return dag

def make_tree_dag():
    dag = Dag(title='binary tree', doc='doc')
    head = PassBlock(name='head')
    l2 = PassBlock(name='L2')
    r2 = PassBlock(name='R2')
    ll3 = PassBlock(name='LL3')
    lr3 = PassBlock(name='LR3')
    rl3 = PassBlock(name='RL3')
    rr3 = PassBlock(name='RR3')

    dag.connect(head, l2, Connection('out_b', 'in_b'))
    dag.connect(head, r2, Connection('out_b', 'in_b'))
    dag.connect(l2, ll3, Connection('out_b', 'in_b'))
    dag.connect(l2, lr3, Connection('out_b', 'in_b'))
    dag.connect(r2, rl3, Connection('out_b', 'in_b'))
    dag.connect(r2, rr3, Connection('out_b', 'in_b'))

    return dag

def make_tree_root_dag():
    tail = PassBlock(name='binary tree to a single block')
    dag = make_tree_dag()
    dag.connect(dag.block_by_name('LL3'), tail, Connection('out_b', 'in_b'))
    dag.connect(dag.block_by_name('LR3'), tail, Connection('out_b', 'in_b'))
    dag.connect(dag.block_by_name('RL3'), tail, Connection('out_b', 'in_b'))
    dag.connect(dag.block_by_name('RR3'), tail, Connection('out_b', 'in_b'))

    return dag

def make_long_dag():
    dag = Dag(title='long', doc='single path')
    head = PassBlock(name='head')
    prev = head
    for i in range(1, 10):
        m = PassBlock(name=f'block{i}')
        dag.connect(prev, m, Connection('out_b', 'in_b'))
        prev = m

    return dag

##########
# The plotting code.
##########

def draw_dag(dag, title):
    topo_blocks = dag.get_sorted()

    p = figure(width=400, height=400, title=title, #toolbar_location=None,
        tooltips='@name',
        aspect_ratio=1,
        # Ranges must be equal.
        x_range=(-1, len(topo_blocks)), y_range=(-1, len(topo_blocks))
        #, tools='hover'
    )
    curdoc().theme = 'dark_minimal'

    n = len(topo_blocks)
    data = {
        'name': [block.name for block in topo_blocks],
        'x': list(range(n)),
        'y': list(range(n-1, -1, -1)),
        'color': random.choices(pals.DarkText, k=n)
    }
    xys = {name: (x,y) for name, x, y in zip(data['name'], data['x'], data['y'])}

    SIZE = 0.25

    c = p.circle(
        source=data,
        x='x', y='y',
        radius=SIZE,
        # alpha=0,
        # line_alpha=1,
        color='color',
        # line_color='line_color',
        radius_units='data'
    )

    def next_to_topo(topo_blocks, b1, b2):
        ix = topo_blocks.index(b1)

        return ix<len(topo_blocks) and  topo_blocks[ix+1]==b2

    lc = 'steelblue'
    lw = 2
    side = 1
    h = math.sin(math.pi/4)*SIZE
    for b1, b2 in dag._block_pairs:
        x0, y0 = xys[b1.name]
        x1, y1 = xys[b2.name]
        if next_to_topo(topo_blocks, b1, b2):
            # Draw a line directly from source to destination.
            #
            x0 += h
            y0 -= h
            x1 -= h
            y1 += h
            p.line([x0, x1], [y0, y1], line_color=lc, line_width=lw)
        else:
            # Bezier curve - width dependent on the distance between blocks.
            #
            delta = (x1-x0)*0.5
            x0 += h*side
            y0 += h*side
            x1 += h*side
            y1 += h*side
            cx0, cy0 = x0 + side*delta, y0 + side*delta
            cx1, cy1 = x1 + side*delta, y1 + side*delta

            # Draw a background line so overlapping curves look nice.
            #
            p.bezier([x0], [y0], [x1], [y1], [cx0], [cy0], [cx1], [cy1], line_color='#2b3035', line_width=lw+5)
            p.bezier([x0], [y0], [x1], [y1], [cx0], [cy0], [cx1], [cy1], line_color=lc, line_width=lw)

            side = -side
    text = p.text(source=data, x='x', y='y', text='name', anchor='center', color='white', alpha=0.5, level=RenderLevel.annotation)

    return p

dagb = make_boring_dag()
dagl = make_long_dag()
dag1 = make_if_else_dag()
dag2 = make_multi_tail_dag()
dag3 = make_tree_dag()
dag4 = make_tree_root_dag()

plots = [draw_dag(dag, dag.title) for dag in [dagb, dagl, dag1, dag2, dag3, dag4]]

show(column(*plots))
