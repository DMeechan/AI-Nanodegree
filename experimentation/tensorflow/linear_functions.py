# Linear functions using variables in TensorFlow

import tensorflow as tf

x = tf.Variable(5)

num_features = 120
num_labels = 5

# tf.truncated_normal() returns a tensor with random values form a normal disttribution
# so we don't need to bother randomising the bias
weights = tf.Variable(tf.truncated_normal((num_features, num_labels)))

# Tensowflow variable states are stored in the session
# So we need to manually initialize the state of the tensors
# This can be done globally to inialize the state of all Variable tensors
init = tf.global_variables_initializer()

with tf.Session() as session:
    session.run(init)
