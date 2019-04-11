#!/usr/bin/env python

"""pseudocode interpreter

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

    If lexer reach the end of input, the `parser.lexer.EndOfFile` exception will be raised.
"""

import sys

from pseudo.lexer import Lexer, EndOfFile

__author__ = "Patryk Niedźwiedziński"
__version__ = "0.7.2"


def main():
    instructions = []

    x = None
    with open(sys.argv[1]) as fp:
        text_input = fp.read()

    lexer = Lexer(text_input)

    while True:
        try:
            x = lexer.read_next(prev=x)
        except EndOfFile:
            break
        instructions.append(x)
    for i in instructions:
        i.eval()
