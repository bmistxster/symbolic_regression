import numpy as np
import tensorflow as tf


def build_expr_representation(a, expr):
  exprs = [build_expr_representation(a, subexp) for subexp in expr.childs]
  return op

def main():
  with tf.Session() as sess:


if __name__ == "__main__":
  main()