#!/usr/bin/env python

# Demonstrate creating a less-than-basic dag.
# Building the dag is just building a list of param connections.
# Look at the graph in the template sidebar.
#

import itertools
import time

import param
from sier2 import Block
from sier2.panel import PanelDag


class PassBlock(Block):
    """A simple block."""

    in_b = param.Boolean(label='inb')
    out_b = param.Boolean(label='outb')

    def execute(self):
        time.sleep(0.5)
        self.out_b = self.in_b


def make_binary_tree_next_level(level: list[Block]):
    """Given a level of blocks in a list, create the next level of blocks in a binary tree."""

    n2 = len(level) * 2
    next_level = []
    for i in range(n2):
        pb = PassBlock(name=f'B{n2}/{i}')
        next_level.append(pb)

    return next_level


def main():
    pb = [PassBlock(name='B1/0', wait_for_input=True)]
    levels = [pb]
    for _ in range(3):
        pb = make_binary_tree_next_level(pb)
        levels.append(pb)

    cxns = []
    for l1, l2 in itertools.pairwise(levels):
        for i in range(len(l2)):
            cxns.append((l1[i // 2].param.out_b, l2[i].param.in_b))

    tail = PassBlock(name='binary tree to a single block')
    for b in pb:
        cxns.append((b.param.out_b, tail.param.in_b))

    dag = PanelDag(cxns, title='Dag title', doc='doc')

    dag.show()


if __name__ == '__main__':
    main()
