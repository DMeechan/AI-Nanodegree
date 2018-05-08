import tensorflow as tf


x = tf.placeholder(tf.string)
y = tf.placeholder(tf.string)
z = tf.placeholder(tf.float32)

with tf.Session() as session:
    # feed_dict sets the placeholder tensor
    output = session.run((x, y, z) , feed_dict={x: 'Hello, World!!', y: 'lol', z: 42.314159265})
    print(output)