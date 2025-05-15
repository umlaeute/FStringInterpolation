FStringInterpolation - interpolation `configparser` that does f-string substitution
===================================================================================

Extended *Interpolation* for the normal [Python `configparser`](https://docs.python.org/3/library/configparser.html)

- Apply f-string interpolation on values


## Usage

```python
>>> import configparser
>>> from fstringinterpolation import FStringInterpolation
>>> config = configparser.ConfigParser(interpolation=FStringInterpolation())
>>> config.read_string("""
[DEFAULT]
_pi = 3.141592653589793238462643383279502884197169399375105820974944592307816406286

[full]
pi = {_pi}

[short]
pi = {float(_pi):.2f}
""")
>>> config["full"]["pi"]
'3.141592653589793238462643383279502884197169399375105820974944592307816406286'
>>> config["short"]["pi"]
'3.14'
```

## More examples

This will automatically create the proper *title*, depending on the values of *a* and *b*

#### Input
```ini
[DEFAULT]
a = 7
title = {a} is {"more" if float(a) > float(b) else "less"} than {b}

[A]
b = 12

[B]
b = 3


[C]
a = 3.14
b = 2.71
```

#### Output

| section | title                    |
|---------|--------------------------|
| A       | "7 is less than 12"      |
| B       | "7 is more than 3"       |
| C       | "3.14 is more than 2.71" |


## Caveats
- no recursion!
  e.g. the following is invalid:
  ```ini
  [DEFAULT]
  pi = 3.141592654
  [int]
  pi = {float(pi)}
  ```

- the type of each value is always <str>.
  if you need something else, you must explicitely convert the values:
  ```ini
  [DEFAULT]
  pi = 3.141592654
  [bad]
  halfpi = {pi/2}
  [good]
  halfpi = {float(pi)/2}

- care must be taken to not override python built-ins (that you want to use) with variables:
  ```ini
  [DEFAULT]
  a = 10
  b = 12
  [good]
  realsum = {sum(float(_) for _ in [a,b])}
  [bad]
  realsum = {sum(float(_) for _ in [a,b])}
  sum = 22
  [bad recursion]
  sum = {sum(float(_) for _ in [a,b])}
  ```
