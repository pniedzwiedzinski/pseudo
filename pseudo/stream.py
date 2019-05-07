"""
This module contains class of stream object used to iterate over input.
"""

from typing import Union
from sys import exit

from pseudo.type import EOL

__author__ = "Patryk Niedźwiedziński"


class Stream:
    """
    Stream is an object used to iterate over input. It is a little bit similar to queue.

    Attributes:
        - input: List of lines of code.
        - line: Number of current line. Counting from 1
        - col: Number of current column. Counting from 1
    """

    def __init__(self, input: str):
        """
        Split input string to list of lines and initialize object.

        args:
            - input - string with pseudocode
        """
        self.input = input.split("\n")
        self.input.append([""])
        self.line = 1
        self.col = 0

    def get_current_line(self):
        """Returns current line"""
        return self.input[self.line - 1]

    def next_line(self):
        """Move cursor to next line."""
        self.line += 1
        if self.line > len(self.input):
            raise EndOfFile
        self.col = 0

    def next(self) -> str:
        """Move cursor to next column and return char from this postion."""
        self.col += 1
        try:
            return self.input[self.line - 1][
                self.col - 1
            ]  # `-1` because list index starts at zero
        except IndexError:
            return EOL()

    def peek(self, size: int = 0) -> Union[str, EOL]:
        """
        Returns next char without moving cursor. If next char does not exists
        it returns EOL instance.

        args:
            - size: Size of shift, default `0`.
        """
        try:
            return self.input[self.line - 1][self.col + size]
        except IndexError:
            return EOL()

    def eol(self) -> bool:
        """Returns true if next char is end of line."""
        if isinstance(self.peek(), EOL):
            return True
        return False

    def eof(self) -> bool:
        """Returns true if next line is end of file and next char is end of line."""
        if not self.eol():
            return False
        if self.line == len(self.input) - 1:
            return True
        return False

    def throw(self, error: str):
        """Used to display error messages with line number. It stops the execution."""
        print(f"\n⚠️  Error on line {self.line}:")
        if "EOL" in error:
            print(f"\t'{self.input[self.line-2]}'")
        else:
            print(f"\t'{self.input[self.line-1]}'")
        print(f"{error}")
        exit(1)


class EndOfFile(Exception):
    """Exception indicating that parsing ends."""

    pass
