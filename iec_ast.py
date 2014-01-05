from llvm import *
from llvm.core import *


def type_generate(text):
    return Type.int()


class iec_function:

    def __init__(self, name, type_string, args_section):
        self.name = name
        self.type_string = type_string
        self.args_section = args_section

    def get_function_args(self):
        for args in self.args_section:
            if isinstance(args, iec_args_input):
                return args
        return iec_args_input([])

    def generate_code(self, mod):
        ret_type = type_generate(self.type_string)
        function_args = self.get_function_args()
        ty_func = Type.function(ret_type, function_args.types())
        f = mod.add_function(ty_func, self.name)
        names = function_args.names()
        for i in range(len(names)):
            f.args[i] = names[i]
        basic_block = f.append_basic_block("entry")
        builder = Builder.new(basic_block)
        tmp = builder.add(f.args[0], f.args[1], "tmp")
        builder.ret(tmp)


class iec_arg:

    def __init__(self, name, type_string):
        self.name = name
        self.type_string = type_string


class iec_args_input:

    def __init__(self, args):
        self.args = args

    def types(self):
        return [type_generate(t.type_string) for t in self.args]

    def names(self):
        return [t.name for t in self.args]


class iec_args_local:

    def __init__(self, args):
        self.args = args
