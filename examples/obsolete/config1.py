#

# Demonstrate using values from a configuration file.
# We don't want to disturb the default config, so we'll load a temporary.
#

from pathlib import Path
import tempfile

from sier2 import Block, Config
import param

CONFIG_NAME = 'test.ini'

class ConfigExample(Block):
    """Demonstrate reading a config value."""

    out_name = param.String(label='Name', doc='A name read from a config file')
    out_score = param.Number(label='Score', doc='The score')
    out_other = param.String(label='Another thing', doc='A key that does not exist')

    def execute(self):
        print(f'{self.block_key()=}')
        # We can get the entire config section as a dictionary ...
        #
        config = self.get_config()
        print(config)
        self.out_name = config['name']
        if 'other' in config:
            raise ValueError('Did not expect "other"')

        # ... or we can get individual items from the config section.
        #
        self.out_score = self.get_config_value('score')
        self.out_other = self.get_config_value('other', 'No config value')

def config_content(name: str, score=0):
    lines = [
        f'[block.__main__.{ConfigExample.__name__}]',
        f'name = "{name}"',
        f'score={score}'
    ]

    return '\n'.join(lines)

def main():
    name = 'Taylor Swift'
    score = 99

    # Use a temporary config file.
    # Write a config to it.
    #
    tmp_config = Path(tempfile.gettempdir()) / CONFIG_NAME
    with open(tmp_config, 'w') as f:
        print(config_content(name, 99), file=f)

    try:
        Config.update(location=tmp_config)

        # We don't need to run an entire dag, just the block will do.
        #
        cn = ConfigExample()
        cn.execute()
    finally:
        tmp_config.unlink()

    print(f'Values read from config file:\n  {cn.out_name=}\n  {cn.out_score=}\n  {cn.out_other=}')
    assert cn.out_name==name
    assert cn.out_score==score
    assert cn.out_other=='No config value'

if __name__=='__main__':
    main()
