import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


import tensorflow as tf
import math
from keras.models import Sequential
from keras.layers import Dense, Input
from keras.utils import np_utils
from keras.layers import Flatten, Dropout
from keras.utils.vis_utils import plot_model

#================================================================================================
# model creation
#================================================================================================

def create_model(x,model_name):
    learning_rate = 0.05
    sgd = tf.keras.optimizers.SGD(learning_rate=learning_rate)
    dim = x.shape[1]
    # op_dim = y.shape[1]
    model = Sequential()
    model.add(Input(shape=(dim)))
    model.add(Dense(math.ceil((2/3)*dim),input_dim=dim,activation='sigmoid'))
    model.add(Dense(9,activation='softmax'))
    # print(model.summary())
    plot_model(model, show_shapes=True, to_file= model_name+'_Fed-ReMECS_model.png')
    model.compile(optimizer=sgd,
                loss='categorical_crossentropy')
    return model
