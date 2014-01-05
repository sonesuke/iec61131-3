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

ConstantVal = Literal('#') + Word(nums)
ConstantVal.setParseAction(lambda ts: iec_val(ts[1]))

Term = ConstantVal

SignOpe = oneOf('+ -')
MultOpe = oneOf('* /')
PlusOpe = oneOf('+ -')

Operators = [
    (SignOpe, 1, opAssoc.RIGHT, lambda ts:
     iec_unary_operator(ts[0][0], ts[0][1])),
    (MultOpe, 2, opAssoc.LEFT, lambda ts:
        iec_binary_operator(ts[0][1], ts[0][0], ts[0][2])),
    (PlusOpe, 2, opAssoc.LEFT, lambda ts:
        iec_binary_operator(ts[0][1], ts[0][0], ts[0][2])),
]

Expression = operatorPrecedence(Term, Operators)

ReturnStatement = Keyword('return') + Expression + Literal(';')
ReturnStatement.setParseAction(
    lambda ts: iec_statement_return(ts[1]))

AssignmentStatement = Expression.setResultsName('Exp')
AssignmentStatement.setParseAction(
    lambda ts: iec_statement_return(ts['Exp']))

Statement = ReturnStatement | AssignmentStatement

Function = CaselessKeyword('function') + \
    Name.setResultsName('Name') + \
    CaselessLiteral(':') + \
    Type.setResultsName('Type') + \
    ZeroOrMore(Args).setResultsName('Args') + \
    ZeroOrMore(Statement).setResultsName('Statements') + \
    CaselessKeyword('end_function')
Function.setParseAction(
    lambda ts: iec_function(
        ts['Name'],
        ts['Type'],
        ts.get('Args'),
        ts.get('Statements')))


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

    def expression(self, text):
        return Expression.parseString(text)[0]

    def statement(self, text):
        return Statement.parseString(text)[0]

    def function(self, text):
        return Function.parseString(text)[0]
