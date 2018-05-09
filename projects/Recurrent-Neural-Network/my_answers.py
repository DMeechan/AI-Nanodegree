import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras

import string

# DONE: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []

    length = len(series)
    for starting_index in range(0, length):
        items = []
        for increment in range(0, window_size):
            index = starting_index + increment
            if index < length:
                item = series[index]
                items.append(item)
            else:
                break

        if len(items) == window_size:
            X.append(items)
            output_index = starting_index + window_size
            if output_index < length:
                y.append([series[output_index]])

    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y

# DONE: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(units=5, activation='tanh', input_shape=(window_size, 1)))
    model.add(Dense(1))
    return model


### DONE: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    # punctuation = ['!', ',', '.', ':', ';', '?']
    translation_table = str.maketrans('', '', string.punctuation)
    text = text.translate(translation_table)

    return text

### DONE: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []

    length = len(text)
    for starting_index in range(0, length, step_size):
        items = []
        for increment in range(0, window_size):
            index = starting_index + increment
            if index < length:
                item = text[index]
                items.append(item)
            else:
                break

        if len(items) == window_size:
            inputs.append(items)
            output_index = starting_index + window_size
            if output_index < length:
                outputs.append([text[output_index]])

    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    pass
