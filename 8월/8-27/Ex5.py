import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from jax.experimental.jax2tf.examples.mnist_lib import input_shape
from pandas.conftest import axis_1
from tensorflow.keras.datasets import cifar100
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (Input, Conv2D, MaxPooling2D, Dense, Dropout,
                                     BatchNormalization, Flatten, Activation, GlobalAveragePooling2D,
                                     Rescaling, RandomRotation, RandomZoom, RandomTranslation, RandomContrast)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

(tr_x, tr_y), (tt_x, tt_y) = cifar100.load_data()
print("훈련 데이터 형태:", tr_x.shape)
print("고유 레이블:", np.unique(tr_y))
print("-" * 30)
from keras import regularizers

def cv2d_bn_l(x, filters, kernel_size, weight_decay=.0, strides=1):
    x = Conv2D(filters, kernel_size, strides, 'same',
               kernel_regularizer=regularizers.l2(weight_decay))(x)
    x = BatchNormalization(scale=False, axis=3)(x)
    x = Activation('relu')(x)
    return x

def inception_module(x, fs_num_l, weight_decay=.0):
    br0_f, br1_f, br2_f, br3_f = fs_num_l

    br0 = cv2d_bn_l(x, br0_f, 1, weight_decay)

    br1 = cv2d_bn_l(x, br1_f[0], 1, weight_decay)
    br1 = cv2d_bn_l(br1, br1_f[1], 3, weight_decay)

    br2 = cv2d_bn_l(x, br2_f[0],1,weight_decay)
    br2 = cv2d_bn_l(br2, br2_f[1],5,weight_decay)

    br3 = MaxPooling2D(pool_size=3, strides=1, padding='same')(x)
    br3 = cv2d_bn_l(br3, br3_f,1,weight_decay)

    concatenate([br0, br1, br2, br3], axis = 3)
    return x

def googlenet(input_shape, classes, weight_decay=.0):
    input_l = Input(shape=input_shape)
    x = input_l
    x = cv2d_bn_l(x, 64, 1, weight_decay)
    x = cv2d_bn_l(x, 192, 3, weight_decay)
    x = MaxPooling2D(3, 2, 'same')(x)
    x = inception_module(x, (64, (96, 128), (16, 32), 32), weight_decay)
    x = inception_module(x, (128, (128, 192), (32, 96), 64), weight_decay)
    x = MaxPooling2D(2, 2, 'same')(x)
    x = inception_module(x, (192, (96, 208), (16, 48), 64), weight_decay)
    x = inception_module(x, (160, (112, 224), (24, 64), 64), weight_decay)
    x = inception_module(x, (128, (128, 256), (24, 64), 64), weight_decay)
    x = inception_module(x, (112, (144, 288), (32, 64), 64), weight_decay)
    x = inception_module(x, (256, (160, 320), (32, 128), 128), weight_decay)
    x = MaxPooling2D(2, 2, 'same')(x)
    x = inception_module(x, (256, (160, 320), (32, 128), 128), weight_decay)
    x = inception_module(x, (384, (192, 384), (48, 128), 128), weight_decay)
    x = Flatten()(x)
    output_l = Dense(classes, activation='softmax')(x)
    m = Model(input_l, output_l)
    return m

input_shape = (32, 32)
c_n = 3
batch_size = 64
weight_decay = 5e-4
l_r = 1e-2
ep=10
class_n = 100
from keras import regularizers
m = googlenet()