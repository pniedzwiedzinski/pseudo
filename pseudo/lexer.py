"""
This module contains Lexer class using to tokenize stream.
"""

from pseudo.stream import Stream, EndOfFile
from pseudo.pseudo_types import (
    String,
    Int,
    Operation,
    Operator,
    Statement,
    EOL,
    Variable,
    Assignment,
    Bool,
    Value,
    Condition,
    Loop
)

__author__ = "Patryk Niedźwiedziński"


GROUP_1 = {"*", "div", "mod"}
GROUP_2 = {"-", "+"}


class Lexer:
    """
    Class to parse code.

    Attributes:
        - i: A Stream instance with input code.
        - keywords: A set of all keywords in pseudo.
        - operators: A set of operators in pseudo.
        - operator_keywords: A set of operators written as string.
        - indent_size: Size of indentation using in particular file.

    Usage::
        >>> lex = Lexer("pisz 12")
        >>> lex.read_next()
        Expression("pisz", args=[Number(12)])
    """

    def __init__(self, inp):
        """Inits Lexer with input."""
        self.i = Stream(inp)
        self.keywords = {"pisz", "koniec", "czytaj", "jeżeli", "to", "wpp", "dopóki", "wykonuj"}
        self.operators = {"+", "-", "*", ":", "<", ">", "=", "!"}
        self.operator_keywords = {"div", "mod"}
        self.indent_char = None
        self.indent_size = None

    def is_keyword(self, string) -> bool:
        """Checks if given string is a keyword."""
        return string in self.keywords

    @staticmethod
    def is_alphabet(c) -> bool:
        """Checks if given char is from alphabet."""
        try:
            ascii = ord(c)
            return (ascii >= 65 and ascii <= 90) or (ascii >= 97 and ascii <= 122)
        except TypeError:
            return False

    @staticmethod
    def is_digit(c) -> bool:
        """Checks if given char is a digit."""
        try:
            return ord(c) >= 48 and ord(c) <= 57
        except TypeError:
            return False

    def is_operator(self, c) -> bool:
        """Checks if given char is an allowed operator."""
        try:
            return c in self.operators or c in self.operator_keywords
        except TypeError:
            return False

    def is_keyword_end(self, c) -> bool:
        """
        Checks if given char breaks parsing a keyword.

        Example:
        `asd1` - This is one keyword.
        `asd1+asd2` - This is two keywords with `+` in between them.
        """
        try:
            return not (self.is_operator(c) or c == " " or c in {"(",")","[","]","{","}"})
        except TypeError:
            return False

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

    def read_number(self) -> Int:
        """Read a number from the stream."""
        number = self.read(self.is_digit)
        try:
            int(number)
        except ValueError:
            return None
        return Int(number)

    def read_string(self) -> String:
        """Read a string from the stream."""
        self.i.next()
        string = self.read(lambda c: c != '"')
        try:
            string_end = self.i.next() == '"'
        except IndexError:
            string_end = False
        if not string_end:
            self.i.throw(f"Could not parse string")
        return String(string)

    def read_bool(self, keyword: str) -> Bool:
        """Parse bool str to Bool object."""
        if keyword == "prawda":
            return Bool(1)
        if keyword == "fałsz":
            return Bool(0)
        self.i.throw(f"Could not parse '{keyword}' to bool.")

    def read_if(self, indent_level: int = 0) -> Condition:
        """Read if statement."""
        #TODO: tests
        condition = self.read_condition("jeżeli", indent_level=indent_level)
        self.i.next_line()
        true = self.read_indent(indent_level=indent_level + 1)
        false = None
        if self.i.eof():
            return Condition(condition, true, false=false)
        c, l = self.i.col, self.i.line
        try:
            for i in range(indent_level * self.indent_size):
                char = self.i.next()
                if char != " ":
                    if i % self.indent_size == 0:
                        self.i.col = 0
                        return Condition(condition, true, false=false)
                    self.i.throw(f"Inconsistent indentation size")
            if self.i.peek() == " ":
                self.i.throw(f"Inconsistent indentation size")
            if self.read_next(prev=Condition(condition, true)) == "wpp":
                self.i.next_line()
                false = self.read_indent(indent_level=indent_level + 1)
            else:
                self.i.col, self.i.line = c, l
        except EndOfFile:
            self.i.col, self.i.line = c, l
        return Condition(condition, true, false=false)

    def read_while(self, indent_level: int = 0) -> Loop:
        """Read while statement."""
        #TODO: test
        condition = self.read_condition("dopóki", indent_level=indent_level)
        self.i.next_line()
        expressions = self.read_indent(indent_level=indent_level + 1)
        if expressions is None:
            self.i.throw(f"Expected indented code, instead got 'nil'")
        return Loop(condition, expressions)

    def read_keyword(self) -> str:
        """Read a keyword from the stream."""
        keyword = self.read(self.is_keyword_end)
        return keyword

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
            if not isinstance(arg, Value):
                args.append(arg)
                continue
            if isinstance(arg, Operator):
                if len(args) == 0:
                    args.append(Int(0))
            if arg == Value(")"):
                if bracket:
                    break
                self.i.throw(f"Invalid character '{operator}'")
            if arg == Value("]"):
                break
            args.append(arg)
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
                elif len(args) < i+1 and not isinstance(args[i+1], Operator):
                    self.i.throw(f"Undefined operation ☹️")
                i += 1
        return args[0]

    def read_operator(self, c):
        """Return operator from input stream."""
        if (c == ":" and self.i.peek() == "=") or (c == "<" and self.i.peek() == "-"):
            self.i.next()
            return ":="
        if c == "!" and self.i.peek() == "=":
            self.i.next()
            return Operator("!=")
        if self.i.peek() == "=":
            if c in "<>":
                return Operator(c + self.i.next())
        return Operator(c)

    def read_next(self, prev: object = None, indent_level: int = 0) -> object:
        """Read next elements from the stream and guess the type."""
        if self.i.eof():
            raise EndOfFile
        try:
            i = indent_level * self.indent_size
        except TypeError:
            i = 0
        if self.i.col > i:
            self.read(lambda c: c == " " or c == "\t", eol=False)
        c = self.i.peek()

        if isinstance(c, EOL):
            self.i.next_line()
            if self.i.eof():
                raise EndOfFile
            return c

        if c == "#":
            self.i.next_line()
            return self.read_next()

        if c in {"(", ")", "]"}:
            self.i.next()
            if c == "(":
                args = self.read_args(bracket=True)
                return self.read_expression(args, bracket=True)
            return Value(c)

        if c == '"' or c == "'":
            return self.read_string()

        if self.is_operator(c):
            self.i.next()
            return self.read_operator(c)

        if self.is_digit(c):
            return self.read_number()

        elif c not in {" ", "\t"}:
            col = self.i.col
            keyword = self.read_keyword()
            if self.is_keyword(keyword):
                if keyword == "wpp":
                    if isinstance(prev, Condition):
                        return keyword
                    self.i.throw(f"Unexpected keyword '{keyword}'")
                if keyword == "to" or keyword == "wykonuj":
                    return keyword
                if keyword == "jeżeli":
                    return self.read_if(indent_level)
                if keyword == "dopóki":
                    return self.read_while(indent_level)
                arg = self.read_args()
                arg = self.read_expression(arg)
                if keyword == "czytaj":
                    if not isinstance(arg, Variable):
                        self.i.throw("Statement 'czytaj' requires variable as argument")
                if isinstance(arg, Statement):
                    self.i.throw(
                        f"Statement '{keyword}' cannot take '{arg}' as argument"
                    )
                return Statement(keyword, args=arg)
            if keyword in self.operator_keywords:
                return Operator(keyword)
            if keyword == "prawda" or keyword == "fałsz":
                return self.read_bool(keyword)
            indices = []
            while self.i.peek() == "[":
                self.i.next()
                arg = self.read_args()
                exp = self.read_expression(arg)
                indices.append(exp)
            if col == i:
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
                return Assignment(Variable(keyword, indices), args)
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

    def read_indent(self, indent_level: int = 1) -> list:
        """Read indented expressions while valid indentation and returns list of them."""
        expressions = []
        while (
            self.i.peek() == " "
            or self.i.peek() == "\t"
            or self.i.peek() == "#"
            or isinstance(self.i.peek(), EOL)
        ):
            if self.i.peek() == "#":
                self.i.next_line()
                continue
            if self.indent_size is None:
                self.read_indent_size()
            else:
                for i in range(self.indent_size * indent_level):
                    c = self.i.next()
                    if isinstance(c, EOL):
                        break
                    if c == "#":
                        self.i.next_line()
                        continue
                    if c != self.indent_char:
                        if i % self.indent_size == 0:
                            self.i.col = 0
                            return expressions
                        self.i.throw(f"Inconsistent indentation size")
            if self.i.peek() == " " or self.i.peek() == "\t":
                self.i.throw(f"Inconsistent indentation size")
            try:
                e = self.read_next(indent_level=indent_level)
            except EndOfFile:
                return expressions
            expressions.append(e)
        return expressions
