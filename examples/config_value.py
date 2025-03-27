#

# Demonstrate using values from a configuration file.
# We don't want to disturb the default config, so we'll load a temporary.
#

from pathlib import Path
import tempfile

from sier2 import Block, Config
import param

CONFIG_NAME = 'test.ini'

class ConfigName(Block):
    """Demonstrate reading a config value."""

    out_name = param.String(label='Name', doc='A name read from a config file')

    def execute(self):
        config = self.get_config()
        self.out_name = config['name']

def main():
    tmp_config = Path(tempfile.gettempdir()) / CONFIG_NAME
    with open(tmp_config, 'w') as f:
        print("""
[block.__main__.ConfigName]
name = 'Taylor Swift'
""", file=f)

    try:
        Config.location = tmp_config

        cn = ConfigName()
        cn.execute()
    finally:
        tmp_config.unlink()

    print(f'Value read from config file: "{cn.out_name}"')
    assert cn.out_name=='Taylor Swift'

if __name__=='__main__':
    main()
