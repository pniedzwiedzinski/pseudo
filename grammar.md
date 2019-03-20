# Grammar of pseudocode

## Data types

- `4` - Int
- `4.2` - Float
- `"hello"` - String
- `true` - Bool

## Operations

- `+` - addition of two numeric values
- `-` - substraction, same as above
- `*` - multiplication, same as above
- `/` - division, same as above
- `div` - integer division, only on Ints
- `mod` - division remainder, only on Ints

### Bool operations

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

### Swapping

Pseudocode has built-in swapping operator

```
a <-> b
```

## Comments

Everything after `#` will be ignored

## Printing

```
print a
```

`print` can take only one argument, `print a, b` is not correct!

## Conditionals operations

```
if a=1 then
  print "A is equal to 1"
else
  print "A is not equal to 1"
```

Multiple conditions

```
if not (a>1 and a<5) or a=3 then # a in [-∞, 1] or a in [5, ∞] or a=3
  print a
```

## Loops

### while

```
while a < 10 do
  a := a + 1
```

### do while

```
do
  a := a + 1
while a < 10
```

### for

```
for i:=1,...,a do
  print i
```

## Functions and procedures

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
