# Softmax quiz
import tensorflow as tf


def run():
    output = None
    logit_data = [2.0, 1.0, 0.1]
    logits = tf.placeholder(tf.float32)

    # DONE: Calculate the softmax of the logits
    softmax = tf.nn.softmax(logits)

    with tf.Session() as sess:
        # DONE: Feed in the logit data
        output = sess.run(softmax, feed_dict={logits: logit_data})

    return output
