"""
This module contains class of stream object used to iterate over input.
"""

__author__ = u"Patryk Niedźwiedziński"


class Stream():
    """Class for input stream."""

    def __init__(self, inp):
        """
        Constructor for class.

        args:
            - inp - string with pseudocode
        """
        self.inp = inp.split("\n")
        self.line = 1
        self.col = 1

    def next_line(self):
        """Switch cursor to next line."""
        self.line += 1
        self.col = 1
    
    def next(self):
        """Switch cursor to next col and return char."""
        self.col += 1
        return self.inp[self.line-1][self.col-2]

    def peek(self):
        """Returns next char without moving cursor."""
        return self.inp[self.line-1][self.col-1]

    def eol(self):
        """Returns true if next char is '\n'."""
        try:
            self.peek()
        except IndexError:
            return True
        return False

    def eof(self):
        """Returns true if next char is end of file."""
        if not self.eol():
            return False
        try:
            self.inp[self.line][0]
        except IndexError:
            return True
        return False

    def throw(self, error):
        """Error handler."""
        #raise Exception(f"\n\n⚠️  Error on line {self.line+1}:\n\t{error}")
        print(f"⚠️  Error on line {self.line+1}:\n\t{error}")
        exit()


class EndOfFile(Exception):
    """Exception indicating that parsing ends."""
    pass