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

1. Download executable from here: [download](https://github.com/pniedzwiedzinski/pseudo/releases/latest).
2. Extract archive
3. Add folder with extracted files to [PATH](<https://en.wikipedia.org/wiki/PATH_(variable)>)

If you're on macOs or Linux you probably have python3 installed. Then it will be easier to install it with [pip](#1-pip)

### Install from source

#### 1. pip

python3.6 or greater. On windows you might need to have `pypiwin32` installed

```bash
python3 -m pip install git+https://github.com/pniedzwiedzinski/pseudo.git
```

#### 2. Docker

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
- [x] type errors
- [x] input variable
- [x] variables
- [x] `koniec`
- [x] conditional statement
- [x] while loop
- [x] for loop
- [x] arrays
- [x] functions

## How it works

W.I.P.

http://pseudo.readthedocs.io
