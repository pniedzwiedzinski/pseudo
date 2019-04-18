"""This module contains RunTime class, which is a representation of runtime resources."""

__author__ = "Patryk Niedźwiedziński"

from sys import exit

class RunTime:
    """
    This class is a representation of computer resources like memory or processor.
    
    Attributes:
        - var: dict, In this object all variables will be stored.
    """

    def __init__(self):
        self.var = {}

    def set_nested_array(self, key: str, indices: list):
        """
        This function returns pointer to nested array in `var`

        Args:
            - key: str, Key under which array will be stored.
            - indices: list of objects, List of indexes, for example
                `T[a][b]` will have indices `[a, b]`.
        """

        pointer = self.var[key]

        for k in indices: # For each index go to lower array
            try:
                pointer = pointer[k.eval(self)]
            except KeyError:
                pointer[k.eval(self)] = {}
                pointer = pointer[k.eval(self)]
        return pointer

    def save(self, key: str, value: object, indices: list = []):
        """
        This functions is used to save value in `var`.
        
        Args:
            - key: str, Unique key under which value will be stored.
            - value: object, Value to store.
            - indices: list of objects, If variable is an array. 
                For example `T[a][b]` will have indices `[a, b]`.
        """

        # Simple variable set
        if not indices:
            self.var[key] = value.eval(self)
            return None

        # Check if array exists
        if key not in self.var:
            self.var[key] = {}
        
        # Get pointer from nested array to wanted index
        v = self.set_nested_array(key, indices[:-1])

        v[indices[-1].eval(self)] = value.eval(self)

    def get(self, key: str, indices: list = []):
        """
        This function returns value stored under key.
        
        Args:
            - key: str, Key under which value is stored.
            - indices: list of objects, If variable is array, for example 
                `T[a][b]` will have indices `[a, b]`.
        """

        try:
            v = self.var[key]
            for k in indices:
                v = v.__getitem__(k.eval(self))
            return v
        except KeyError:
            return "nil"

    def stdin(self, key: str, indices: list = []):
        """Read from stdin and store it in `var`."""
        value = input(f"{key}: ")

        try: # value is a string by default
            value = int(value)
        except TypeError:
            pass

        self.save(key, value, indices)

    def stdout(self, key: str, indices: list = []):
        """Write to stdout from `var`"""
        value = self.get(key, indices)
        
        if value == "\\n":
            print("")
        else:
            print(value, end="")

    def throw(self, error_message: str, line_causing_error: str = ""):
        """This function is used to tell user that a runtime error has occurred."""

        print(f"⚠️  Runtime error:")
        print(f"\t{line_causing_error}")
        print(error_message)
        exit(1)