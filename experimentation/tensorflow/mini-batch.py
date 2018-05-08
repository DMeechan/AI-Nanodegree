# from tensorflow.examples.tutorials.mnist import input_data
# import tensorflow as tf

def mini_batch_sample_code():
    n_input = 784  # MNIST data input (img shape: 28*28)

    n_classes = 10  # MNIST total classes (0-9 digits)

    # Import MNIST data
    mnist = input_data.read_data_sets('/datasets/ud730/mnist', one_hot=True)

    # The features are already scaled and the data is shuffled
    train_features = mnist.train.images
    test_features = mnist.test.images

    train_labels = mnist.train.labels.astype(np.float32)
    test_labels = mnist.test.labels.astype(np.float32)

    # Weights & bias
    weights = tf.Variable(tf.random_normal([n_input, n_classes]))
    bias = tf.Variable(tf.random_normal([n_classes]))


# Doing da maths
# float32 = 
train_features = 55000*784*4
train_labels = 55000*10*4
weights = 784*10*4
bias = 10*4

def bytesToGb(num):
    return num / 1024 / 1024 / 1024


train_features = bytesToGb(train_features)
train_labels = bytesToGb(train_labels)
weights = bytesToGb(weights)
bias = bytesToGb(bias)

sum = train_features + train_labels + weights + bias

print("train_features:" + str(train_features))
print("train_labels:" + str(train_labels))
print("weights:" + str(weights))
print("bias:" + str(bias))
print("")
print("SUM:" + str(sum) + " GB")
