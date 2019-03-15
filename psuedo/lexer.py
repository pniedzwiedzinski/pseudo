"""
This module contains Lexer class using to tokenize stream.
"""

from stream import Stream, EndOfFile
from pseudo_types import String, Int, Operator, Statement, EOL

__author__ = u"Patryk Niedźwiedziński"


class Lexer():
    """
    Class to parse code.

    Attributes:
        i: A Stream instance with input code.
        keywords: A set of all keywords in pseudo.
        operators: A set of operators in pseudo.

    Usage:
    >>> lex = Lexer("pisz 12")
    >>> lex.read_next()
    Expression("pisz", args=[Number(12)])
    """

    def __init__(self, inp):
        """Inits Lexer with input."""
        self.i = Stream(inp)
        self.keywords = {"pisz"}
        self.operators = {"+", "-"}

    def is_keyword(self, string) -> bool:
        """Checks if given string is a keyword."""
        return string in self.keywords

    def is_alphabet(self, c) -> bool:
        """Checks if given char is from alphabet."""
        ascii = ord(c)
        return (ascii >= 65 and ascii <= 90) or (ascii >= 97 and ascii <= 122)

    def is_digit(self, c) -> bool:
        """Checks if given char is a digit."""
        return ord(c) >= 48 and ord(c) <= 57

    def is_operator(self, c) -> bool:
        """Checks if given char is an allowed operator."""
        return c in self.operators

    def is_not_keyword_end(self, c) -> bool:
        """
        Checks if given char breaks parsing a keyword.

        Example:
        `asd1` - This is one keyword.
        `asd1+asd2` - This is two keywords with `+` in between them.
        """
        return c != " " and not self.is_operator(c)

    def read(self, test, eol=True) -> str:
        """
        Read an element of code from the stream based on given test function.

        Args:
            test: Function used to determine if next char should be included
                to expression.
            eol: Optional variable, which switches `end of line` to be included
                to expression.
        """

        expression = ""
        while not self.i.eof() and test(self.i.peek()):
            if eol and self.i.eol():
                break
            expression += self.i.next()
        return expression

    def read_number(self) -> Int:
        """Read a number from the stream."""
        number = self.read(self.is_digit)
        return Int(number)

    def read_string(self) -> String:
        """Read a string from the stream."""
        self.i.next()
        string = self.read(lambda c: c != "\"")
        self.i.next()
        return String(string)

    def read_keyword(self) -> str:
        """Read a keyword from the stream."""
        keyword = self.read(self.is_not_keyword_end)
        return keyword

    def read_next(self):
        """Read next element from the stream and guess the type."""
        if self.i.eof():
            raise EndOfFile
        self.read(lambda c: c == "\n" or c == " ", eol=False)
        if self.i.eol():
            self.i.next_line()
            return EOL()
        c = self.i.peek()
        if c == "#":
            self.i.next_line()
            return self.read_next()

        if c == "\"" or c == "\'":
            return self.read_string()

        if self.is_digit(c):
            return self.read_number()

        if self.is_operator(c):
            self.i.next()
            return Operator(c)

        if self.is_alphabet(c):
            keyword = self.read_keyword()
            if self.is_keyword(keyword):
                args = []
                while not self.i.eol():
                    arg = self.read_next()
                    if not isinstance(arg, EOL):
                        args.append(arg)
                return Statement(keyword, args=args)
            self.i.throw(f"'{keyword}' is not defined")

        self.i.throw(f"Invalid character: '{c}'")

