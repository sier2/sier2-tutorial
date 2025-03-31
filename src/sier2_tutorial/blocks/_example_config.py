from sier2 import Block
import param

class ExampleConfig(Block):
    """A block that provides an example config.

    Make sure that --config is used so the default config is not overwritten.

    A config block can get the configuration from anywhere (an https endpoint,
    a local file), but this one is hard-coded, depending on the input arg.
    """

    in_arg = param.String(label='config arg', doc='An input to the config example', allow_None=True)
    out_config = param.String(label='new config', doc='The contents of an ini file')

    def execute(self):
        arg = f'Config from in_arg is "{self.in_arg}"' if self.in_arg else 'This is a default config.'

        # The ini file content to be returned to the caller.
        #
        ini = f'''
[block.sier2_tutorial.blocks:ConfigurableBlock]
output = 'String from {ExampleConfig.__name__}'
arg = '{arg}'
'''

        self.out_config = ini
