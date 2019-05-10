"""
Functions are a way to use the same fragment of code multiple times.
"""


from pseudo.type.base import ASTNode, Value
from pseudo.type.variable import Assignment
from pseudo.type.exceptions import ReturnCall


class Function(Value):
    """
    This class is a representation of function in memory.

    Attributes:
        - name: str, Name of function.
        - args: list, List of arguments names that function takes.
        - instructions: list, List of instructions to be evaluated.
        - line: str, Line in pseudocode.
        - void: bool, Defines if function can return value.
    """

    def __init__(
        self,
        name: str,
        args: list,
        instructions: list,
        line: str = "",
        void: bool = False,
    ):
        self.name = name
        self.args = args
        self.instructions = instructions
        self.line = line
        self.void = void

    def call(self, r, args: list, scope_id: str, calling_line: str):
        """
        Call function.

        Args:
            - r: pseudo.runtime.RunTime, Runtime in which function will be called.
            - args: list, Arguments passed in function call.
            - scope_id, str, Scope in which function's instructions will be evaluated.
            - calling_ling: str, Line in pseudocode.
        """
        if len(self.args) != len(args):
            r.throw(
                f"Function {repr(self.name)} takes {len(self.args)} arguments, but {len(args)} were given.",
                calling_line,
            )
        for key, value in zip(self.args, args):
            r.save(key.value, value, scope_id=scope_id)
        try:
            r.run(self.instructions, scope_id)
        except ReturnCall as ret:
            if self.void:
                r.throw(f"Procedure {repr(self.name)} can not return value.", self.line)
            return ret.return_value

    def eval(self, r, scope_id=None):
        return self


def read_function(lexer, indent_level: int = 0, void: bool = False):
    """
    This function parse function statement. The function expect cursor to be after `function`
    keyword::

        funkcja a()
               ^

    Args:
        - lexer: pseudo.lexer.Lexer
        - indent_level
        - void: bool, Defines if function can return value.
    """

    lexer.read_white_chars()
    name = lexer.read_keyword()

    lexer.read_white_chars()

    lexer.i.next()
    args = lexer.read_args(bracket=True)

    line = lexer.i.get_current_line()

    lexer.i.next_line()

    instructions = lexer.read_indent_block(indent_level + 1)

    return FunctionDefinition(name, args, instructions, line, void)


class FunctionDefinition(ASTNode):
    """
    Representation of function definition in AST.

    Attributes:
        - function_name: str; Name of function.
        - args: list; List of arguments that function takes.
        - instructions: list; List of instructions to be evaluated.
        - line: str; Line in pseudocode.
        - void: bool, Defines if function can return value.
    """

    def __init__(
        self,
        function_name: str,
        args: list,
        instructions: list,
        line: str,
        void: bool = False,
    ):
        self.function_name = function_name
        self.args = args
        self.instructions = instructions
        self.line = line
        self.void = void

    def eval(self, r, scope_id=None):
        r.save(
            self.function_name,
            Function(
                self.function_name, self.args, self.instructions, self.line, self.void
            ),
        )

    def __repr__(self):
        return f"FunctionDefinition({repr(self.function_name)}, {repr(self.args)}, {repr(self.instructions)})"


class Call(Value):
    """
    Representation of function call in AST.

    Attributes:
        - function_name: str; Name of function to call.
        - args: list; List of given arguments.
        - line: str; Line in pseudocode.
    """

    def __init__(self, function_name: str, args: list = [], line: str = ""):
        Value.__init__(self, function_name, line)
        self.function_name = function_name
        self.args = args
        self.line = line

    def eval(self, r, scope_id=None):
        function_exists = self.function_name in r.var

        if function_exists:
            function = r.get(self.function_name)
            if isinstance(function, Function):
                scope_id = r.register_scope(self.function_name)
                return_value = function.call(r, self.args, scope_id, self.line)
                r.remove_scope(scope_id)
                return return_value or "nil"

        r.throw(f"Function {repr(self.function_name)} is not defined.", self.line)

    def __repr__(self):
        return f"Call({repr(self.function_name)}, {repr(self.args)})"


class Return(ASTNode):
    """
    Representation of `return` call in AST.

    Attributes:
        - return_value: `pseudo.type.base.Value`, Value to return.
    """

    def __init__(self, return_value):
        self.return_value = return_value

    def eval(self, r, scope_id):
        raise ReturnCall(self.return_value.eval(r, scope_id))
