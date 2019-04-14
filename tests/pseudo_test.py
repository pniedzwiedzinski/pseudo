import os
import subprocess
import platform

from pseudo import compile, main, __version__
from pseudo.type import Int, Statement


def test_compile():
    if compile("pisz 4") != [Statement("pisz", args=Int(4))]:
        print(compile("pisz 4"))
        raise AssertionError


def test_main():
    with open("t1.pdc", "w") as fp:
        fp.write("pisz 4")

    cmd = "python pdc.py t1.pdc"
    if subprocess.getoutput(cmd) != "4":
        print(subprocess.getoutput(cmd))
        raise AssertionError
    os.remove("t1.pdc")

    cmd = "python pdc.py -v"
    if subprocess.getoutput(cmd) != __version__:
        print(subprocess.getoutput(cmd))
        raise AssertionError

    cmd = ["python", "pdc.py"]
    if subprocess.run(cmd).returncode == 0:
        print(subprocess.run(cmd).returncode)
        raise AssertionError
