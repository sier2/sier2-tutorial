from sier2 import Block, Dag, Connection
import param

class PassThrough(Block):
    """Pass an in string to an out string."""

    in_string = param.String(label='Input string', doc='in')
    out_string = param.String(label='Output string', doc='out')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self):
        print(f'In execute {self.name=}, {self.in_string=}')
        self.out_string = self.in_string

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
    b1 = PassThrough(name='pass')
    b2 = Pause(name='pause')

    dag = Dag(title='Test prepare', doc='input params set before prepare()')
    dag.connect(b1, b2, Connection('out_string', 'in_string'))

    b1.out_string = 'this'
    b = dag.execute()
    dag.execute_after_input(b)

    print(f'{b2.out_string=}')

if __name__=='__main__':
    main()
