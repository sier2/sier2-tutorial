#!/usr/bin/env python

import param
from sier2 import Block, Dag

# Demonstrate an if-else branch.
#
# The ``IfEvenElseOdd`` block is connected to two output blocks by two different
# output params. Only one of the output params is updated, so only the block
# connected via that param will execute next.


class IfEvenElseOdd(Block):
    """An if-else branch."""

    in_input = param.Integer()
    out_even = param.Integer()
    out_odd = param.Integer()

    wait_for_input = True

    def execute(self):
        if self.in_input % 2 == 0:
            self.out_even = self.in_input
        else:
            self.out_odd = self.in_input


class Annotate(Block):
    """Annotate a number."""

    in_value = param.Integer(default=None)
    out_note = param.String()

    def execute(self):
        self.out_note = f'The number {self.in_value} is {self.name}.'


class Display(Block):
    """Display a string."""

    in_note = param.String()

    def execute(self):
        print(f'**** {self.in_note} ****')


if __name__ == '__main__':
    ifelse = IfEvenElseOdd()
    note_even = Annotate(name='even')
    note_odd = Annotate(name='odd')
    display = Display()

    dag = Dag(
        [
            (ifelse.param.out_even, note_even.param.in_value),
            (ifelse.param.out_odd, note_odd.param.in_value),
            (note_even.param.out_note, display.param.in_note),
            (note_odd.param.out_note, display.param.in_note),
        ],
        title='If-Else branch',
        doc='Demonstrate execution paths.',
    )

    b = dag.execute()
    b.in_input = int(input('Enter an integer: '))
    dag.execute_after_input(b)

    print(f'\n{note_even.in_value=}\n{note_odd.in_value=}')
