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
import os
import click
import datetime
from pseudo.lexer import Lexer, EndOfFile
from pseudo.utils import append


__author__ = "Patryk Niedźwiedziński"
__version__ = "0.7.4"


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
        sys.exit(1)
    instructions = []

    with open(file) as fp:
        text_input = fp.read()

    instructions = compile(text_input)

    for i in instructions:
        try:
            i.eval()
        except Exception as err:
            now = datetime.datetime.now().strftime("%H-%M-%S-%d-%m-%Y")
            with open(f"crash/{now}.log", "w") as fp:
                fp.write(str(err))
            print("⚠️  Error: \n\tRuntime error has occurred!\n")
            print(
                "Wow! You encountered a bug! Please tell me how did you do that on https://github.com/pniedzwiedzinski/pseudo/issues\n"
            )
            print(f"Error message was copied to {os.getcwd()}/crash/{now}.log")
            exit(1)


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
        instructions = append(instructions, x)
    return instructions
