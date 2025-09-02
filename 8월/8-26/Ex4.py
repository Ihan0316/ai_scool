import numpy as np
from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input
from keras.optimizers import Adam
from keras.losses import categorical_crossentropy


(tr_x, tr_y), (tt_x, tt_y) = mnist.load_data()

# print(tr_x.shape)

s_tr_x = tr_x.reshape(-1, 28*28)/255.0
s_tt_x = tt_x.reshape(-1, 28*28)/255.0
s_tr_y = to_categorical(tr_y)
s_tt_y = to_categorical(tt_y)

m = Sequential()
m.add(Input(shape=(784,)))
m.add(Dense(1024, activation='relu'))
m.add(Dense(512, activation='relu'))
m.add(Dense(10, activation='softmax'))
m.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

hy = m.fit(s_tr_x, s_tr_y, validation_data = (s_tt_x, s_tt_y), batch_size = 128, epochs = 30, verbose = 2)

m.save('m.keras')