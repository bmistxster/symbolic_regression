import numpy as np
import tensorflow as tf
import tree

BATCH_SIZE = 10

def build_expr_representation(a, expr, id2op):
  if expr.id() == tree.OPERATOR_CONST || expr.id() == tree.OPERATOR_VAR:
    return id2op[exprs.id()]({})
  exprs = [build_expr_representation(a, subexp, id2op) for subexp in expr.childs]
  return id2op[exprs.id()](exprs)


def tesor3dmul(x, y, W, n):
"""
  x - b x n
  y - b x n
  W - n x n x n
"""
  # b x (n * n)
  #xW = tf.matmul(x, tf.reshape(W, [n, n * n]))
  #tf.matmul(y, tf.reshape(xW, [b, n, n]))
  return tf.matmul(x + y, W)


def build_ops_dict(n):
  def var_op(exprs):
    return tf.get_variable("var_params", [n])

  def const_op(exprs):
    return tf.constant(exprs.calculate({}))

  def sin_op(exprs):
    W = tf.get_variable("sin_params", [n, n])
    return tf.nn.relu(tf.matmul(W, exprs[0]))

  def add_op(exprs):
    W = tf.get_variable("addition_params", [n, n])
    return tesor3dmul(exprs[0], exprs[1], W, n)
    
  res = {tree.OPERATOR_ADD: add_op,
         tree.OPERATOR_SIN: sin_op,
         tree.OPERATOR_CONST: const_op,
         tree.OPERATOR_VAR: var_op}
  return res


def train(exprs, id2op):
  with tf.Graph() as g:
    pairs = [(build_expr_representation(a, expr, id2op), expr) for expr in exprs]
    with tf.Session('local') as sess:
      for p in pairs:
        sess.run(p[0])


def main():
  id2op = build_ops_dict()

  with tf.Session() as sess:


if __name__ == "__main__":
  main()