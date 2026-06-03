#!/usr/bin/env python

import sys
from typing import Any

import param
from sier2 import Block, Dag

# Demonstrates a "configuration" solution without a Config block.
#


class Note(Block):
    """Add a note to a word."""

    out_note = param.String()

    def __init__(self, config: dict[str, Any], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

    def execute(self):
        word = self.config['word']
        self.out_note = f'The word of the day is {word}.'


class Highlight(Block):
    """Highlight a word in a string."""

    in_string = param.String(default=None)
    out_string = param.String()

    def __init__(self, config: dict[str, Any], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

    def execute(self):
        word = self.config['word']
        highlight = f'"{word.upper()}"'
        self.out_string = self.in_string.replace(word, highlight)


class Display(Block):
    """Display a string."""

    in_word = param.String(default='NO-WORD')
    in_value = param.String(default='NO-VALUE')

    def __init__(self, config: dict[str, Any], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

    def execute(self):
        word = self.config['word']
        print(f'DISPLAY: {self.in_value} (from {word})')


if __name__ == '__main__':
    # Read a word from the command line.
    #
    if len(sys.argv) != 2:
        print('Please provide a word as the command argument.')
        sys.exit(1)

    word = sys.argv[1]

    # Use a dictionary to make it look more "configuration-y".
    #
    config = {'word': word}

    # Pass the config to each successive block.
    #
    note = Note(config)
    highlight = Highlight(config)
    display = Display(config)

    dag = Dag(
        [(note.param.out_note, highlight.param.in_string), (highlight.param.out_string, display.param.in_value)],
        title='Config',
        doc='Using a configuration block.',
    )

    b = dag.execute()
