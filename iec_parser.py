from iec_ast import *
from pyparsing import *


Name = Word(alphas)
Type = Word(alphas)

Arg = Name.setResultsName('Name') + \
    Literal(':') + Type.setResultsName('Type') + Literal(';')
Arg.setParseAction(lambda ts: iec_arg(ts['Name'], ts['Type']))

ArgsInput = CaselessKeyword('var_input') + \
    Group(OneOrMore(Arg)).setResultsName('Args') + \
    CaselessKeyword('end_var')
ArgsInput.setParseAction(lambda ts: iec_args_input(ts['Args']))


ArgsLocal = CaselessKeyword('var') + \
    Group(OneOrMore(Arg)).setResultsName('Args') + \
    CaselessKeyword('end_var')
ArgsLocal.setParseAction(lambda ts: iec_args_local(ts['Args']))

Args = ArgsInput | ArgsLocal

Function = CaselessKeyword('function') + \
    Name.setResultsName('Name') + \
    CaselessLiteral(':') + \
    Type.setResultsName('Type') + \
    ZeroOrMore(Args).setResultsName('Args') + \
    CaselessKeyword('end_function')
Function.setParseAction(
    lambda ts: iec_function(ts['Name'], ts['Type'], ts.get('Args')))


class Parser(object):

    def __init__(self):
        pass

    def arg(self, text):
        return Arg.parseString(text)[0]

    def args_input(self, text):
        return ArgsInput.parseString(text)[0]

    def args_local(self, text):
        return ArgsLocal.parseString(text)[0]

    def args(self, text):
        return Args.parseString(text)

    def function(self, text):
        return Function.parseString(text)[0]
