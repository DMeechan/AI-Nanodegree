from keras import backend as K
from keras.models import Model
from keras.layers import (BatchNormalization, Conv1D, Dense, Input,
                          TimeDistributed, Activation, Bidirectional, SimpleRNN, GRU, LSTM)


def simple_rnn_model(input_dim, output_dim=29):
    """ Build a recurrent network for speech
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add recurrent layer
    simp_rnn = GRU(output_dim, return_sequences=True,
                   implementation=2, name='rnn')(input_data)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(simp_rnn)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def rnn_model(input_dim, units, activation, output_dim=29):
    """ Build a recurrent network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add recurrent layer
    rnn_layer = GRU(units, activation=activation,
                    return_sequences=True, implementation=2, name='rnn')(input_data)

    # DONE: Add batch normalization
    bn_rnn = BatchNormalization(name='bn_rnn_1d')(rnn_layer)

    # DONE: Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bn_rnn)

    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def cnn_rnn_model(input_dim, filters, kernel_size, conv_stride,
                  conv_border_mode, units, output_dim=29):
    """ Build a recurrent + convolutional network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add convolutional layer
    conv_1d = Conv1D(filters, kernel_size,
                     strides=conv_stride,
                     padding=conv_border_mode,
                     activation='relu',
                     name='conv1d')(input_data)
    # Add batch normalization
    bn_cnn = BatchNormalization(name='bn_conv_1d')(conv_1d)
    # Add a recurrent layer
    simp_rnn = SimpleRNN(units, activation='relu',
                         return_sequences=True, implementation=2, name='rnn')(bn_cnn)

    # DONE: Add batch normalization
    bn_rnn = BatchNormalization(name='bn_rnn_1d')(simp_rnn)

    # DONE: Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bn_rnn)

    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: cnn_output_length(
        x, kernel_size, conv_border_mode, conv_stride)
    print(model.summary())
    return model


def cnn_output_length(input_length, filter_size, border_mode, stride,
                      dilation=1):
    """ Compute the length of the output sequence after 1D convolution along
        time. Note that this function is in line with the function used in
        Convolution1D class from Keras.
    Params:
        input_length (int): Length of the input sequence.
        filter_size (int): Width of the convolution kernel.
        border_mode (str): Only support `same` or `valid`.
        stride (int): Stride size used in 1D convolution.
        dilation (int)
    """
    if input_length is None:
        return None
    assert border_mode in {'same', 'valid'}
    dilated_filter_size = filter_size + (filter_size - 1) * (dilation - 1)
    if border_mode == 'same':
        output_length = input_length
    elif border_mode == 'valid':
        output_length = input_length - dilated_filter_size + 1
    return (output_length + stride - 1) // stride


def deep_rnn_model(input_dim, units, recur_layers, output_dim=29):
    """ Build a deep recurrent network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))

    # DONE: Add recurrent layers, each with batch normalization
    activation = 'relu'
    return_sequences = True
    implementation = 2

    layer = None
    # Set batch layer to the input data to begin with
    # So the loop below starts with the right input data
    batch_layer = input_data

    for i in range(0, recur_layers):
        layer = GRU(units, activation=activation,
                    return_sequences=return_sequences, name='gru_{}'.format(i + 1), implementation=implementation)(batch_layer)
        batch_layer = BatchNormalization(
            name='bn_rnn_{}d'.format(i + 1))(layer)

    # DONE: Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(batch_layer)

    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def bidirectional_rnn_model(input_dim, units, output_dim=29):
    """ Build a bidirectional recurrent network for speech
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))

    # DONE: Add bidirectional recurrent layer
    return_sequences = True
    activation = 'relu'
    merge_mode = 'concat'
    implementation = 2

    gru = GRU(units, activation=activation,
              return_sequences=return_sequences, implementation=implementation)
    bidir_rnn = Bidirectional(gru, merge_mode=merge_mode)(input_data)

    # DONE: Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bidir_rnn)

    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def final_model(input_dim=161, output_dim=29, filters=200, kernel_size=11, conv_stride=2, conv_border_mode='valid',  units=200):
    """ Build a deep network for speech
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))

    # DONE: Specify the layers in your network

    # GRU & Bidirectional RNN parameters
    activation = 'relu'
    return_sequences = True
    implementation = 2
    merge_mode = 'concat'

    # Set up GRU to be used later in the bidirectional layers
    gru1 = GRU(units, activation=activation,
              return_sequences=return_sequences, implementation=implementation, dropout=0.15)
    gru2 = GRU(units, activation=activation,
              return_sequences=return_sequences, implementation=implementation, dropout=0.25)

    # Add first layer: convolutional
    conv_1d = Conv1D(filters, kernel_size, strides=conv_stride,
                     padding=conv_border_mode, activation=activation, name='conv1d')(input_data)

    # Batch normalization
    bn_cnn = BatchNormalization(name='bn_conv_1d')(conv_1d)

    # Bidirectional recurrent layer
    bidir_rnn_1 = Bidirectional(gru1, merge_mode=merge_mode)(bn_cnn)

    # Batch normalization
    bn_bidir_1 = BatchNormalization(name='bn_bidir_1')(bidir_rnn_1)

    # Second bidirectional recurrent layer (deep)
    bidir_rnn_2 = Bidirectional(gru2, merge_mode=merge_mode)(bn_bidir_1)

    # Batch normalization
    bn_bidir_2 = BatchNormalization(name='bn_bidir_2')(bidir_rnn_2)

    time_dense = TimeDistributed(Dense(output_dim))(bn_bidir_2)

    # DONE: Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)

    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)

    # DONE: Specify model.output_length
    # model.output_length = lambda x: x
    # Use for CNN:
    model.output_length = lambda x: cnn_output_length(
        x, kernel_size, conv_border_mode, conv_stride)

    print(model.summary())
    return model
