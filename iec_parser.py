from iec_ast import *
from pyparsing import *


Name = Word(alphas)
Type = Word(alphas)

Arg = Name.setResultsName('Name') + \
    Literal(':') + Type.setResultsName('Type') + Literal(';')
Arg.setParseAction(lambda ts: iec_arg(ts['Name'], ts['Type']))

Args = CaselessKeyword('var_input') + \
    Group(OneOrMore(Arg)).setResultsName('Args') + \
    CaselessKeyword('end_var')
Args.setParseAction(lambda ts: ts['Args'])

Function = CaselessKeyword('function') + \
    Name.setResultsName('Name') + \
    CaselessLiteral(':') + \
    Type.setResultsName('Type') + \
    Optional(Args).setResultsName('Args') + \
    CaselessKeyword('end_function')
Function.setParseAction(
    lambda ts: iec_function(ts['Name'], ts['Type'], ts.get('Args')))


def parse_arg(text):
    return Arg.parseString(text)[0]


def parse_args(text):
    return Args.parseString(text)


def parse_function(text):
    return Function.parseString(text)[0]
