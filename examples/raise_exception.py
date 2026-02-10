from sier2 import Block, BlockError, Dag, Connection
import param

class OneOut(Block):
    """One output parameter."""

    in_o = param.String()
    out_o = param.String()

    def execute(self):
        print(f'{self.in_o=}')
        self.out_o = self.in_o

class OneIn(Block):
    """One input parameter."""

    in_o = param.String()

    def execute(self):
        print(f'Raise exception with "{self.in_o}"')
        raise ValueError(f'This is an exception with value {self.in_o}')

oo = OneOut()
oi = OneIn()
dag = Dag(doc='Example: raise an exception in execute()', title='raise an exception')
dag.connect(oo, oi, Connection('out_o', 'in_o'))

try:
    oo.in_o = 'plugh'
    dag.execute()
except BlockError as e:
    print(f'\nCaught expected Block exception {e}')
    print(f'Actual cause: {type(e.__cause__)} {e.__cause__}')
except ValueError as e:
    print(f'Caught exception {e}')
else:
    print('Did not catch an exception.')

print('\nExecute dag without try .. except')

# After an exception is thrown, the dag is stopped from further execution.
# To start again, it must be unstopped.
#
dag.unstop()

oo.in_o = 'xyzzy'
dag.execute()
print('Done.')