import tensorflow as tf

# Create TF object called tensor
hello_constant = tf.constant('Hello world')
adding = tf.add('13', tf.cast(37, tf.string))
# subtracting = tf.subtract(13, tf.cast('3', tf.int32))

with tf.Session() as session:
    # Run the tf.constant operation in the session
    output = session.run(adding)
    print(output)
