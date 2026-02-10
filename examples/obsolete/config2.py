from sier2 import Block, Connection, Dag, Library, Config

import param

class PrintBlock(Block):
    """Just print something."""
    in_string = param.String(label='String to print', doc='Just print something', allow_None=True)

    def execute(self):
        print(f'Result: {self.in_string}')

if __name__=='__main__':
    # Update the config for ConfigurableBlock using ExampleConfig.
    #
    Config.update(config_block='sier2_tutorial.blocks:ExampleConfig')

    cb = Library.get_block('sier2_tutorial.blocks:ConfigurableBlock')()
    pb = PrintBlock()

    dag = Dag(doc='Demonstrate configuration of a block', site='Example', title='Configuration')
    dag.connect(cb, pb, Connection('out_output', 'in_string'))

    block = dag.execute()
    while block is not None:
        block = dag.execute_after_input(block)
