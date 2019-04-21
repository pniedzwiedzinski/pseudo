"""This module contains RunTime class, which is a representation of runtime resources."""

__author__ = "Patryk Niedźwiedziński"

from sys import exit
from pseudo.type.numbers import Int
from pseudo.type.string import String


class MemoryObject:
    """
    This class is a representation of object in runtime memory.

    Attributes:
        - value: object, Stored object.
        - const: bool, If true object is constant and cannot be changed.
    """

    def __init__(self, key: str, value: object, const: bool = False):
        self.key = key
        self.value = value
        self.const = const

    def setter(self, value: object, r):
        """This function updates value."""
        if self.const:
            r.throw(f"Variable is not settable", self.line)
        else:
            self.value = value

    def getter(self):
        """This function returns value."""
        return self.value


class RunTime:
    """
    This class is a representation of computer resources like memory or processor.
    
    Attributes:
        - var: dict, In this object all variables will be stored.
    """

    def __init__(self):
        self.var = {}

    def save(self, key: str, value: object, object_class=MemoryObject):
        """
        This functions is used to save value in `var`.
        
        Args:
            - key: str, Unique key under which value will be stored. `T[1][10]` is also a key
            - value: object, Value to store.
            - object_class: class, Class of value.
        """

        if key not in self.var:
            self.var[key] = object_class(key, value.eval(self))
        else:
            self.var[key].setter(value.eval(self), self)

    def get(self, key: str):
        """
        This function returns value stored under key.
        
        Args:
            - key: str, Key under which value is stored.
        """

        if key in self.var:
            return self.var[key].getter()
        else:
            return "nil"

    def delete(self, key: str):
        """Remove from memory."""
        del self.var[key]

    def stdin(self, key: str, indices: list = []):
        """Read from stdin and store it in `var`."""
        value = input(f"{key}: ")

        try:  # value is a string by default
            value = Int(value)
        except ValueError:
            value = String(value)

        self.save(key, value, indices)

    def stdout(self, value: object):
        """Write to stdout"""
        if value == "\\n":
            print("")
        else:
            print(value, end="")

    def throw(self, error_message: str, line_causing_error: str = ""):
        """This function is used to tell user that a runtime error has occurred."""

        print(f"⚠️  Runtime error:")
        print(f"\t'{line_causing_error}'")
        print(error_message)
        exit(1)
