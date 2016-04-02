import numpy as np

class Node:
    def __init__(self):
        pass

    def children(self):
        raise NotImplementedError("")

    def calculate(self, values_dict):
        raise NotImplementedError("")

    def id(self):
        raise NotImplementedError("")

class Add(Node):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

a = Node()
b = Node()
c = Add(a, b)
