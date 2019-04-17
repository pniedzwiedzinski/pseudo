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

    If lexer reach the end of input, the `pseudo.stream.EndOfFile` exception will be raised.
"""


__author__ = "Patryk Niedźwiedziński"
__version__ = "0.8.2a"

import datetime
import traceback
import gc
import os

from pseudo.lexer import Lexer
from pseudo.stream import EndOfFile
from pseudo.utils import append


def run(text_input: str, range_symbol: str = "..."):
    """Run pseudocode string"""
    try:
        instructions = compile(text_input, range_symbol)

        for i in instructions:
            i.eval()
    except Exception:
        now = datetime.datetime.now().strftime("%H-%M-%S-%d-%m-%Y")
        try:
            os.mkdir("crash")
        except FileExistsError:
            pass
        with open(f"crash/{now}.log", "w") as fp:
            fp.write(traceback.format_exc())
        print("⚠️  Error: \n\tRuntime error has occurred!\n")
        print(
            "Wow! You encountered a bug! Please tell me how did you do that on https://github.com/pniedzwiedzinski/pseudo/issues\n"
        )
        print(f"Error message was copied to {os.getcwd()}/crash/{now}.log")
        exit(1)


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
