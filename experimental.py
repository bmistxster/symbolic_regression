import numpy as np
import tensorflow as tf
import tree

BATCH_SIZE = 10
EXPR_VEC_SIZE = 6

def build_expr_representation(expr, id2op):
  if expr.id() == tree.OPERATOR_CONST or expr.id() == tree.OPERATOR_VAR:
    return id2op[expr.id()]([expr])
  exprs = [build_expr_representation(subexp, id2op) for subexp in expr.children()]
  return id2op[expr.id()](exprs)


def tesor3dmul(x, y, W, n):
  # b x (n * n)
  #xW = tf.matmul(x, tf.reshape(W, [n, n * n]))
  #tf.matmul(y, tf.reshape(xW, [b, n, n]))
  return tf.matmul(W, x + y)


def build_ops_dict():
  n = EXPR_VEC_SIZE
  def var_op(exprs):
    return tf.get_variable("var_params", [n, 1])

  def const_op(exprs):
    return tf.get_variable("const_params", [n, 1])
    #return tf.constant(exprs[0].calculate({}), dtype=tf.float32)

  def sin_op(exprs):
    W = tf.get_variable("sin_params", [n, n])
    return tf.nn.relu(tf.matmul(W, exprs[0]))

  def add_op(exprs):
    W = tf.get_variable("addition_params", [n, n])
    return tf.nn.relu(tesor3dmul(exprs[0], exprs[1], W, n))

  def mlt_op(exprs):
    W = tf.get_variable("multiply_params", [n, n])
    return tf.nn.relu(tesor3dmul(exprs[0], exprs[1], W, n))

  def sqrt_op(exprs):
    W = tf.get_variable("sqrt_params", [n, n])
    return tf.nn.relu(tf.matmul(W, exprs[0]))

    
  res = {tree.OPERATOR_ADD: add_op,
         tree.OPERATOR_SIN: sin_op,
         tree.OPERATOR_CONST: const_op,
         tree.OPERATOR_VAR: var_op,
         tree.OPERATOR_SQRT: sqrt_op,
         tree.OPERATOR_MUL: mlt_op}
  return res


def create_variables():
  with tf.variable_scope("tnn"):
    tf.get_variable("var_params", initializer=tf.random_normal([EXPR_VEC_SIZE, 1]))
    tf.get_variable("const_params", initializer=tf.random_normal([EXPR_VEC_SIZE, 1]))
    tf.get_variable("sin_params", initializer=tf.random_normal([EXPR_VEC_SIZE, EXPR_VEC_SIZE]))
    tf.get_variable("sqrt_params", initializer=tf.random_normal([EXPR_VEC_SIZE, EXPR_VEC_SIZE]))
    tf.get_variable("addition_params", initializer=tf.random_normal([EXPR_VEC_SIZE, EXPR_VEC_SIZE]))
    tf.get_variable("multiply_params", initializer=tf.random_normal([EXPR_VEC_SIZE, EXPR_VEC_SIZE]))

    tf.get_variable("W0", initializer=tf.random_normal([EXPR_VEC_SIZE + 1, 5]))
    tf.get_variable("W1", initializer=tf.random_normal([5, 1]))


def prediction(expr_vec, x):
  W0 = tf.get_variable("W0")
  W1 = tf.get_variable("W1")
  expr_vec = tf.transpose(expr_vec, perm=[1, 0])
  ev_batch = tf.concat(0, [expr_vec] * BATCH_SIZE)
  x0 = tf.concat(1, [ev_batch, x])
  h = tf.nn.relu(tf.matmul(x0, W0))
  return tf.matmul(h, W1)


def get_xy(expr):
  x = np.random.randn(BATCH_SIZE, 1)
  y = np.array([expr.calculate({'x': x0}) for x0 in x])
  y = np.reshape(y, [BATCH_SIZE, 1])
  return x, y


def loss(p, y):
  return tf.reduce_mean(tf.square(p - y))


def train(exprs, id2op):
  with tf.Graph().as_default():
    create_variables()
    x = tf.placeholder(tf.float32, shape=[BATCH_SIZE, 1])
    y = tf.placeholder(tf.float32, shape=[BATCH_SIZE, 1])
    with tf.variable_scope("tnn", reuse=True):
      tree_data = []
      for i, expr in enumerate(exprs):
        print i
        if i > 100:
          break
        expr_vec = build_expr_representation(expr, id2op)
        p = prediction(expr_vec, x)
        l = loss(p, y)
        opt = tf.train.MomentumOptimizer(learning_rate=0.01, momentum=0.9)
        tr_op = opt.minimize(l)
        tree_data.append([expr, expr_vec, p, l, tr_op])
    print 'Graph is built. Starting training....'
    with tf.Session() as sess:
      sess.run(tf.initialize_all_variables())
      for expr, _, _, l, tr_op in tree_data:
        xval, yval = get_xy(expr)
        print str(expr)
        sess.run(tr_op, feed_dict={x: xval, y: yval})
        print sess.run(l, feed_dict={x: xval, y: yval})


def main():
  id2op = build_ops_dict()
  exprs = tree.generate_expressions(2)
  train(exprs, id2op)


if __name__ == "__main__":
  main()