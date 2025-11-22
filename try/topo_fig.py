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
# Since this is done using bokeh, it should be possible to update the block
# colors as the dag executes.
#

from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.core.enums import RenderLevel
from bokeh.models import HoverTool
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

def make_so_dag():
    """https://stackoverflow.com/questions/39644616/is-there-a-2d-layout-algorithm-for-dags-that-allows-the-positions-on-one-axis-to"""

    blocks = [PassBlock(name=f'Block{i}') for i in range(9)]
    c = Connection('out_b', 'in_b')
    dag = Dag(title='Example', doc='from SO')
    dag.connect(blocks[0], blocks[1], c)
    dag.connect(blocks[0], blocks[3], c)

    dag.connect(blocks[1], blocks[2], c)
    dag.connect(blocks[1], blocks[6], c)

    dag.connect(blocks[3], blocks[4], c)
    dag.connect(blocks[3], blocks[5], c)
    dag.connect(blocks[3], blocks[8], c)

    dag.connect(blocks[4], blocks[7], c)
    dag.connect(blocks[4], blocks[8], c)

    dag.connect(blocks[5], blocks[6], c)

    dag.connect(blocks[6], blocks[7], c)

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

def make_binary_tree_dag(title):
    dag = Dag(title=title, doc='doc')
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

def make_tree_tail_dag():
    tail = PassBlock(name='binary tree to a single block')
    dag = make_binary_tree_dag('binary tree to tail')
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

def count_param(block, prefix):
    return sum(1 for p in block.param if p.startswith(prefix))

def draw_dag(dag, title):
    topo_blocks = dag.get_sorted()
    n = len(topo_blocks)

    fig = figure(width=400, height=400, title=title, #toolbar_location=None,
        # tooltips=[('Name', '@name'), ('In', '@icount'), ('Out', '@ocount')],
        aspect_ratio=1,
        # Ranges must be equal.
        x_range=(-1, n), y_range=(-1, n)
        #, tools='hover'
    )
    curdoc().theme = 'dark_minimal'

    hover = HoverTool(tooltips=[('Name', '@name'), ('In', '@icount'), ('Out', '@ocount')])
    fig.add_tools(hover)

    data = {
        'name': [block.name for block in topo_blocks],
        'x': list(range(n)),
        'y': list(range(n-1, -1, -1)),
        'color': random.choices(pals.DarkText, k=n),
        'icount': [count_param(block, 'in_') for block in topo_blocks],
        'ocount': [count_param(block, 'out_') for block in topo_blocks],
    }
    xys = {name: (x,y) for name, x, y in zip(data['name'], data['x'], data['y'])}

    SIZE = 0.25

    circle = fig.circle(
        source=data,
        x='x', y='y',
        radius=SIZE,
        # alpha=0,
        # line_alpha=1,
        color='grey',
        # line_color='line_color',
        radius_units='data'
    )

    def next_to_topo(topo_blocks, b1, b2):
        """Are blocks b1 and b2 next to each other in the topological sort?"""
        ix = topo_blocks.index(b1)

        return ix<len(topo_blocks) and topo_blocks[ix+1]==b2

    lc = 'steelblue'
    lw = 2
    side = True
    heads = []
    OFFSET = 1.5 * SIZE
    h = math.sin(math.pi/4) * OFFSET
    for b1, b2 in dag._block_pairs:
        x0, y0 = xys[b1.name]
        x1, y1 = xys[b2.name]
        if next_to_topo(topo_blocks, b1, b2):
            # Draw a line directly from source to destination.
            #
            x0 += h
            y0 -= h
            x1 -= h + h*OFFSET
            y1 += h + h*OFFSET
            angle = -math.pi/12
            fig.line([x0, x1], [y0, y1], line_color=lc, line_width=lw)
        else:
            # Define how far out the Bezier curve control points are.
            #
            c = (x1-x0) * 0.75

            if side:
                # Below.
                cx0, cy0 = x0, y0-c
                cx1, cy1 = x1-c, y1
                x0, y0 = x0, y0 - OFFSET
                x1, y1 = x1 - OFFSET*1.5, y1
                angle = -math.pi/2
            else:
                # Above.
                cx0, cy0 = x0+c, y0
                cx1, cy1 = x1, y1+c
                x0, y0 = x0 + OFFSET, y0
                x1, y1 = x1, y1 + OFFSET*1.5
                angle = -math.pi/3

            # # Plot the Bezier control points for debugging.
            # #
            # p.circle([cx0, cx1], [cy0, cy1], radius=0.05, color='red')

            # Draw a background line under the actual line so overlapping curves look nice.
            #
            fig.bezier([x0], [y0], [x1], [y1], [cx0], [cy0], [cx1], [cy1], line_color='#2b3035', line_width=lw+5)
            fig.bezier([x0], [y0], [x1], [y1], [cx0], [cy0], [cx1], [cy1], line_color=lc, line_width=lw)

        heads.append((x1, y1, angle))
        side = not side

    # text = p.text(source=data, x='x', y='y', text='name', anchor='center', color='white', alpha=0.5, level=RenderLevel.annotation)

    # Draw the triangles to look like arrowheads.
    #
    xtri, ytri, atri = list(zip(*heads))
    fig.scatter(xtri, ytri, marker='triangle', angle=atri, color=lc, size=10)

    hover.renderers = [circle]

    return fig

dagb = make_boring_dag()
dagso = make_so_dag()
dagl = make_long_dag()
dag1 = make_if_else_dag()
dag2 = make_multi_tail_dag()
dag3 = make_binary_tree_dag('binary tree')
dag4 = make_tree_tail_dag()

plots = [draw_dag(dag, dag.title) for dag in [dagb, dagso, dagl, dag1, dag2, dag3, dag4]]

show(column(*plots))
