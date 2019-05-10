"""This module contains RunTime class, which is a representation of runtime resources."""

__author__ = "Patryk Niedźwiedziński"

import datetime
import os
import traceback
from uuid import uuid4
from sys import exit

from pseudo.exceptions import RunTimeError
from pseudo.type.numbers import Int
from pseudo.type.string import String
from pseudo.type.exceptions import ReturnCall


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

    def call(self, r, args=[]):
        """Call variable like `a()`"""
        r.throw(f"Variable {self.key} is not callable", self.line)


class RunTime:
    """
    This class is a representation of computer resources like memory or processor. It is used
    to run instructions parsed by `pseudo.lexer.Lexer`.

    Attributes:
        - var: dict, In this object all variables will be stored.


    Variable names:

        Variable names consist of alphanumeric characters, starting with alphabetical char. Arrays
        are stored as independent keys i.e.::

            {
                "T[1]": 1,
                "T[2]": 2,
            }

    Usage::
        >>> instructions = [Statement("pisz", Int(42))]
        >>> r = RunTime()
        >>> r.run(instructions)
        42
    """

    def __init__(self, var={}):
        self.var = var
        self.scopes = {}

    def register_scope(self, function_name: str) -> str:
        """
        Create new scope and return its id.

        Args:
            - function_name: str, Prefix for scope id.
        """

        while True:
            scope_id = f"{function_name}-{uuid4()}"
            if scope_id not in self.scopes:
                break

        self.scopes[scope_id] = {}

        return scope_id

    def remove_scope(self, scope_id: str):
        """
        Remove scope from scope register.

        Args:
            - scope_id: str, Scope to remove.
        """

        del self.scopes[scope_id]

    def save(
        self, key: str, value: object, object_class=MemoryObject, scope_id: str = None
    ):
        """
        This functions is used to save variable's value in memory

        Args:
            - key: str, Unique key under which value will be stored. `T[1][10]` is also a key
            - value: object, Value to store.
            - object_class: class, Class of value.
            - scope_id: str, Scope in which value should be saved, if None it will be saved to
                global scope.
        """

        if key not in self.var:
            if scope_id:
                self.scopes[scope_id][key] = object_class(
                    key, value.eval(self, scope_id)
                )
            else:
                self.var[key] = object_class(key, value.eval(self))
        else:
            self.var[key].setter(value.eval(self), self)

    def get(self, key: str, scope_id: str = None):
        """
        This function returns value of stored variable.
        
        Args:
            - key: str, Key under which value is stored.
        """

        if scope_id and key in self.scopes[scope_id]:
            return self.scopes[scope_id][key].getter()
        if key in self.var:
            return self.var[key].getter()
        else:
            return "nil"

    def delete(self, key: str, scope_id: str = None):
        """This function removes variable from memory."""
        if scope_id and key in self.scopes[scope_id]:
            del self.scopes[scope_id][key]
        else:
            del self.var[key]

    def stdin(self, key: str):
        """This function reads value from standard input and stores it in given variable."""
        value = input(f"{key}: ")

        try:  # value is a string by default
            value = Int(value)
        except ValueError:
            value = String(value)

        self.save(key, value)

    def stdout(self, value: object):
        """This function writes value to standard output."""
        if value == "\\n":
            print("")
        else:
            print(value, end="")

    @staticmethod
    def save_crash(error_message: str):
        """Save crash message to file and return path to it."""

        now = datetime.datetime.now().strftime("%H-%M-%S-%d-%m-%Y")

        try:  # Create folder to store .log file
            os.mkdir("crash")
        except FileExistsError:
            pass

        with open(f"crash/{now}.log", "w") as fp:
            fp.write(error_message)

        return f"{os.getcwd()}/crash/{now}.log"

    def eval(self, instruction, scope_id: str = None):
        """Evaluate instruction."""
        try:
            if scope_id:
                instruction.eval(self, scope_id)
            else:
                instruction.eval(self)
        except RunTimeError as err:
            self.throw(err, instruction.line)
        except ReturnCall as r:
            raise r

    def run(self, instructions: list, scope_id: str = None):
        """Run pseudocode instructions"""
        try:
            for i in instructions:
                self.eval(i, scope_id)
        except ReturnCall as r:
            raise r
        except Exception:
            path = self.save_crash(traceback.format_exc())
            print("⚠️  Error: \n\tRuntime error has occurred!\n")
            print(
                "Wow! You encountered a bug! Please tell me how did you do that on https://github.com/pniedzwiedzinski/pseudo/issues\n"
            )
            print(f"Error message was copied to {path}")
            exit(1)

    def throw(self, error_message: str, line_causing_error: str = ""):
        """This function is used to tell user that a runtime error has occurred."""

        print(f"\n⚠️  Error on line :")
        print(f"\t'{line_causing_error}'")
        print(error_message)
        exit(1)
