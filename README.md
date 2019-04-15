![pseudo](pseudo.svg)

<!--<img style="height:60px" src="pseudo.svg">-->

A prototype of pseudocode interpreter.

- Linux: [![CircleCI](https://circleci.com/gh/pniedzwiedzinski/pseudo/tree/master.svg?style=svg)](https://circleci.com/gh/pniedzwiedzinski/pseudo/tree/master)
- MacOs: [![TravisCI](https://travis-ci.com/pniedzwiedzinski/pseudo.svg?branch=master)](https://travis-ci.com/pniedzwiedzinski/pseudo)
- Windows: ![Appveyor](https://ci.appveyor.com/api/projects/status/mb619aaflsyamen8/branch/master?svg=true)

[![Maintainability](https://api.codeclimate.com/v1/badges/f204e006912933370b41/maintainability)](https://codeclimate.com/github/pniedzwiedzinski/pseudo/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f204e006912933370b41/test_coverage)](https://codeclimate.com/github/pniedzwiedzinski/pseudo/test_coverage)

## Goal

Goal of this project is to enable property and other kinds of testing in pseudocode exercises.

## Install

There are two options of installing pseudo

### 1. pip

python3.6 or greater. On windows you might need to have `pypiwin32` installed

```bash
pip3 install git+https://github.com/pniedzwiedzinski/pseudo.git
```

### 2. Docker

Download docker and follow instructions:

```bash
docker pull pniedzwiedzinski/pseudo

# Create alias
alias pdc='docker run -it --rm -v $(pwd):/home pseudo'
```

## Usage

Create sample file `file.pdc`

```
pisz "test"
```

To run it type:

```bash
pdc file.pdc
```

## Sample pseudocode

test.pdc

```
czytaj n
pisz "Start"
# Pętla wypisuje liczby parzyste od 1 do `n`
i:=1
dopóki i<=n wykonuj
    jeżeli i mod 2 = 0 to
        pisz i
        T[i] := 1
    wpp
        pisz "nie"
    pisz "\n"
    i:=i+1

dla a:=1,...,5 wykonuj
    pisz a
```

## Features

- [x] printing
- [x] math operations
- [x] math operations order
- [ ] type errors
- [x] input variable
- [x] variables
- [x] `koniec`
- [x] conditional statement
- [x] while loop
- [x] for loop
- [x] arrays
- [ ] functions

## How it works

W.I.P.

http://pseudo.readthedocs.io
