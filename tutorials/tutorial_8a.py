#!/usr/bin/env python

import sys

import param
from sier2 import Block, Dag

# Demonstrates a "configuration" problem.
#


class Config(Block):
    """Configuration for this app.

    Could be passed as parameters, read from a file, etc.
    """

    in_word = param.String()
    out_word = param.String()

    wait_for_input = True

    def execute(self):
        self.out_word = self.in_word


class Note(Block):
    """Add a note to a word."""

    in_word = param.String(default=None)
    out_note = param.String()

    def execute(self):
        self.out_note = f'The word of the day is {self.in_word}.'


class Highlight(Block):
    """Highlight a word in a string."""

    in_string = param.String(default=None)
    in_word = param.String(default=None)
    out_string = param.String()

    def execute(self):
        highlight = f'"{self.in_word.upper()}"'
        self.out_string = self.in_string.replace(self.in_word, highlight)


class Display(Block):
    """Display a string."""

    in_word = param.String(default='NO-WORD')
    in_value = param.String(default='NO-VALUE')

    def execute(self):
        print(f'DISPLAY: {self.in_value} (from {self.in_word})')


if __name__ == '__main__':
    # Read a word from the command line.
    #
    word = sys.argv[1]

    config = Config()
    note = Note()
    highlight = Highlight()
    display = Display()

    dag = Dag(
        [
            (config.param.out_word, display.param.in_word),
            (config.param.out_word, note.param.in_word),
            (config.param.out_word, highlight.param.in_word),
            (note.param.out_note, highlight.param.in_string),
            (highlight.param.out_string, display.param.in_value),
        ],
        title='Config',
        doc='Using a configuration block.',
    )

    b = dag.execute()
    b.in_word = word
    dag.execute_after_input(b)
