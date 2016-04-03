import numpy as np
import tensorflow as tf


def build_expr_representation(a, expr, id2op):
  
  exprs = [build_expr_representation(a, subexp, id2op) for subexp in expr.childs]
  return


def tesor3dmul(x, y, W, n):
"""
  x - b x n
  y - b x n
  W - n x n x n
"""
  # b x (n * n)
  xW = tf.matmul(x, tf.reshape(W, [n, n * n]))
  tf.matmul(y, tf.reshape(xW, [b, n, n]))
  return xW


def build_ops_dict(n):
  res = {}
  # addidiotn
  v = tf.get_variable("addition_params", [n, n, n])
  res['add'] = tesor3dmul()
  return res


def train(exprs):
  with tf.Graph() as g:
    for expr in exprs:
      r = build_expr_representation(a, expt, id2op)
    with tf.Session('local') as sess:



def main():
  id2op = build_ops_dict()

  with tf.Session() as sess:


if __name__ == "__main__":
  main()