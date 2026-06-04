#!/usr/bin/env python

# A basic demonstration of connecting blocks into a dag.
#
# The first block (O) takes an integer and a string, and outputs string * int.
# The second block (P) takes a string and outputs an integer - the lenth of the string.
# The third block (Q) takes an integer output, and outputs the input+1.
# The fourth block (R) prints its input.
#

import param
from sier2 import Block, Dag

# from sier2.debug import Debug


class O(Block):
    """A block that converts an int to a string of that length."""

    in_oi = param.Integer(label='input P int', bounds=(0, None))
    in_os = param.String(label='input P str', default='')
    out_o = param.String(label='output P')

    def execute(self):
        self.out_o = self.in_os * self.in_oi


class P(Block):
    """A block with a single output parameter."""

    in_p = param.String(label='input P')
    out_p = param.Integer(label='output P')

    def execute(self):
        self.out_p = len(self.in_p)


class Q(Block):
    """A block with a single input and a single output."""

    in_q = param.Integer(label='Int 2', doc='input Q')
    out_q = param.Integer(label='Int 3', doc='output Q')

    def execute(self):
        print(f'{self.name} acting {self.in_q=}')
        self.out_q = self.in_q + 1


class R(Block):
    """A block with a single input."""

    in_r = param.Integer(label='Int 4', doc='input R')

    def execute(self):
        print(f'{self.name} acting {self.in_r=}')


o = O()
p = P()
q = Q()
r = R()

dag = Dag(
    [
        (o.param.out_o, p.param.in_p),
        (p.param.out_p, q.param.in_q),
        (q.param.out_q, r.param.in_r),
    ],
    doc='Simple dag',
    title='simple dag',
)

# dag._debug = Debug.DAG_QUEUE | Debug.BLOCK_PARAMS

start_number = 4
start_string = 'ZX'

o.in_oi = start_number
o.in_os = start_string
dag.execute()

print(f'''
    {o.out_o= } (expecting {start_string * start_number!r})
    {p.in_p = } (expecting {start_string * start_number!r})
    {p.out_p= } (expecting {start_number})
    {q.in_q = } (expecting {start_number})
    {q.out_q= } (expecting {start_number + 1})
    {r.in_r = } (expecting {start_number + 1})
''')
