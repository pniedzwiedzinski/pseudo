"""This module contains RunTime class, which is a representation of runtime resources."""

__author__ = "Patryk Niedźwiedziński"

import datetime
import os
import traceback
from sys import exit

from pseudo.exceptions import RunTimeError
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
    This class is a representation of computer resources like memory or processor. It is used 
    to run instructions parsed by `pseudo.lexer.Lexer`.

    Attributes:
        - var: dict, In this object all variables will be stored. Arrays are stored as independent
            keys i.e.::
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

    def __init__(self):
        self.var = {}

    def save(self, key: str, value: object, object_class=MemoryObject):
        """
        This functions is used to save variable's value in memory
        
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
        This function returns value of stored variable.
        
        Args:
            - key: str, Key under which value is stored.
        """

        if key in self.var:
            return self.var[key].getter()
        else:
            return "nil"

    def delete(self, key: str):
        """This function removes variable from memory."""
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

    def eval(self, instruction):
        """Evaluate instruction."""
        try:
            instruction.eval(self)
        except RunTimeError as err:
            self.throw(err, instruction.line)

    def run(self, instructions: list):
        """Run pseudocode instructions"""
        try:
            for i in instructions:
                self.eval(i)
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

        print(f"⚠️  Error on line :")
        print(f"\t'{line_causing_error}'")
        print(error_message)
        exit(1)
