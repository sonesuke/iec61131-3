from llvm import *
from llvm.core import *


def type_generate(text):
    return Type.int()


class symbol:

    def __init__(self, llvm_type, alloca):
        self.llvm_type = llvm_type
        self.alloca = alloca


class context:

    counter = 0

    def __init__(self):
        self.module = None
        self.function = None
        self.builder = None
        self.symbols = {}

    def get_id(self):
        context.counter += 1
        return str(context.counter)


class iec_function:

    def __init__(self, name, type_string, args_section, statements):
        self.name = name
        self.type_string = type_string
        self.args_section = args_section
        self.statements = statements

    def get_function_args(self):
        for args in self.args_section:
            if isinstance(args, iec_args_input):
                return args
        return iec_args_input([])

    def generate_function(self, context):
        ret_type = type_generate(self.type_string)
        function_args = self.get_function_args()
        ty_func = Type.function(ret_type, function_args.types())
        f = context.module.add_function(ty_func, self.name)
        names = function_args.names()
        for i in range(len(names)):
            f.args[i] = names[i]
        return f

    def generate_args_alloca(self, context):
        for args in self.args_section:
            args.generate_code(context)

    def generate_code(self, context):
        context.function = self.generate_function(context)
        basic_block = context.function.append_basic_block("entry")
        builder = Builder.new(basic_block)
        context.builder = builder
        self.generate_args_alloca(context)
        for s in self.statements:
            s.generate_code(context)
        return context.function


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

    def generate_code(self, context):
        for i in range(len(self.args)):
            llvm_type = type_generate(self.args[i].type_string)
            alloca = context.builder.alloca(
                llvm_type,
                None,
                "__tmp_" + context.get_id())
            context.builder.store(context.function.args[i], alloca)
            context.symbols[self.args[i].name] = symbol(llvm_type, alloca)


class iec_args_local:

    def __init__(self, args):
        self.args = args

    def generate_code(self, context):
        for i in range(len(self.args)):
            llvm_type = type_generate(self.args[i].type_string)
            alloca = context.builder.alloca(
                llvm_type,
                None,
                "__tmp_" + context.get_id())
            context.symbols[self.args[i].name] = symbol(llvm_type, alloca)


class iec_statement_return:

    def __init__(self, expression):
        self.expression = expression

    def generate_code(self, context):
        return_value = self.expression.generate_code(context)
        context.builder.ret(return_value)


class iec_statement_assign:

    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def generate_code(self, context):
        assign_value = self.expression.generate_code(context)
        context.builder.store(assign_value, self.symbols[self.variable].alloca)


class iec_val:

    def __init__(self, val):
        self.val = val

    def generate_code(self, context):
        return Constant.int(Type.int(), int(self.val))


class iec_variable:

    def __init__(self, variable):
        self.variable = variable

    def generate_code(self, context):
        alloca = context.symbols[self.variable].alloca
        return context.builder.load(alloca, "__tmp_" + context.get_id())


class iec_binary_operator:

    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def generate_code(self, context):
        lhs = self.lhs.generate_code(context)
        rhs = self.rhs.generate_code(context)
        if self.op == "+":
            return context.builder.add(lhs, rhs, "__tmp_" + context.get_id())
        elif self.op == "-":
            return context.builder.sub(lhs, rhs, "__tmp_" + context.get_id())
        if self.op == "*":
            return context.builder.mul(lhs, rhs, "__tmp_" + context.get_id())
        elif self.op == "/":
            return context.builder.div(lhs, rhs, "__tmp_" + context.get_id())
        assert(False)


class iec_unary_operator:

    def __init__(self, op, val):
        self.op = op
        self.val = val

    def generate_code(self, context):
        val = self.val.generate_code(context)
        if self.op == "+":
            return val
        elif self.op == "-":
            return context.builder.neg(val, "__tmp_" + context.get_id())
        assert(False)
