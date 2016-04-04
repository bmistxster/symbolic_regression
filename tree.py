import hashlib
import math
import random

OPERATOR_ADD = "add"
OPERATOR_MUL = "mul"
OPERATOR_CONST = "const"
OPERATOR_SIN = "sin"
OPERATOR_SQRT = "sqrt"
OPERATOR_VAR = "var"

class Node(object):
    def __init__(self):
        pass

    def children(self):
        raise NotImplementedError("")

    def calculate(self, values_dict):
        raise NotImplementedError("")

    def id(self):
        raise NotImplementedError("")

    def __str__(self):
        raise NotImplementedError("")

    def __eq__(self, other):
        return type(self) == type(other) and self.eq(other)

    def __hash__(self):
        return hash(self.hsh)

    def eq(self, other):
        raise NotImplementedError("")

class BinaryOperator(Node):
    def __init__(self, lhs, rhs):
        self.depth = 1 + max(lhs.depth, rhs.depth)
        if lhs.hsh < rhs.hsh:
            self.lhs = lhs
            self.rhs = rhs
        else:
            self.lhs = rhs
            self.rhs = lhs
        md5 = hashlib.md5()
        md5.update(self.id())
        md5.update("(")
        md5.update(self.lhs.hsh)
        md5.update(",")
        md5.update(self.rhs.hsh)
        md5.update(")")
        self.hsh = md5.hexdigest()

    def children(self):
        return [self.lhs, self.rhs]

    def eq(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs

class Add(BinaryOperator):
    def calculate(self, values_dict):
        return self.lhs.calculate(values_dict) + self.rhs.calculate(values_dict)

    def id(self):
        return OPERATOR_ADD

    def __str__(self):
        return "({0} + {1})".format(self.lhs, self.rhs)

class Mul(BinaryOperator):
    def calculate(self, values_dict):
        return self.lhs.calculate(values_dict) * self.rhs.calculate(values_dict)

    def id(self):
        return OPERATOR_MUL

    def __str__(self):
        return "{0} * {1}".format(self.lhs, self.rhs)

class UnaryOperator(Node):
    def __init__(self, child):
        self.depth = 1 + child.depth
        self.child = child
        md5 = hashlib.md5()
        md5.update(self.id())
        md5.update("(")
        md5.update(self.child.hsh)
        md5.update(")")
        self.hsh = md5.hexdigest()

    def children(self):
        return [self.child]

    def eq(self, other):
        return self.child == other.child

class Sin(UnaryOperator):
    def calculate(self, values_dict):
        return math.sin(self.child.calculate(values_dict))

    def id(self):
        return OPERATOR_SIN

    def __str__(self):
        return "sin({0})".format(self.child)

class Sqrt(UnaryOperator):
    def calculate(self, values_dict):
        return math.sqrt(self.child.calculate(values_dict))

    def id(self):
        return OPERATOR_SQRT

    def __str__(self):
        return "sqrt({0})".format(self.child)

class Const(Node):
    def __init__(self, value):
        self.depth = 1
        self.value = value
        self.hsh = hashlib.md5(str(value)).hexdigest()

    def children(self):
        return []

    def calculate(self, values_dict):
        return self.value

    def id(self):
        return OPERATOR_CONST

    def __str__(self):
        return str(self.value)

    def eq(self, other):
        return self.value == other.value

class Var(Node):
    def __init__(self, name):
        self.depth = 1
        self.name = name
        self.hsh = hashlib.md5(str(name)).hexdigest()

    def children(self):
        return []

    def calculate(self, values_dict):
        return values_dict[self.name]

    def id(self):
        return OPERATOR_VAR

    def __str__(self):
        return self.name

    def eq(self, other):
        return self.name == other.name

base_exprs = [Const(1), Const(2), Const(-1), Var("x")]
binary_ops = [Add, Mul]
unary_ops = [Sin, Sqrt]
total_exprs = len(base_exprs)
exprs_count = [total_exprs]
partial_sums = [total_exprs]
for level in xrange(10):
    last_exprs_count = exprs_count[-1]
    new_count = len(unary_ops) * last_exprs_count
    new_count += len(binary_ops) * (
        last_exprs_count * (last_exprs_count + 1) / 2 +
        last_exprs_count * (total_exprs - last_exprs_count))
    total_exprs += new_count
    exprs_count.append(new_count)
    partial_sums.append(total_exprs)

def generate_expressions(level):
    exprs = base_exprs
    for expr in exprs:
        yield expr
    for it in xrange(level):
        new_exprs = set()
        for expr in exprs:
            new_exprs.add(expr)
        for op in unary_ops:
            for expr in exprs:
                nexpr = op(expr)
                if nexpr not in new_exprs:
                    yield nexpr
                    new_exprs.add(nexpr)
        for op in binary_ops:
            for ind1 in xrange(len(exprs)):
                for ind2 in xrange(ind1, len(exprs)):
                    nexpr = op(exprs[ind1], exprs[ind2])
                    if nexpr not in new_exprs:
                        yield nexpr
                        new_exprs.add(nexpr)
        exprs = list(new_exprs)

def generate_random_expr(level):
    if level == 0:
        return random.choice(base_exprs)
    last_exprs_count = exprs_count[level - 1]
    total_exprs = partial_sums[level - 1]
    unary_op_count = len(unary_ops) * last_exprs_count
    binary_op_count = len(binary_ops) * (
        last_exprs_count * (last_exprs_count + 1) / 2 +
        last_exprs_count * (total_exprs - last_exprs_count))
    if random.randint(1, unary_op_count + binary_op_count) <= unary_op_count:
        return random.choice(unary_ops)(generate_random_expr(level - 1))
    else:
        op = random.choice(binary_ops)
        expr_a = generate_random_expr(level - 1)
        if (random.randint(1, last_exprs_count * (last_exprs_count + 1) / 2 +
                              last_exprs_count * (total_exprs - last_exprs_count)) <=
                last_exprs_count * (last_exprs_count + 1) / 2):
            if (random.randint(1, last_exprs_count * (last_exprs_count + 1) / 2) <=
                    last_exprs_count):
                return op(expr_a, expr_a)
            else:
                while True:
                    expr_b = generate_random_expr(level - 1)
                    if not (expr_a == expr_b):
                        break
                return op(expr_a, expr_b)
        else:
            val = random.randint(1, partial_sums[level - 2])
            for other_level in xrange(level - 1):
                if val <= exprs_count[other_level]:
                    return op(expr_a, generate_random_expr(other_level))
                val -= exprs_count[other_level]
            raise Exception("Should have generated something")

#import collections
#ccc = collections.defaultdict(int)
#ttt = 10000000
#for i in xrange(ttt):
#    ccc[generate_random_expr(2)] += 1

#avg = ttt / len(ccc)
#for a, b in ccc.iteritems():
#    print(b, str(a))

#print(len(ccc), avg)

print(generate_random_expr(4))
