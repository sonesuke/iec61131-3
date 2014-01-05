import pytest
from iec_parser import Parser
from iec_ast import *


def test_arg():
    p = Parser()
    a = p.arg("""
            a: integer;
            """)
    assert isinstance(a, iec_arg)
    assert a.name == 'a'
    assert a.type_string == 'integer'


def test_args_local():
    p = Parser()
    a = p.args_local("""
            var
            a: integer;
            b: integer;
            end_var
            """)
    assert isinstance(a, iec_args_local)
    assert len(a.args) == 2
    assert a.args[0].name == 'a'
    assert a.args[0].type_string == 'integer'
    assert a.args[1].name == 'b'
    assert a.args[1].type_string == 'integer'


def test_args_input():
    p = Parser()
    a = p.args_input("""
            var_input
            a: integer;
            b: integer;
            end_var
            """)
    assert isinstance(a, iec_args_input)
    assert len(a.args) == 2
    assert a.args[0].name == 'a'
    assert a.args[0].type_string == 'integer'
    assert a.args[1].name == 'b'
    assert a.args[1].type_string == 'integer'


def test_function():
    p = Parser()
    f = p.function("""
            function hoge: integer
            end_function
            """)
    assert isinstance(f, iec_function)
    assert f.name == "hoge"
    assert f.type_string == "integer"


def test_expression():
    p = Parser()
    e = p.expression("#3")
    assert isinstance(e, iec_val)
    assert e.val == "3"
    e = p.expression("#2+#2")
    assert isinstance(e, iec_binary_operator)
    assert e.op == "+"


def test_statement():
    p = Parser()
    s = p.statement("return #3;")
    assert isinstance(s, iec_statement_return)
    assert isinstance(s.expression, iec_val)
    assert s.expression.val == "3"


def test_function_with_arg():
    p = Parser()
    f = p.function("""
            function hoge: integer
            var_input
                a : integer;
            end_var
            return #3;
            end_function
            """)
    assert isinstance(f, iec_function)
    assert f.name == "hoge"
    assert f.type_string == "integer"
    assert f.args_section[0].args[0].name == 'a'
    assert f.args_section[0].args[0].type_string == 'integer'
