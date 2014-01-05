import pytest
from iec_parser import *
from iec_ast import *


def test_arg():
    a = parse_arg("""
            a: integer;
            """)
    assert isinstance(a, iec_arg)
    assert a.name == 'a'
    assert a.type_string == 'integer'


def test_args():
    a = parse_args("""
            var_input
            a: integer;
            b: integer;
            end_var
            """)
    print(a)
    assert len(a) == 2
    assert a[0].name == 'a'
    assert a[0].type_string == 'integer'
    assert a[1].name == 'b'
    assert a[1].type_string == 'integer'


def test_function():
    f = parse_function("""
            function hoge: integer
            end_function
            """)
    assert isinstance(f, iec_function)
    assert f.name == "hoge"
    assert f.type_string == "integer"


def test_function_with_arg():
    f = parse_function("""
            function hoge: integer
            var_input
                a : integer;
            end_var

            end_function
            """)
    assert isinstance(f, iec_function)
    assert f.name == "hoge"
    assert f.type_string == "integer"
    assert f.args[0].name == 'a'
    assert f.args[0].type_string == 'integer'
