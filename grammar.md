# Grammar of pseudocode

## Data types

- `4` - Int
- `4.2` - Float #WIP
- `"hello"` - String
- `prawda` - Bool

## Operations

- `+` - addition of two numeric values
- `-` - substraction, same as above
- `*` - multiplication, same as above
- `/` - division, same as above
- `div` - integer division, only on Ints
- `mod` - division remainder, only on Ints

### Bool operations #WIP

- `and`
- `or`
- `not`

## Variables

To create new variable assign value to it. Pseudocode has dynamic typing.

```
a := 1
```
or
```
a <- 1
```

### Incrementing

Pseudocode has no incrementing mechanism, neither increasing, so you need to type exact new value.

```
a := a + 1
```

### Swapping #WIP

Pseudocode has built-in swapping operator

```
a <-> b
```

## Comments

Everything after `#` will be ignored

## IO

```
pisz a
```

`pisz` can take only one argument, `pisz a, b` is not correct!


```
czytaj a
```

`czytaj` as well can take only one argument

## Conditionals operations

```
jeżeli a=1 to
  pisz "A is equal to 1"
wpp
  pisz "A is not equal to 1"
```

Multiple conditions #WIP

```
if not (a>1 and a<5) or a=3 then # a in [-∞, 1] or a in [5, ∞] or a=3
  print a
```

## Loops

### while

```
dopóki a < 10 wykonuj
  a := a + 1
```

### do while #WIP

```
do
  a := a + 1
while a < 10
```

### for

```
dla i:=1,...,a wykonuj
  pisz i
```

## Functions and procedures #WIP

```
function Test(arg1, arg2)
  if arg1 > arg2 then
    arg1 := arg1 + 1
  return arg1
```

```
procedure Zero(T, n)
  for i:=1,...,n do
    T[i] := 0
```
