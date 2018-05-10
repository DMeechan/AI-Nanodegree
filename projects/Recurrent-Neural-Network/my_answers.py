import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Activation
import keras

import string

# DONE: fill out the function below that transforms the input series
# and window-size into a set of input/output pairs for use with our RNN model


def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []
    length = len(series)
    
    for index in range(0, length - window_size):
        input_items = series[index: index + window_size]
        X.append(input_items)

        output_item = series[index + window_size]
        y.append(output_item)

    # reshape each
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y), 1)

    return X, y

# DONE: build an RNN to perform regression on our time series input/output data


def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(units=5, activation='tanh', input_shape=(window_size, 1)))
    model.add(Dense(1))
    return model


# DONE: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    # Grab special characters & numbers and put them all in a string together
    punctuation_to_keep = ['!', ',', '.', ':', ';', '?']

    punctuation = ['à', 'â', 'è', 'é']
    punctuation += ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    punctuation += ['\n', '\r', '\t', '\f']
    punctuation += ['\u000b', '\ufeff']
    punctuation += ['"', '#', '$', '%', '&', "'", '(', ')', '*', '+', '-', '/']
    punctuation += ['@', '[', ']', '<', '>', '~', '^', '_', '{', '}', '|', '=', '`', '\\']
    punctuation = ''.join(punctuation)

    # Remove all the punctuation found
    translation_table = str.maketrans(' ', ' ', punctuation)
    text = text.translate(translation_table)

    return text

# DONE: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model


def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []
    length = len(text)

    for index in range(0, length - window_size, step_size):
        input_items = text[index : index + window_size]
        inputs.append(input_items)
        output_item = text[index + window_size]
        outputs.append(output_item)

    return inputs, outputs

# DONE build the required RNN model:
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss


def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    input_shape = (window_size, num_chars)

    layer_1 = LSTM(units=200, activation='tanh', input_shape=input_shape)
    layer_2 = Dense(units=num_chars)
    layer_3 = Activation('softmax')

    model.add(layer_1)
    model.add(layer_2)
    model.add(layer_3)

    return model
