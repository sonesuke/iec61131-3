import pytest
from iec_ast import *
from llvm import *
from llvm.core import *
from llvm.ee import *


def test_function():
    args_input = [
        iec_arg("a", "integer"),
        iec_arg("b", "integer"),
    ]
    args_local = [
        iec_arg("c", "integer"),
        iec_arg("d", "integer"),
    ]
    args = [iec_args_input(args_input), iec_args_local(args_local)]
    statements = [
        iec_statement_return(iec_val(3))
    ]
    f = iec_function("my_func", "integer", args, statements)

    c = context()
    c.module = Module.new('my_module')
    v = f.generate_code(c)

    gf = c.module.get_function_named("my_func")

    e = ExecutionEngine.new(c.module)
    arg1 = GenericValue.int(Type.int(), 1)
    arg2 = GenericValue.int(Type.int(), 2)

    retval = e.run_function(gf, [arg1, arg2])
    assert retval.as_int() == 3


def test_function_expression():
    args_input = [
        iec_arg("a", "integer"),
        iec_arg("b", "integer"),
    ]
    args = [iec_args_input(args_input)]
    statements = [
        iec_statement_return(iec_binary_operator("+", iec_val(2), iec_val(3))),
    ]
    f = iec_function("my_func", "integer", args, statements)

    c = context()
    c.module = Module.new('my_module')
    v = f.generate_code(c)

    gf = c.module.get_function_named("my_func")
    arg1 = GenericValue.int(Type.int(), 1)
    arg2 = GenericValue.int(Type.int(), 2)
    e = ExecutionEngine.new(c.module)

    retval = e.run_function(gf, [arg1, arg2])
    assert retval.as_int() == 5


def test_function_expression():
    args_input = [
        iec_arg("a", "integer"),
        iec_arg("b", "integer"),
    ]
    args = [iec_args_input(args_input)]
    statements = [
        iec_statement_return(iec_binary_operator("+", iec_val(2), iec_val(3))),
    ]
    f = iec_function("my_func", "integer", args, statements)

    c = context()
    c.module = Module.new('my_module')
    v = f.generate_code(c)

    gf = c.module.get_function_named("my_func")
    arg1 = GenericValue.int(Type.int(), 1)
    arg2 = GenericValue.int(Type.int(), 2)
    e = ExecutionEngine.new(c.module)

    retval = e.run_function(gf, [arg1, arg2])
    assert retval.as_int() == 5


def test_function_variable_expression():
    args_input = [
        iec_arg("a", "integer"),
        iec_arg("b", "integer"),
    ]
    args = [iec_args_input(args_input)]
    statements = [
        iec_statement_return(
            iec_binary_operator("+", iec_variable('a'), iec_variable('b'))),
    ]
    f = iec_function("my_func", "integer", args, statements)

    c = context()
    c.module = Module.new('my_module')
    v = f.generate_code(c)

    gf = c.module.get_function_named("my_func")
    arg1 = GenericValue.int(Type.int(), 1)
    arg2 = GenericValue.int(Type.int(), 2)
    e = ExecutionEngine.new(c.module)

    retval = e.run_function(gf, [arg1, arg2])
    assert retval.as_int() == 3
