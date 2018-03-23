import tensorflow as tf

# Create TF object called tensor
hello_constant = tf.constant('Hello world')

with tf.Session() as session:
    # Run the tf.constant operation in the session
    output = session.run(hello_constant)
    print(output)