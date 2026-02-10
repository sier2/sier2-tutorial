from sier2 import Block, Dag, Connection
import param
import random

class PassThrough(Block):
    """Pass an in string to an out string."""

    in_string = param.String(label='Input string', doc='in')
    out_string = param.String(label='Output string', doc='out')

    def execute(self):
        print(f'In execute {self.name=}, {self.in_string=}')
        self.out_string = f'{self.in_string} via {self.name}'

class Pause(Block):
    """Ensure that prepare() can see the in_string."""

    in_string = param.String(label='Input string (pause)', doc='in (pause)')
    out_string = param.String(label='Output string (pause)', doc='out (pause)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, wait_for_input=True, **kwargs)

    def prepare(self):
        print(f'In prepare {self.name=}, {self.in_string=}')

    def execute(self):
        print(f'In execute {self.name=}, {self.in_string=}')
        self.out_string = self.in_string

def main():
    passthru1 = PassThrough(name='PT1')
    pause_block = Pause(name='PAUSE')
    passthru2 = PassThrough(name='PT2')

    dag = Dag(title='Test prepare', doc='input params set before prepare()')
    dag.connect(passthru1, pause_block, Connection('out_string', 'in_string'))
    dag.connect(pause_block, passthru2, Connection('out_string', 'in_string'))

    # Set up the dag input.
    #
    passthru1.in_string = f'this{random.randint(0, 9)}'

    # Start the dag.
    #
    b = dag.execute()

    # The dag pause at the input block after running prepare
    # but before running execute.
    #
    assert b is pause_block
    print(f'Paused value: {pause_block.in_string}')

    # Modify the input before resuming the dag.
    #
    pause_block.in_string = f'[{pause_block.in_string} - paused]'
    dag.execute_after_input(b)

    print(f'{pause_block.out_string=}')
    print(f'Final result: {passthru2.out_string=}')

if __name__=='__main__':
    main()
