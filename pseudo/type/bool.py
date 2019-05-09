"""This module contains everything about bool in pseudocode."""

__author__ = "Patryk Niedźwiedziński"

from pseudo.type.base import Value


class Bool(Value):
    """Bool value node."""

    def __str__(self):
        if self.value:
            return "prawda"
        return "fałsz"

    @staticmethod
    def eval_operation(
        operator: str, left: Value, right: Value, r, scope_id: str = None
    ):
        """
        Eval bool operation.

        Args:
            - operator: str, bool operator
            - left: Value
            - right: Value
        """

        return_value = None

        if operator == "=":
            return_value = int(left.eval(r, scope_id) == right.eval(r, scope_id))
        elif operator == "!=":
            return_value = int(left.eval(r, scope_id) != right.eval(r, scope_id))
        elif operator == ">":
            return_value = int(left.eval(r, scope_id) > right.eval(r, scope_id))
        elif operator == "<":
            return_value = int(left.eval(r, scope_id) < right.eval(r, scope_id))
        elif operator == "<=":
            return_value = int(left.eval(r, scope_id) <= right.eval(r, scope_id))
        elif operator == ">=":
            return_value = int(left.eval(r, scope_id) >= right.eval(r, scope_id))

        return return_value

    def __repr__(self):
        return f"Bool({self.value})"


def read_bool(keyword: str) -> Bool:
    """Parse bool str to Bool object."""
    if keyword == "prawda":
        return Bool(1)
    if keyword == "fałsz":
        return Bool(0)
