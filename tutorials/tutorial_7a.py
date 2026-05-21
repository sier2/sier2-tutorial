#!/usr/bin/env python

import random

import param
from sier2 import Block, Dag

# Demonstrates multiple incoming connections.
#


class Range(Block):
    """Provide a range for random numbers."""

    out_max = param.Integer(bounds=(0, None))

    def execute(self):
        self.out_max = 10


class RandomInt(Block):
    """A random integer between 1 and the specified maximum inclusive."""

    in_max = param.Integer(bounds=(0, None))
    out_max = param.Integer(bounds=(0, None))
    out_r = param.Integer()

    def execute(self):
        self.out_r = random.randint(1, self.in_max)
        print(f'Random {self.name} = {self.out_r}')


class Add(Block):
    """Add two integers."""

    in_a = param.Integer()
    in_b = param.Integer()
    out_result = param.Integer()

    def execute(self):
        print('Adding:')
        print(f'{self.in_a=}')
        print(f'{self.in_b=}')
        self.out_result = self.in_a + self.in_b


class AddWithCheck(Block):
    """Add two integers."""

    in_a = param.Integer(default=None)
    in_b = param.Integer(default=None)
    out_result = param.Integer()

    def execute(self):
        if self.in_a is None or self.in_b is None:
            return

        print('Adding:')
        print(f'{self.in_a=}')
        print(f'{self.in_b=}')
        self.out_result = self.in_a + self.in_b


class Display(Block):
    """Display a result."""

    in_result = param.Integer()

    def execute(self):
        print(f'\n+ Result is {self.in_result}\n')


if __name__ == '__main__':
    range = Range()
    ra = RandomInt(name='A')
    rb = RandomInt(name='B')
    add = Add()
    display = Display()

    dag = Dag(
        [
            (range.param.out_max, ra.param.in_max),
            (ra.param.out_r, add.param.in_a),
            (ra.param.out_r, rb.param.in_max),
            (rb.param.out_r, add.param.in_b),
            (add.param.out_result, display.param.in_result),
        ],
        title='Add',
        doc='Add two random numbers.',
    )

    dag.execute()
