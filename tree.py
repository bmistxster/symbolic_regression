import math

OPERATOR_ADD = "add"
OPERATOR_MUL = "mul"
OPERATOR_CONST = "const"
OPERATOR_SIN = "sin"
OPERATOR_SQRT = "sqrt"
OPERATOR_VAR = "var"

class Node:
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

class BinaryOperator(Node):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def children(self):
        return [self.lhs, self.rhs]

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
        return OPERATOR_ADD

    def __str__(self):
        return "{0} * {1}".format(self.lhs, self.rhs)

class UnaryOperator(Node):
    def __init__(self, child):
        self.child = child

    def children(self):
        return [self.child]

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
        self.value = value

    def children(self):
        return []

    def calculate(self, values_dict):
        return self.value

    def id(self):
        return OPERATOR_CONST

    def __str__(self):
        return str(self.value)

class Var(Node):
    def __init__(self, name):
        self.name = name

    def children(self):
        return []

    def calculate(self, values_dict):
        return values_dict[self.name]

    def id(self):
        return OPERATOR_VAR

    def __str__(self):
        return self.name

a = Var("x")
b = Var("y")
c = Add(a, b)
print(c)
print(c.calculate({"x": 1, "y": 2}))
