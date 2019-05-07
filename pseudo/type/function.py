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

    def __init__(self, key, args, instructions, line=""):
        MemoryObject.__init__(self, key, '<type: "func">', True)
        self.args = args
        self.instructions = instructions
        self.line = line

    def call(self, r, args=[]):
        # TODO: create scope and init args
        if len(self.args) != len(args):
            r.throw(
                f"Function {repr(self.key)} takes {len(self.args)} arguments, but {len(args)} were given.",
                self.line,
            )
        for key, value in zip(self.args, args):
            r.save(key, value)
        r.run(self.instructions)


class Call(ASTNode):
    """
    Representation of function call in AST.

    Attributes:
        - function_name: str; Name of function to call.
        - args: list; List of given arguments.
        - line: str; Line in pseudocode.
    """

    def __init__(self, function_name, args=[], line=""):
        self.function_name = function_name
        self.args = args
        self.line = line

    def eval(self, r):
        if self.function_name in r.var:
            return r.var[self.function_name].call(r, self.args)
        else:
            r.throw(f"Function {repr(self.function_name)} is not defined.", self.line)
