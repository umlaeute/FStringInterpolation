#!/usr/bin/env python3

# FStringInterpolation - tests

import configparser
import pytest

import fstringinterpolation

pi = "3.1415926535897932384626433832795"

inistring = r"""
[DEFAULT]
a = %s
title = {a} is {"more" if float(a) > float(b) else "less"} than {b}
[basic]
b = two_%%(a)s
c = three_%%(b)s
[fstring]
b = two_{a}
c = three_{b}
[more]
b = 0
[more2]
b = {(float(a)-1)}
[less]
b = 42
[less2]
b = {(float(a)+1)}
[shortfloat]
pi = {float(a):.2f}
[shortstring]
pi = {a:.2s}
[halfpi]
halfpi = {float(a)/2}
[badhalfpi]
halfpi = {a/2}
[sum]
a = 4
b = 5
realsum = {sum(float(_) for _ in [a,b])}
[badsum]
b = 5
sum = {sum(float(_) for _ in [a,b])}
[backslash]
forward = /1
backward = \1
""" % (
    pi,
)


## helpers


def read_config(configstring: str, raw_string=False, filename=None):
    if raw_string:
        interpolation = fstringinterpolation.FStringInterpolationRaw
    else:
        interpolation = fstringinterpolation.FStringInterpolation

    cfg = configparser.ConfigParser(interpolation=interpolation())
    if filename:
        cfg.read([filename])
    else:
        cfg.read_string(configstring)
    return cfg


def get(section, option):
    cfg = read_config(inistring)
    return cfg[section][option]


def getraw(section, option):
    cfg = read_config(inistring, raw_string=True)
    return cfg[section][option]


## the actual tests
section_option_value = [
    ("basic", "a", pi),
    ("basic", "b", f"two_%(a)s"),
    ("basic", "c", f"three_%(b)s"),
    ("fstring", "a", pi),
    ("fstring", "b", f"two_{pi}"),
    ("fstring", "c", f"three_two_{pi}"),
    ("more", "a", pi),
    ("more", "b", "0"),
    ("more", "title", f"{pi} is more than 0"),
    ("more2", "a", pi),
    # ("more2", "title", f"{pi} is more than 0"),
    ("less", "a", pi),
    ("less", "b", "42"),
    ("less", "title", f"{pi} is less than 42"),
    ("less2", "a", pi),
    # ("less2", "title", f"{pi} is less than 42"),
    ("shortfloat", "a", pi),
    ("shortfloat", "pi", f"{float(pi):.2f}"),
    ("shortstring", "a", pi),
    ("shortstring", "pi", pi[:2]),
    ("sum", "a", "4"),
    ("sum", "b", "5"),
    ("badsum", "a", "3.1415926535897932384626433832795"),
    ("badsum", "b", "5"),
    ("backslash", "forward", "/1"),
]


@pytest.mark.parametrize(
    "section,option,value",
    section_option_value + [("backslash", "backward", "\1")],
)
def test_get(section, option, value):
    assert get(section, option) == value


@pytest.mark.parametrize(
    "section,option,value",
    section_option_value + [("backslash", "backward", r"\1")],
)
def test_getraw(section, option, value):
    assert getraw(section, option) == value


@pytest.mark.parametrize(
    "section,option,value",
    [
        ("less2", "b", float(pi) + 1),
        ("halfpi", "halfpi", float(pi) / 2),
        ("sum", "realsum", 9),
    ],
)
def test_getfloat(section, option, value):
    assert float(get(section, option)) == value


@pytest.mark.parametrize(
    "section,option,exception",
    [
        ("more", "c", KeyError),
        ("more2", "c", KeyError),
        ("shortfloat", "title", configparser.InterpolationMissingOptionError),
        ("shortstring", "title", configparser.InterpolationMissingOptionError),
        ("badhalfpi", "halfpi", configparser.InterpolationError),
        ("badsum", "sum", configparser.InterpolationError),
    ],
)
def test_raises(section, option, exception):
    with pytest.raises(exception):
        get(section, option)


@pytest.mark.xfail(reason="needs fixing")
def test_more2_title():
    assert get("more2", "title") == f"{pi} is more than 0"


@pytest.mark.xfail(reason="needs fixing")
def test_less2_title():
    assert get("less2", "title") == f"{pi} is less than 42"
