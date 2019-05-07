"""
Functions are a way to use the same fragment of code multiple times.
"""


from pseudo.runtime import MemoryObject
from pseudo.type.base import ASTNode


class Function(MemoryObject):
    """
    This class is a representation of function in memory.

    Attributes:
        - instructions: list; List of instructions to be evaluated.
        - args: list; List of arguments names that function takes.
    """

    def __init__(self, key, args, instructions):
        MemoryObject.__init__(self, key, '<type: "func">', True)
        self.args = args
        self.instructions = instructions

    def call(self, r, args=[]):
        # TODO: create scope and init args
        r.run(self.instructions)


class Call(ASTNode):
    def __init__(self, function_name, args=[], line=""):
        self.function_name = function_name
        self.args = args
        self.line = line

    def eval(self, r):
        if self.function_name in r.var:
            return r.var[self.function_name].call(r, self.args)
        else:
            r.throw(f"Function {repr(self.function_name)} is not defined.", self.line)
