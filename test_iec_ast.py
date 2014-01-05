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
    f = iec_function("my_func", "integer", args)

    m = Module.new('my_module')
    v = f.generate_code(m)

    gf = m.get_function_named("my_func")

    e = ExecutionEngine.new(m)
    arg1 = GenericValue.int(Type.int(), 1)
    arg2 = GenericValue.int(Type.int(), 2)

    retval = e.run_function(gf, [arg1, arg2])
    assert retval.as_int() == 3
