import functools
from lexer import *
from combinators import *
from ast import *

# Basic parsers
def keyword(kw):
    return Reserved(kw, RESERVED)


num = Tag(INT) ^ (lambda i: int(i))
identifier = Tag(ID)
string = String(STRING)


# Top level parser
def parse(tokens):
    ast = parser()(tokens, 0)
    return ast


def parser():
    return Phrase(stmt_list())


# Statements
def stmt_list():
    separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)


def stmt():
    return assign_stmt() | for_stmt() | if_stmt() | while_stmt() | print_stmt() | input_stmt() | func_call() | func_stmt()


def assign_stmt():
    def process(parsed):
        ((name, _), stm) = parsed
        return AssignStatement(name, stm)

    return identifier + keyword('=') + exp() ^ process


def input_stmt():
    def process(parsed):
        (_, name) = parsed
        return InputStatement(name)

    return keyword('input') + identifier ^ process


def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfStatement(condition, true_stmt, false_stmt)

    return keyword('if') + bexp() + keyword('then') + Lazy(stmt_list) + Opt(keyword('else') + Lazy(stmt_list)) + keyword('end') ^ process


def while_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileStatement(condition, body)

    return keyword('while') + bexp() + keyword('do') + Lazy(stmt_list) + keyword('end') ^ process


def for_stmt():
    def process(parsed):
        ((((((((_, name), _), start), _), end), _), body), _) = parsed
        return ForStatement(name, start, end, body)

    return keyword('for') + identifier + keyword('=') + aexp() + keyword('to') + aexp() + keyword('do') + Lazy(stmt_list) + keyword('end') ^ process


def func_stmt():
    def process(parsed):
        ((((_, name), _), body), _) = parsed
        return FunctionStatement(name, body)

    return keyword('func') + identifier + keyword('do') + Lazy(stmt_list) + keyword('end') ^ process


def func_call():
    def process(parsed):
        (_, name) = parsed
        return FunctionCall(name)

    return keyword('call') + identifier ^ process


def print_stmt():
    def process(parsed):
        (_, value) = parsed
        return PrintStatement(value)

    return keyword('print') + exp() ^ process


# Boolean expressions
def bexp():
    return precedence(bexp_term(),
                      bexp_precedence_levels,
                      process_logic)


def bexp_term():
    return bexp_not() | \
           bexp_relop() | \
           bexp_group()


def bexp_not():
    return keyword('not') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))


def bexp_relop():
    relops = ['<', '<=', '>', '>=', '==', '!=']
    return exp() + any_operator_in_list(relops) + exp() ^ process_relop


def exp():
    return sexp() | aexp()


def bexp_group():
    return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group


def sexp():
    return string ^ (lambda str: StringExp(str))


# Arithmetic expressions
def aexp():
    return precedence(aexp_term(),
                      aexp_precedence_levels,
                      process_binop)


def aexp_term():
    return aexp_value() | aexp_group()


def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group


def aexp_value():
    return (num ^ (lambda i: IntAexp(i))) | \
           (identifier ^ (lambda v: VarExp(v)))


# An IMP-specific combinator for binary operator expressions (aexp and bexp)
def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine

    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser


# Miscellaneous functions for binary and relational operators
def process_binop(op):
    return lambda l, r: BinopAexp(op, l, r)


def process_relop(parsed):
    ((left, op), right) = parsed
    return RelopBexp(op, left, right)


def process_logic(op):
    if op == 'and':
        return lambda l, r: AndBexp(l, r)
    elif op == 'or':
        return lambda l, r: OrBexp(l, r)
    else:
        raise RuntimeError('unknown logic operator: ' + op)


def process_group(parsed):
    ((_, p), _) = parsed
    return p


def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = functools.reduce(lambda l, r: l | r, op_parsers)
    return parser


# Operator keywords and precedence levels
aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

bexp_precedence_levels = [
    ['and'],
    ['or'],
]
