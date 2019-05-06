import os
import codecs
import subprocess
import platform

from pseudo import compile, __version__
from pseudo.cli import pdc
from pseudo.type import Int, Statement, EOL


def test_compile():
    if compile("pisz 4") != [Statement("pisz", args=Int(4)), EOL()]:
        print(compile("pisz 4"))
        raise AssertionError


script = """
a := 1
jeżeli a=1 to
    T[a] := a
    pisz a

dopóki a < 2 wykonuj
    T[a] := a
    a:=a+1
pisz "2"

dla i:=3,...,5 wykonuj
    dla x:=3,...,5 wykonuj
        T[x] <- x
        pisz x

koniec
"""


def test_main():
    with codecs.open("t1.pdc", encoding="utf-8", mode="w") as fp:
        fp.write(script)
    cmd = "python3 pdc.py t1.pdc"
    if platform.system() == "Windows":
        cmd = cmd.replace("3", "")
    if subprocess.getoutput(cmd) != "12345345345":
        print(cmd)
        print(subprocess.getoutput(cmd))
        raise AssertionError
    os.remove("t1.pdc")

    cmd = "python3 pdc.py -v"
    if platform.system() == "Windows":
        cmd = cmd.replace("3", "")
    if subprocess.getoutput(cmd) != __version__:
        print(cmd)
        print(subprocess.getoutput(cmd))
        raise AssertionError

    cmd = ["python3", "pdc.py"]
    if platform.system() == "Windows":
        cmd[0] = cmd[0].replace("3", "")
    if subprocess.run(cmd).returncode == 0:
        print(cmd)
        print(subprocess.run(cmd).returncode)
        raise AssertionError
