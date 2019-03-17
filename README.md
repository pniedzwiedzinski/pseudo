# pseudo

A prototype for pseudocode interpreter. Currently it's only building AST.

## Goal

Goal of this project is to enable property and other kinds of testing in pseudocode exercises.

## Install

```bash
pip3 install git+https://github.com/pniedzwiedzinski/pseudo.git
```

### Requirements

- python3.6 or greater

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
