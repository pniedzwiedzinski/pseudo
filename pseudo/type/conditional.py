"""This module contains everything about conditional statements in pseudocode."""

__author__ = "Patryk Niedźwiedziński"


from pseudo.stream import EndOfFile


class Condition:
    """
    Node for representing conditional expressions (if).

    Attributes:
        - condition: Condition to check
        - true: List to evaluate if condition is true
        - false: List to evaluate if condition is false (optional)
    """

    def __init__(self, condition, true, false=None):
        self.condition = condition
        self.true = true
        self.false = false

    def eval(self):
        b = self.condition.eval()
        if b and b != "nil":
            for x in self.true:
                x.eval()
        elif self.false is not None:
            for x in self.false:
                x.eval()

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

    # TODO: tests
    condition = lexer.read_condition("jeżeli", indent_level=indent_level)
    lexer.i.next_line()
    true = lexer.read_indent_block(indent_level=indent_level + 1)

    false = None
    if lexer.i.eof():
        return Condition(condition, true, false=false)
    c, l = lexer.i.col, lexer.i.line

    try:
        for i in range(indent_level * lexer.indent_size):
            char = lexer.i.next()
            if char != " ":
                if i % lexer.indent_size == 0:
                    lexer.i.col = 0
                    return Condition(condition, true, false=false)
                lexer.i.throw(f"Inconsistent indentation size")
        if lexer.i.peek() == " ":
            lexer.i.throw(f"Inconsistent indentation size")
        if lexer.read_next(prev=Condition(condition, true)) == "wpp":
            lexer.i.next_line()
            false = lexer.read_indent_block(indent_level=indent_level + 1)
        else:
            lexer.i.col, lexer.i.line = c, l
    except EndOfFile:
        lexer.i.col, lexer.i.line = c, l
    return Condition(condition, true, false=false)

