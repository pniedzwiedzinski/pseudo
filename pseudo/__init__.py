"""
Writing actual code might be hard to understand for new-learners. Pseudocode is a tool
for writing algorithms without knowing how to code. This module contains classes and
methods for parsing pseudocode to AST and then evaluating it.

Example:
    If you installed this module with pip you can run pseudocode from file, i.e. to run
    `test.pdc` file type::

        $ pdc test.pdc

    If you want to parse it by your own you will need `pseudo.lexer.Lexer` instance.::

        from pseudo.lexer import Lexer

        lex = Lexer("x := 12")

        expression = lex.read_next()
        print(expression)

    If lexer reach the end of input, the `pseudo.stream.EndOfFile` exception will be raised.
"""


__author__ = "Patryk Niedźwiedziński"
__version__ = "0.11.0dev"


import gc

from pseudo.lexer import Lexer
from pseudo.stream import EndOfFile
from pseudo.utils import append


def compile(text_input: str, range_symbol: str = "...") -> list:
    """Compile from string to list of operations."""

    lexer = Lexer(text_input)
    lexer.range_symbol = range_symbol

    x = None
    instructions = []

    while True:
        try:
            x = lexer.read_next(prev=x)
        except EndOfFile:
            break
        instructions = append(instructions, x)
    del lexer
    gc.collect()
    return instructions
