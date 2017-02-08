from equality import *


class Statement(Equality):
    pass


class Aexp(Equality):
    pass


class Bexp(Equality):
    pass


class AssignStatement(Statement):
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp

    def __repr__(self):
        return 'AssignStatement(%s, %s)' % (self.name, self.exp)

    def eval(self, env):
        value = self.exp.eval(env)
        env[self.name] = value
        pass


class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'CompoundStatement(%s, %s)' % (self.first, self.second)

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)


class PrintStatement(Statement):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return 'PrintStatement({})'.format(self.exp)

    def eval(self, env):
        print(self.exp.eval(env))


class InputStatement(Statement):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'InputStatement(%s)' % (self.name)

    def eval(self, env):
        value = input()
        try:
            value = int(value)
        except:
            pass
        env[self.name] = value


class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def __repr__(self):
        return 'IfStatement(%s, %s, %s)' % (self.condition, self.true_stmt, self.false_stmt)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        if condition_value:
            self.true_stmt.eval(env)
        else:
            if self.false_stmt:
                self.false_stmt.eval(env)


class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WhileStatement(%s, %s)' % (self.condition, self.body)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        while condition_value:
            self.body.eval(env)
            condition_value = self.condition.eval(env)


class ForStatement(Statement):
    def __init__(self, name, start, end, body):
        self.start = start
        self.name = name
        self.end = end
        self.body = body

    def __repr__(self):
        return 'ForStatement(%s, %s, %s)' % (self.start, self.end, self.body)

    def eval(self, env):
        startVal = self.start.eval(env)
        endVal = self.end.eval(env)
        for i in range(startVal, endVal):
            env[self.name] = i
            self.body.eval(env)


class FunctionCall(Statement):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'FunctionCall(%s)' % self.name

    def eval(self, env):
        env[self.name]()


class FunctionStatement(Statement):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __repr__(self):
        return 'FunctionStatement(%s)' % self.name

    def eval(self, env):
        env[self.name] = lambda: self.body.eval(env)


class IntAexp(Aexp):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'IntAexp(%d)' % self.i

    def eval(self, env):
        return self.i


class StringExp(Equality):
    def __init__(self, str):
        self.str = str

    def __repr__(self):
        return 'StringExpression(%s)' % self.str

    def eval(self, env):
        return self.str.strip('"')


class VarExp(Aexp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'VarExp(%s)' % self.name

    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            raise RuntimeError("Variable not defined: {}".format(self.name))


class BinopAexp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'BinopAexp(%s, %s, %s)' % (self.op, self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '+':
            value = left_value + right_value
        elif self.op == '-':
            value = left_value - right_value
        elif self.op == '*':
            value = left_value * right_value
        elif self.op == '/':
            value = left_value / right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value


class RelopBexp(Bexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'RelopBexp(%s, %s, %s)' % (self.op, self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '<':
            value = left_value < right_value
        elif self.op == '<=':
            value = left_value <= right_value
        elif self.op == '>':
            value = left_value > right_value
        elif self.op == '>=':
            value = left_value >= right_value
        elif self.op == '==':
            value = left_value == right_value
        elif self.op == '!=':
            value = left_value != right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value


class AndBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'AndBexp(%s, %s)' % (self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value and right_value


class OrBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'OrBexp(%s, %s)' % (self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value or right_value


class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return 'NotBexp(%s)' % self.exp

    def eval(self, env):
        value = self.exp.eval(env)
        return not value
