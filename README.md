![pseudo](pseudo.svg)

<!--<img style="height:60px" src="pseudo.svg">-->

A prototype of pseudocode interpreter.

## Goal

Goal of this project is to enable property and other kinds of testing in pseudocode exercises.

## Install

There are two options of installing pseudo

### 1. pip

python3.6 or greater

```bash
pip3 install git+https://github.com/pniedzwiedzinski/pseudo.git
```

### 2. Docker

Download docker and follow instructions:

```bash
docker pull pniedzwiedzinski/pseudo

# Create alias
alias pseudo='docker run -it --rm -v $(pwd):/home pseudo'
```

## Usage

Create sample file `file.pdc`

```
pisz "test"
```

To run it type:

```bash
pseudo file.pdc
```

## Sample pseudocode

test.pdc

```
czytaj n
pisz "Start"
# Pętla wypisuje liczby parzyste od 1 do `n`
dla i=1,...,n wykonuj
    jeżeli i mod 2 = 0 to
        pisz i
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
- [ ] for loop
- [x] arrays
- [ ] functions

## How it works

W.I.P.

http://pseudo.readthedocs.io
