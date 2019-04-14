import os
import subprocess

from pseudo import compile, main, __version__
from pseudo.type import Int, Statement


def test_compile():
    if compile("pisz 4") != [Statement("pisz", args=Int(4))]:
        print(compile("pisz 4"))
        raise AssertionError


def test_main():
    with open("t1.pdc", "w") as fp:
        fp.write("pisz 4")
    if subprocess.getoutput("python3 pdc.py t1.pdc") != "4":
        print(subprocess.getoutput("python3 pdc.py t1.pdc"))
        raise AssertionError
    os.remove("t1.pdc")

    if subprocess.getoutput("python3 pdc.py -v") != __version__:
        print(subprocess.getoutput("python3 pdc.py -v"))
        raise AssertionError

    if subprocess.run(["python3", "pdc.py"]).returncode == 0:
        print(subprocess.run(["python3", "pdc.py"]).returncode)
        raise AssertionError
