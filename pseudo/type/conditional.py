"""This module contains everything about conditional statements in pseudocode."""

__author__ = "Patryk Niedźwiedziński"


from pseudo.stream import EndOfFile
from pseudo.type.base import ASTNode


class Condition(ASTNode):
    """
    Node for representing conditional expressions (if).

    Attributes:
        - condition: Condition to check
        - true: List to evaluate if condition is true
        - false: List to evaluate if condition is false (optional)
        - line: String of pseudocode representation
    """

    def __init__(self, condition, true, false=None, line=""):
        self.condition = condition
        self.true = true
        self.false = false
        self.line = line

    def eval(self, r, scope_id=None):
        b = self.condition.eval(r, scope_id)
        if b and b != "nil":
            r.run(self.true, scope_id)
        elif self.false is not None:
            r.run(self.false, scope_id)

    def __eq__(self, other):
        if not isinstance(other, Condition):
            return False
        if self.__dict__ != other.__dict__:
            raise Exception
            return False
        return True

    def __repr__(self):
        return f"Condition({self.condition}, {self.true}, {self.false})"


def read_if(lexer, indent_level: int = 0) -> Condition:
    """
    Read if statement from stream. This function expect stream cursor be after if keyword::

        'if condition then'
           ^
    
    Args:
        - lexer: Lexer object used to apply lexing rules.
        - indent_level: int, Indicates level of indentation passed to children.
    """

    condition = lexer.read_condition("jeżeli", indent_level=indent_level)
    line = lexer.i.get_current_line()
    lexer.i.next_line()
    true = lexer.read_indent_block(indent_level=indent_level + 1)

    false = None
    if lexer.i.eof():
        return Condition(condition, true, false=false, line=line)
    c, l = lexer.i.col, lexer.i.line

    try:
        lexer.read_indent(indent_level)
        if lexer.read_next(prev=Condition(condition, true)) == "wpp":
            lexer.i.next_line()
            false = lexer.read_indent_block(indent_level=indent_level + 1)
        else:
            lexer.i.col, lexer.i.line = c, l
    except EndOfFile:
        lexer.i.col, lexer.i.line = c, l
    return Condition(condition, true, false=false, line=line)

