"""This module contains ASTNode for loop and iterator memory object."""

__author__ = "Patryk Niedźwiedziński"

from pseudo.exceptions import RunTimeError
from pseudo.runtime import MemoryObject
from pseudo.type.base import Value, ASTNode
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


class Loop(ASTNode):
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
    """
    This function reads and returns for loop statement. The for loop needs couple things:
        
        - iterator: Variable to iterate over.
        - start value: Value with which iterator will be initialized.
        - end value: Value on which loop will end its execution.
        - instruction stack: Instructions to execute during loop.
    """

    # Read iterator name
    lexer.read_white_chars()
    iterator = lexer.read_next()
    if not isinstance(iterator, Variable):
        lexer.i.throw(f"Expected Variable, but {type(iterator)} was given")
    lexer.read_white_chars()

    # Check assign operator
    assign = read_operator(lexer.i)
    if not isinstance(assign, str) or (assign != ":=" and assign != "<-"):
        lexer.i.throw(f"Expected assignment symbol")

    # Read start and end values
    start_value, end_value = lexer.read_range()

    line = lexer.i.get_current_line()
    lexer.i.next_line()

    # Read instructions
    instructions = lexer.read_indent_block(indent_level + 1)
    instructions.append(Increment(iterator.value))

    return [
        Assignment(iterator, start_value, Iterator, line=line),
        Loop(
            Operation(Operator("<="), iterator, end_value), instructions, iterator, line
        ),
    ]


def read_while(lexer, indent_level: int = 0) -> Loop:
    """
    This function reads and returns while loop statement. The while loop needs condition
    and instruction stack.

    Args:
        - lexer: Lexer object to read values
        - indent_level: Level of indentation on which loop was written.
    """

    # Read condition
    condition = lexer.read_condition("dopóki", indent_level=indent_level)
    line = lexer.i.get_current_line()
    lexer.i.next_line()

    # Read instructions
    instructions = lexer.read_indent_block(indent_level=indent_level + 1)
    if instructions is None:
        lexer.i.throw(f"Expected indented code, instead got 'nil'")

    return Loop(condition, instructions, line=line)
