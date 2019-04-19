"""This module contains functions used to run pseudocode."""

__author__ = "Patryk Niedźwiedziński"

import datetime
import traceback
import os

from pseudo.runtime import RunTime


def run(instructions: list, r: RunTime = RunTime()):
    """Run pseudocode string"""
    try:
        for i in instructions:
            i.eval(r)
    except Exception:
        now = datetime.datetime.now().strftime("%H-%M-%S-%d-%m-%Y")
        try:
            os.mkdir("crash")
        except FileExistsError:
            pass
        with open(f"crash/{now}.log", "w") as fp:
            fp.write(traceback.format_exc())
        print("⚠️  Error: \n\tRuntime error has occurred!\n")
        print(
            "Wow! You encountered a bug! Please tell me how did you do that on https://github.com/pniedzwiedzinski/pseudo/issues\n"
        )
        print(f"Error message was copied to {os.getcwd()}/crash/{now}.log")
        exit(1)

