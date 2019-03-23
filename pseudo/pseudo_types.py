"""
This module contains classes for types in AST.
"""


__author__ = "Patryk Niedźwiedziński"

VAR = {}

GROUP_1 = {"*", "div", "mod"}
GROUP_2 = {"-", "+"}


class Value:
    """
    Node containing a value.

    Attributes:
        value: Value of instance.
    """

    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"Value({repr(self.value)})"

    def __str__(self):
        return str(self.value)


class Int(Value):
    """Int value node."""

    def __init__(self, value):
        self.value = int(value)

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"Int({repr(self.value)})"


class String(Value):
    """String value node."""

    def __repr__(self):
        return f'String("{self.value}")'


class Bool(Value):
    """Bool value node."""

    def __repr__(self):
        return f"Bool({self.value})"


class Operator(Value):
    """Opartor class for representing mathematical operator."""

    def eval(self, left: Value, right: Value):
        if self.value == "+":
            return left.eval() + right.eval()
        if self.value == "-":
            return left.eval() - right.eval()
        if self.value == "*":
            return left.eval() * right.eval()
        if self.value == "div":
            return left.eval() // right.eval()
        if self.value == "mod":
            return left.eval() % right.eval()

        if self.value == "=":
            if left.eval() == right.eval():
                return 1
            return 0

        if self.value == "!=":
            if left.eval() != right.eval():
                return 1
            return 0

    def __lt__(self, o):
        if self.value in GROUP_2:
            if o.value in GROUP_1:
                return True
        return False

    def __gt__(self, o):
        if self.value in GROUP_1:
            return True
        if self == o:
            return True
        return False

    def __eq__(self, o):
        if self.value in GROUP_1 and o.value in GROUP_1:
            return True
        if self.value in GROUP_2 and o.value in GROUP_2:
            return True
        return False

    def __repr__(self):
        return self.value


class Operation:
    """Operation node."""

    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def eval(self):
        return self.operator.eval(self.left, self.right)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"({self.left}{self.operator}{self.right})"


class Statement:
    """
    Node for statement with arguments.

    Attributes:
        value: Statement name.
        args: Arguments of statement.
    """

    def __init__(self, value, args=None):
        self.value = value
        self.args = args

    def eval(self):
        if self.value == "pisz":
            print(self.args.eval())
        elif self.value == "czytaj":
            inp = input(self.args.value + ": ")
            try:
                inp = int(inp)
                inp = Int(inp)
            except ValueError:
                inp = String(inp)
            x = Assignment(self.args, inp)
            x.eval()
        elif self.value == "koniec":
            exit()

    def __repr__(self):
        return f'Statement("{self.value}", args={self.args})'

    def __str__(self):
        return self.__repr__()


class Variable(Value):
    """
    Node for representing variables.

    Attributes:
        value: Name of the variable.
    """

    def eval(self):
        try:
            return VAR[self.value]
        except KeyError:
            return "nil"

    def __repr__(self):
        return f'Variable("{self.value}")'

    def __str__(self):
        return self.__repr__()


class Assignment:
    """
    Node for representing assignments.

    Attributes:
        target: Target variable.
        value: Value to assign.
    """

    def __init__(self, target, value):
        self.target = target
        self.value = value

    def eval(self):
        VAR[self.target.value] = self.value.eval()

    def __repr__(self):
        return f"Assignment({self.target}, {self.value})"

    def __str__(self):
        return self.__repr__()


class Condition:
    """
    Node for representing conditional expressions (if).

    Attributes:
        condition: Condtion to check
        true: List to evaluate if condition is true
        false: List to evaluate if condition is false (optional)
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

    def __repr__(self):
        return f"Condition({self.condition}, {self.true}, {self.false})"


class EOL:
    """Representation of newline."""

    def __init__(self):
        pass

    def eval(self):
        pass

    def __repr__(self):
        return f"EOL()"

    def __str__(self):
        return "EOL"
