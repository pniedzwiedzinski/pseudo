"""
Functions are a way to use the same fragment of code multiple times.
"""


from pseudo.runtime import MemoryObject
from pseudo.type.base import ASTNode
from pseudo.type.variable import Assignment


class Function:
    """
    This class is a representation of function in memory.

    Attributes:
        - instructions: list; List of instructions to be evaluated.
        - args: list; List of arguments names that function takes.
    """

    def __init__(self, name: str, args: list, instructions: list, line: str = ""):
        self.name = name
        self.args = args
        self.instructions = instructions
        self.line = line

    def call(self, r, args=[], calling_line=""):
        # TODO: create scope and init args
        if len(self.args) != len(args):
            r.throw(
                f"Function {repr(self.name)} takes {len(self.args)} arguments, but {len(args)} were given.",
                calling_line,
            )
        for key, value in zip(self.args, args):
            r.save(key.value, value)
        r.run(self.instructions)

    def eval(self, r):
        return self


def read_function(lexer, indent_level: int):
    """
    This function parse function statement.

    Args:
        - lexer: pseudo.lexer.Lexer
    """

    lexer.read_white_chars()
    name = lexer.read_keyword()

    lexer.read_white_chars()

    lexer.i.next()
    args = lexer.read_args(bracket=True)

    lexer.i.next_line()

    instructions = lexer.read_indent_block(indent_level + 1)

    return FunctionDefinition(name, args, instructions, lexer.i.get_current_line())


class FunctionDefinition(ASTNode):
    """
    Representation of function definition in AST.

    Attributes:
        - function_name: str; Name of function.
        - args: list; List of arguments that function takes.
        - instructions: list; List of instructions to be evaluated.
        - line: str; Line in pseudocode.
    """

    def __init__(self, function_name: str, args: list, instructions: list, line: str):
        self.function_name = function_name
        self.args = args
        self.instructions = instructions
        self.line = line

    def eval(self, r):
        r.save(
            self.function_name,
            Function(self.function_name, self.args, self.instructions, self.line),
        )


class Call(ASTNode):
    """
    Representation of function call in AST.

    Attributes:
        - function_name: str; Name of function to call.
        - args: list; List of given arguments.
        - line: str; Line in pseudocode.
    """

    def __init__(self, function_name: str, args: list = [], line: str = ""):
        self.function_name = function_name
        self.args = args
        self.line = line

    def eval(self, r):
        function_exists = self.function_name in r.var

        if function_exists:
            function = r.get(self.function_name)
            function.call(r, self.args, self.line)
        else:
            r.throw(f"Function {repr(self.function_name)} is not defined.", self.line)
