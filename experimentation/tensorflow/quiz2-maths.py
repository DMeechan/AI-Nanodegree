import tensorflow as tf

# The fun way to do it:
x = 10
y = 2
z = x/y - 1

z = tf.constant(z)

# And the way they were expecting it...

x = tf.constant(x)
y = tf.constant(y)
z = tf.divide(tf.cast(x, tf.float32), tf.cast(y, tf.float32))
z = tf.subtract(z, 1.0)

# And then let's run it to finish this off

with tf.Session() as session:
    output = session.run(z)
    print(output)
