# Multi-layer feedforward neural network to solve XOR problem

import numpy as np
from keras.utils import np_utils
import tensorflow as tf
# Using TensorFlow 1.0.0; use tf.python_io in later versions
# tf.python.control_flow_ops = tf
tf.python_io.control_flow_ops = tf

# Set random seed
np.random.seed(42)

# Our data
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]).astype('float32')
y = np.array([[0], [1], [1], [0]]).astype('float32')

# Initial Setup for Keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation

# Building the model
xor_model = Sequential()

# Add required layers
xor_model.add(Dense(8, input_dim=X.shape[1]))

xor_model.add(Activation('tanh'))

xor_model.add(Dense(1))

xor_model.add(Activation('sigmoid'))

# Specify loss as "binary_crossentropy", optimizer as "adam",
# and add the accuracy metric
xor_model.compile(loss="binary_crossentropy",
                  optimizer="adam", metrics=["accuracy"])

# Uncomment this line to print the model architecture
xor_model.summary()

# Fitting the model
history = xor_model.fit(X, y, epochs=174, verbose=0)
# history = xor_model.fit(X, y, nb_epoch=50, verbose=0)

# Scoring the model
score = xor_model.evaluate(X, y)
print("\nAccuracy: ", score[-1])

# Checking the predictions
print("\nPredictions:")
print(xor_model.predict_proba(X))
