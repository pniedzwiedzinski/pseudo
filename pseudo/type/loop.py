"""This module contains ASTNode for loop and iterator memory object."""

__author__ = "Patryk Niedźwiedziński"

from pseudo.exceptions import RunTimeError
from pseudo.runtime import MemoryObject
from pseudo.type.base import Value
from pseudo.type.variable import Variable, Assignment, Increment
from pseudo.type.operation import Operation, Operator, read_operator


class Iterator(MemoryObject):
    """
    This class is a representation of iterator in memory.
    """

    def __init__(self, key: str, value: int):
        MemoryObject.__init__(self, key, value, const=True)

    def setter(self, _, r):
        raise RunTimeError("Cannot change value of iterator")

    def incr(self):
        self.value += 1


class Loop:
    """
    Node for representing looped actions.

    Attributes:
        - condition: Condition to check if loop should be executed.
        - expressions: List of expressions to execute if condition is positive.
    """

    def __init__(self, condition, expressions, iterator=None, line=""):
        self.condition = condition
        self.expressions = expressions
        self.iterator = iterator
        self.line = line

    def eval(self, r):
        while self.condition.eval(r):
            r.run(self.expressions)
        if self.iterator is not None:
            r.delete(self.iterator.value)

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __repr__(self):
        return f"Loop({self.condition}, {self.expressions})"


def read_for(lexer, indent_level: int = 0) -> Loop:
    """Read for statement."""
    lexer.read_white_chars()
    condition = lexer.read_next()

    if not isinstance(condition, Variable):
        lexer.i.throw(f"Expected Variable, but {type(condition)} was given")
    lexer.read_white_chars()
    assign = read_operator(lexer.i)
    if not isinstance(assign, str) or (assign != ":=" and assign != "<-"):
        lexer.i.throw(f"Expected assignment symbol")

    a, b = lexer.read_range()
    line = lexer.i.current_line()
    lexer.i.next_line()
    expressions = lexer.read_indent_block(indent_level + 1)
    expressions.append(Increment(condition.value))

    return [
        Assignment(condition, a, Iterator, line=line),
        Loop(Operation(Operator("<="), condition, b), expressions, condition, line),
    ]


def read_while(lexer, indent_level: int = 0) -> Loop:
    """Read while statement."""
    # TODO: test
    condition = lexer.read_condition("dopóki", indent_level=indent_level)
    lexer.i.next_line()
    expressions = lexer.read_indent_block(indent_level=indent_level + 1)
    if expressions is None:
        lexer.i.throw(f"Expected indented code, instead got 'nil'")
    return Loop(condition, expressions)
