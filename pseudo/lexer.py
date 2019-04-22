"""
This module contains Lexer class using to tokenize stream.
"""

from pseudo.stream import Stream, EndOfFile
from pseudo.utils import append
from pseudo.type.numbers import Int, is_digit, read_number
from pseudo.type.string import String, read_string
from pseudo.type.bool import Bool, read_bool
from pseudo.type.conditional import Condition, read_if
from pseudo.type.operation import (
    Operation,
    Operator,
    OPERATORS,
    OPERATOR_KEYWORDS,
    read_operator,
    is_operator,
)
from pseudo.type.variable import Variable, Assignment, Increment
from pseudo.type.loop import Loop, Iterator, read_for, read_while
from pseudo.type import Statement, EOL, Value
from pseudo.exceptions import IndentationBlockEnd, Comment

__author__ = "Patryk Niedźwiedziński"


class Lexer:
    """
    Class to parse code.

    Attributes:
        - i: A Stream instance with input code.
        - keywords: A set of all keywords in pseudo.
        - range_symbol: String used to define range in for loop.
        - indent_char: Character of indentation (" " or "\t").
        - indent_size: Size of indentation using in particular file.

    Usage::
        >>> lex = Lexer("pisz 12")
        >>> lex.read_next()
        Expression("pisz", args=[Number(12)])
    """

    def __init__(self, inp):
        """Inits Lexer with input."""
        self.i = Stream(inp)
        self.keywords = {
            "pisz",
            "koniec",
            "czytaj",
            "jeżeli",
            "to",
            "wpp",
            "dopóki",
            "wykonuj",
            "dla",
        }
        self.range_symbol = "..."
        self.indent_char = None
        self.indent_size = None

    def is_keyword(self, string) -> bool:
        """Checks if given string is a keyword."""
        return string in self.keywords or string == self.range_symbol

    def is_keyword_end(self, c) -> bool:
        """
        Checks if given char breaks parsing a keyword.

        Example:
        `asd1` - This is one keyword.
        `asd1+asd2` - This is two keywords with `+` in between them.
        """
        try:
            return (
                is_operator(c) or c == " " or c in {"(", ")", "[", "]", "{", "}", ","}
            )
        except TypeError:
            return True

    def update_args(self, args, i):
        """Update args with new operation instance."""
        try:
            args[i] = Operation(args[i], args[i - 1], args[i + 1])
            del args[i + 1]
            del args[i - 1]
        except IndexError:
            self.i.throw(f"Cannot do '{arg.operator}' on nil")
        return args

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

    def read_range(self) -> tuple:
        """Read range `a ,..., b`"""
        a = self.read_args()
        a = self.read_expression(a)
        r = self.read_next()

        if not isinstance(r, str) or r != self.range_symbol:
            self.i.throw(f"Expected {self.range_symbol}, but {r} was given")
        self.i.next()
        b = self.read_condition("dopóki")
        return (a, b)

    def read_keyword(self) -> str:
        """Read a keyword from the stream."""
        keyword = self.read(lambda c: not self.is_keyword_end(c))
        return keyword

    def read_builtin(self, keyword: str, indent_level: int, prev: object) -> object:
        """Read builtin statement, expression from input stream i.e.: if, while etc"""
        if keyword == self.range_symbol:
            return keyword
        if keyword == "wpp":
            if isinstance(prev, Condition):
                return keyword
            self.i.throw(f"Unexpected keyword '{keyword}'")
        if keyword == "to" or keyword == "wykonuj":
            return keyword
        if keyword == "jeżeli":
            return read_if(self, indent_level)
        if keyword == "dopóki":
            return read_while(self, indent_level)
        if keyword == "dla":
            return read_for(self, indent_level)
        arg = self.read_args()
        arg = self.read_expression(arg)
        if keyword == "czytaj":
            if not isinstance(arg, Variable):
                self.i.throw("Statement 'czytaj' requires variable as argument")
        if isinstance(arg, Statement):
            self.i.throw(f"Statement '{keyword}' cannot take '{arg}' as argument")
        return Statement(keyword, args=arg)

    def read_condition(self, keyword, indent_level: int = 0) -> object:
        """Read condition of conditional expression."""
        m = {"jeżeli": "to", "dopóki": "wykonuj"}
        args = self.read_args(indent_level=indent_level)
        if not isinstance(args[-1], str) or args[-1] != m[keyword]:
            self.i.throw(f"Expected keyword '{m[keyword]}', instead got '{args[-1]}'")
        condition = self.read_expression(args[:-1])
        return condition

    def read_args(self, bracket: bool = None, indent_level: int = 0) -> list:
        """Read arguments from the stream."""
        args = []
        while not self.i.eol():
            arg = self.read_next(indent_level=indent_level)

            if arg == self.range_symbol:
                self.i.col -= len(self.range_symbol)
                break
            if not isinstance(arg, Value):
                args = append(args, arg)
                continue
            if isinstance(arg, Operator):
                if len(args) == 0:
                    args.append(Int(0))
            if arg == Value(","):
                break
            if arg == Value(")"):
                if bracket:
                    break
                self.i.throw(f"Invalid character '{operator}'")
            if arg == Value("]"):
                break

            args = append(args, arg)
        return args

    def read_expression(self, args: list, bracket: bool = None) -> object:
        while len(args) > 1:
            prev = Operator("+")
            i = 0
            while i < len(args):
                operator = args[i]
                if isinstance(operator, Operator):
                    if operator < prev:
                        i += 1
                        continue
                    if isinstance(args[i + 1], Operator):
                        self.i.throw(f"Cannot do '{operator}' on nil")
                    try:
                        next_operator = args[i + 2]
                        if operator > next_operator:
                            prev = operator
                            args = self.update_args(args, i)
                            i -= 1
                        else:
                            prev = next_operator
                            args = self.update_args(args, i + 2)
                    except IndexError:
                        args = self.update_args(args, i)
                elif len(args) > i + 1 and not isinstance(args[i + 1], Operator):
                    self.i.throw(f"Undefined operation ☹️")
                i += 1
        return args[0]

    def read_white_chars(self) -> None:
        """Read white chars from stream."""
        self.read(lambda c: c == " " or c == "\t", eol=False)

    def read_next(self, prev: object = None, indent_level: int = 0) -> object:
        """Read next elements from the stream and guess the type."""
        i = self.indent_size
        if self.indent_size is None:
            i = 0
        if self.i.col > i * indent_level:
            self.read_white_chars()
        c = self.i.peek()

        if isinstance(c, EOL):
            self.i.next_line()
            return c

        if c == "#":
            self.i.next_line()
            return EOL()

        if c in {"(", ")", "]", ","}:
            self.i.next()
            if c == "(":
                args = self.read_args(bracket=True)
                return self.read_expression(args, bracket=True)
            return Value(c)

        if c == '"' or c == "'":
            return read_string()

        if is_operator(c):
            return read_operator(self.i)

        if is_digit(c):
            return read_number(self)

        elif c not in {" ", "\t"}:
            col = self.i.col
            keyword = self.read_keyword()
            if self.is_keyword(keyword):
                return self.read_builtin(keyword, indent_level, prev)
            if keyword in OPERATOR_KEYWORDS:
                return Operator(keyword)
            if keyword == "prawda" or keyword == "fałsz":
                return read_bool(keyword)
            indices = []
            while self.i.peek() == "[":
                self.i.next()
                arg = self.read_args()
                exp = self.read_expression(arg)
                indices.append(exp)
            if col == i * indent_level:
                operator = self.read_next()
                if isinstance(operator, EOL):
                    return Variable(keyword, indices)
                if operator != ":=":
                    self.i.throw(f"Cannot parse '{operator}'")
                args = self.read_args()
                args = self.read_expression(args)
                if (
                    not isinstance(args, Int)
                    and not isinstance(args, String)
                    and not isinstance(args, Operation)
                    and not isinstance(args, Variable)
                    and not isinstance(args, Bool)
                ):
                    self.i.throw(f"Cannot assign type {type(args)} to variable")
                return Assignment(Variable(keyword, indices), args, line=self.i.current_line())
            return Variable(keyword, indices)
        if c == "":
            raise EndOfFile
        self.i.throw(f"Invalid character: '{c}'")

    def read_indent_size(self):
        """Read indent size from stream."""
        size = 0
        self.indent_char = self.i.peek()
        while self.i.peek() == self.indent_char:
            self.i.next()
            size += 1
        if size == 0:
            return None
        if size <= 1 and self.indent_char == " ":
            self.i.throw(f"Invalid indentation, should be at least 2, not {size}")
        self.indent_size = size

    def read_indent(self, indent_level: int = 1) -> None:
        """Read indented expressions while valid indentation and returns list of them."""
        if self.indent_size is None:
            self.read_indent_size()
            return None
        for i in range(self.indent_size * indent_level):
            c = self.i.next()
            if isinstance(c, EOL):
                break
            if c == "#":
                raise Comment
            if c != self.indent_char:
                if i % self.indent_size == 0:
                    self.i.col = 0
                    raise IndentationBlockEnd
                self.i.throw(f"Inconsistent indentation size")
        if self.i.peek() == " " or self.i.peek() == "\t":
            self.i.throw(f"Inconsistent indentation size")

    def read_indent_block(self, indent_level: int = 1) -> list:
        """Read indented expressions while valid indentation and returns list of them."""
        expressions = []
        while (
            self.i.peek() == " "
            or self.i.peek() == "\t"
            or self.i.peek() == "#"
            or isinstance(self.i.peek(), EOL)
        ):
            try:
                self.read_indent(indent_level)
            except IndentationBlockEnd:
                break
            except Comment:
                self.i.next_line()
                continue
            try:
                e = self.read_next(indent_level=indent_level)
            except EndOfFile:
                break
            expressions = append(expressions, e)
        return expressions
