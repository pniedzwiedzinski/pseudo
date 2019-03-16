#!/usr/bin/env python

import sys

from pseudo.lexer import Lexer, EndOfFile

__author__ = u"Patryk Niedźwiedziński"
__version__ = "0.1"


def main():
    with open(sys.argv[1]) as fp:
        text_input = fp.read()

    lexer = Lexer(text_input)

    while True:
        try:
            x = lexer.read_next()
        except EndOfFile:
            break
        print(x)