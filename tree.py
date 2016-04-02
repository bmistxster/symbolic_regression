import numpy as np

class Node:
    def __init__(self):
        pass

class Add(Node):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

a = Node()
b = Node()
c = Add(a, b)
