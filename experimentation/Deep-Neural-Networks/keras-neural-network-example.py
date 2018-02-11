import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation

def create_single_hidden_layer_model():
    # X has the shape (num rows, num cols)
    # where the training data are stored as row vectors
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype = np.float32)

    # y must have an output vector for each input vector
    y = np.array([[0], [0], [0], [1]],  dtype = np.float32)

    # Create Sequential model
    model = Sequential()

    # 1st layer - add input nayer of 32 nodes
    # with same input shape as training samples in X
    # (only need to specify shape for 1st later)
    # (Keras infers the shape of the other layers)
    model.add(Dense(32, input_dim = X.shape[1]))

    # Add softmax activation layer
    model.add(Activation('softmax'))

    # 2nd layer - add a fully connected output layer
    # with a dimension of 1
    model.add(Dense(1))

    # Add a sigmoid activation layer
    model.add(Activation('sigmoid'))

    # categorical_crossentropy can be used when where are only 2 classes
    # adam is a decent optimiser for speed
    # and we want to optimise for model accuracy
    model.compile(loss = "categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])

    # show the resulting model architecture
    model.summary()

    # fit() trains the model
    model.fit(X, y, epochs = 1000, verbose = 0)

    # Evaluate the model
    model.evaluate()


create_single_hidden_layer_model()
