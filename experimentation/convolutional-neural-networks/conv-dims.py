from keras.models import Sequential
from keras.layers import Conv2D

model = Sequential()
# conv_layer = Conv2D(
#     filters=16, 
#     kernel_size=2, 
#     strides=2, 
#     padding='valid', 
#     activation='relu',
#     input_shape=(200, 200, 1)
# )
conv_layer = Conv2D(
    filters=32, 
    kernel_size=3, 
    strides=2, 
    padding='same', 
    activation='relu',
    input_shape=(128, 128, 3)
)
# conv_layer = Conv2D(
#     filters=32, 
#     kernel_size=4, 
#     strides=2, 
#     padding='valid', 
#     activation='relu',
#     input_shape=(500, 500, 1)
# )
model.add(conv_layer)
model.summary()
