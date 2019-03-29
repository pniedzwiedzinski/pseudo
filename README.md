![pseudo](pseudo.svg)

<!--<img style="height:60px" src="pseudo.svg">-->

A prototype for pseudocode interpreter.

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

## Features

- [x] `pisz 2`, `pisz "hello"`, `pisz prawda`
- [x] `pisz 2+2`, `pisz 2-2`
- [x] `pisz 2*2`, `pisz 2 div 2`
- [x] `x mod 2`
- [x] `czytaj x`
- [x] `x := x+2`, `x <- 0-x`
- [x] `x := -x`
- [x] `koniec`
- [x] `jeżeli .. to`
- [x] `dopóki .. wykonuj`
- [ ] `dla .. wykonuj`
