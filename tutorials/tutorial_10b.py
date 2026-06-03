#!/usr/bin/env python

import param
from sier2 import Block, Dag


class First(Block):
    """Create soem data."""

    out_collection = param.Dict(default={})

    def __init__(self):
        super().__init__()
        self.count = 0

    def execute(self):
        tmp_collection = {}
        self.count += 1
        print(f'execute {self.name}: {self.count}')
        tmp_collection[self.count] = 'X' * self.count
        self.out_collection = tmp_collection
        print(f'collection: {self.out_collection}')


class Display(Block):
    """Display some data."""

    in_things = param.Dict()

    def execute(self):
        print(f'\nexecute {self.name}')
        for k, v in self.in_things.items():
            print(f'Key: {k}, Value: {v}')


if __name__ == '__main__':
    first = First()
    display = Display()
    dag = Dag([(first.param.out_collection, display.param.in_things)], title='Mutation', doc='Mutating, not assigning.')

    print('\n---- Execute the dag.')
    dag.execute()

    print('\n---- Execute the dag again.')
    dag.execute()
