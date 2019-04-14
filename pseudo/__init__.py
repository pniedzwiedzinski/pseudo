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
import click
from pseudo.lexer import Lexer, EndOfFile

__author__ = "Patryk Niedźwiedziński"
__version__ = "0.7.3"


@click.command()
@click.option("--version", "-v", help="Display version", is_flag=True)
@click.argument("file", type=click.Path(exists=True), required=False)
def main(file, version):
    """Run pseudocode file."""

    if version:
        print(__version__)
        sys.exit()

    if file is None:
        click.echo('⚠️  Error: Missing argument "FILE".')
        sys.exit()
    instructions = []

    with open(file) as fp:
        text_input = fp.read()

    instructions = compile(text_input)

    for i in instructions:
        i.eval()


def compile(text_input: str) -> list:
    """Compile from string to list of operations."""

    lexer = Lexer(text_input)

    x = None
    instructions = []

    while True:
        try:
            x = lexer.read_next(prev=x)
        except EndOfFile:
            break
        instructions.append(x)
    return instructions
