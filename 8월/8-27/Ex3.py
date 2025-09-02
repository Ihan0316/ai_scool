from keras.datasets import cifar100
import numpy as np
(tr_x,tr_y),(tt_x,tt_y) = cifar100.load_data()
print(tr_x.shape)
print(np.unique(tr_y))
#CNN
from keras.models import Sequential
from keras.layers import Input,Conv2D,MaxPooling2D,Dense,Dropout,BatchNormalization,Flatten
from keras.optimizers import Adam,Adagrad,Nadam,RMSprop
from keras.losses import categorical_crossentropy,sparse_categorical_crossentropy
from keras.callbacks import ModelCheckpoint,EarlyStopping,ReduceLROnPlateau

"""
#100종 분류기 완성하기

ReduceLROnPlateau(#성능 향상이 일어나지 않으면 학습률 조정해라
    monitor: str = "val_loss",#*
    factor: float = 0.1,#조정값(학습률 어떤비율로 조정할꺼야)*
    patience: int = 10,#조정 결정 기준(반복적으로 개선되지 않을때의 기준)*
    verbose: int = 0,
    mode: str = "auto",#*
    min_delta: float = 0.0001,#학습률 조정시 변화 한계지점 결정
    cooldown: int = 0,
    min_lr: float = 0,#학습률 조정시 학습률의 최소점 결정*
)
"""
from keras import regularizers
from keras import Model
from keras.layers import Activation,MaxPool2D,concatenate

def cv2d_bn_l(x,filters,kernel_size,weight_decay=.0,strides=1):
    x=Conv2D(filters,kernel_size,strides,'same',
             kernel_regularizer=regularizers.l2(weight_decay))(x)
    x=BatchNormalization(scale=False,axis=3)(x)
    x=Activation('relu')(x)
    return x

def inception_module(x,fs_num_l,weight_decay=.0):
    br0_f, br1_f, br2_f, br3_f=fs_num_l
    
    br0=cv2d_bn_l(x,br0_f,1,weight_decay)
    
    br1=cv2d_bn_l(x,br1_f[0],1,weight_decay)
    br1=cv2d_bn_l(br1,br1_f[1],3,weight_decay)
    
    br2=cv2d_bn_l(x,br2_f[0],1,weight_decay)
    br2=cv2d_bn_l(br2,br2_f[1],5,weight_decay)
    
    br3=MaxPool2D(pool_size=3,strides=1,padding='same')(x)
    br3=cv2d_bn_l(br3,br3_f,1,weight_decay)
    
    x=concatenate([br0,br1,br2,br3],axis=3)
    return x

def googlenet(input_shape,classes,weight_decay=.0):
    input_l=Input(shape=input_shape)
    x=input_l
    x=cv2d_bn_l(x,64,1,weight_decay)
    x=cv2d_bn_l(x,192,3,weight_decay)
    x=MaxPool2D(3,2,'same')(x)
    x=inception_module(x,(64,(96,128),(16,32),32),weight_decay)
    x=inception_module(x,(128,(128,192),(32,96),64),weight_decay)
    x=MaxPool2D(2,2,'same')(x)
    x=inception_module(x,(192,(96,208),(16,48),64),weight_decay)
    x=inception_module(x,(160,(112,224),(24,64),64),weight_decay)
    x=inception_module(x,(128,(128,256),(24,64),64),weight_decay)
    x=inception_module(x,(112,(144,288),(32,64),64),weight_decay)
    x=inception_module(x,(256,(160,320),(32,128),128),weight_decay)
    x=MaxPool2D(2,2,'same')(x)
    x=inception_module(x,(256,(160,320),(32,128),128),weight_decay)
    x=inception_module(x,(384,(192,384),(48,128),128),weight_decay)
    x=Flatten()(x)
    output_l=Dense(classes,activation='softmax')(x)
    m=Model(input_l,output_l)
    return m
    
input_shape=(32,32)
c_n=3
batch_size=64
weight_decay=5e-4
l_r=1e-2
ep=10
class_n=100
from keras.losses import sparse_categorical_crossentropy
ggn_m=googlenet(input_shape+(3,),class_n,weight_decay)
from keras.optimizers import SGD
op=SGD(learning_rate=l_r,momentum=0.9)
ggn_m.compile(optimizer=op,loss=sparse_categorical_crossentropy,metrics=['acc'])
reduce_lr=ReduceLROnPlateau(factor=0.5,patience=4,min_lr=1e-7,verbose=1)
es=EarlyStopping(patience=10,restore_best_weights=True)
ck=ModelCheckpoint('b_m.keras',save_best_only=True)
hy=ggn_m.fit(tr_x,tr_y,batch_size=batch_size,epochs=ep,validation_split=0.2,
          callbacks=[reduce_lr,es,ck])

