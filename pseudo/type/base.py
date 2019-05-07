"""This module contains base class for all objects representing value in AST"""

__author__ = "Patryk Niedźwiedziński"


class ASTNode:
    """
    When pseudocode is being compiled interpreter builds Abstract Syntax Tree. It's a graph
    representing actual code. Every node has `eval` method which is called to get result of
    code.
    """

    def eval(self, r):
        """
        Args:
            - r: `pseudo.runtime.RunTime`_; Every node is evaluated in some context. This context
                is contained in runtime.

        .. _`pseudo.runtime.RunTime`: https://pseudo.readthedocs.io/en/latest/runtime.html#pseudo.runtime.RunTime
        """

        raise NotImplementedError


class Value(ASTNode):
    """
    Node containing a value.

    Attributes:
        - value: Value of instance.
        - line: Line of pseudocode representation
    """

    def __init__(self, value, line=""):
        self.value = value
        self.line = line

    def eval(self, r):
        return self.value

    def __eq__(self, other):
        try:
            return self.value == other.value
        except AttributeError:
            return False

    def __repr__(self):
        return f"Value({repr(self.value)})"

    def __str__(self):
        return str(self.value)


class EOL(ASTNode):
    """Representation of newline."""

    def __init__(self):
        self.line = ""

    def eval(self, r):
        pass

    def __eq__(self, other):
        return isinstance(other, EOL)

    def __repr__(self):
        return f"EOL()"

    def __str__(self):
        return "EOL"
