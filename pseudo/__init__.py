#!/usr/bin/env python

import sys

from pseudo.lexer import Lexer, EndOfFile

__author__ = "Patryk Niedźwiedziński"
__version__ = "0.5"


def main():
    x = None
    with open(sys.argv[1]) as fp:
        text_input = fp.read()

    lexer = Lexer(text_input)

    while True:
        try:
            x = lexer.read_next(prev=x)
        except EndOfFile:
            break
        x.eval()
