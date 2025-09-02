# 개 고양이 데이터를 로드하여 기학습된 모델을 이용하여 결과를 도출 및 시각화 하시오
#1. 기학습된 모델을 그대로 사용하시오
import os
import shutil
import pathlib
import cv2
from keras.utils import image_dataset_from_directory
from keras.applications.densenet import DenseNet121,preprocess_input,decode_predictions

d_path = pathlib.Path(r'C:/Users/user/Desktop/dl/dogs-vs-cats/train')
def f(n, st_idx, end_idx):
    for m in ('dog', 'cat'):            
        dir = d_path / n / m            
        try:
            os.makedirs(dir)            
        except:
            print("있습니다")           
        f_ns = [f'{m}.{i}.jpg' for i in range(st_idx, end_idx)]
        for f_n in f_ns:
            shutil.copyfile(src=d_path / f_n, dst=dir / f_n)
"""            
f("tr_data", 0, 50) 
l_path = pathlib.Path(r'C:/Users/user/Desktop/dl/dogs-vs-cats/train/tr_data') 
ds=image_dataset_from_directory(l_path,None,image_size=(224,224),
                                batch_size=32,shuffle=False)
ds=ds.map(preprocess_input)
file_paths=getattr(ds,'file_paths',None)
m=DenseNet121(weights='imagenet')
py=m.predict(ds)
for i,path in enumerate(file_paths):
    top5=decode_predictions(py[i:i+1])[0]
    
    img=cv2.imread(path)
    
    h,w=img.shape[:2]
    if w>900:
        scale=900.0/w
        img=cv2.resize(img,(900,int(h*scale)),interpolation=cv2.INTER_AREA)
    x,y=10,30
    line_h=26
    for k,(_,name,p) in enumerate(top5):
        text=f'{k}.{name}: {p:.2%}'
        cv2.putText(img,text,(x,y+(k*line_h)),
                    cv2.FONT_HERSHEY_SIMPLEX,0.65,
                    (255,255,255),2,cv2.LINE_AA)
    cv2.imshow('img',img)
    key=cv2.waitKey(1)
    if key==27:
        break
cv2.destroyAllWindows()
"""
#2. 기학습된 모델의 특징 검출기를 이용하여 분류층을 증가시켜 모델을 학습하시오(동결)
l_path = pathlib.Path(r'C:/Users/user/Desktop/dl/dogs-vs-cats/train/tr_data') 
tr_ds=image_dataset_from_directory(l_path,labels="inferred",label_mode='int',seed=14,validation_split=0.2,subset='training',image_size=(224,224),batch_size=32)
val_ds=image_dataset_from_directory(l_path,labels="inferred",label_mode='int',seed=14,validation_split=0.2,subset='validation',image_size=(224,224),batch_size=32)
#print(tr_ds.class_names)
class_n=len(tr_ds.class_names)
print(class_n)
tr_ds=tr_ds.map(lambda x,y: (preprocess_input(x),y))
val_ds=val_ds.map(lambda x,y: (preprocess_input(x),y))


#백본을 사용했다.
base=DenseNet121(weights='imagenet',include_top=False,input_shape=(224,224,3))#특징 검출기
base.trainable=False

from keras.models import Model,Sequential
from keras.layers import Input,Dense,Dropout,BatchNormalization,Flatten,GlobalAveragePooling2D
from keras.optimizers import Adam
from keras.losses import BinaryCrossentropy,binary_crossentropy,SparseCategoricalCrossentropy,sparse_categorical_crossentropy
from keras.callbacks import ModelCheckpoint,EarlyStopping
input_l=Input(shape=(224,224,3))
x=base(input_l,training=False)
x=GlobalAveragePooling2D()(x)
x=Dense(512,activation='relu')(x)
x=Dropout(0.4)(x)
x=Dense(256,activation='relu')(x)
x=Dropout(0.3)(x)

output_l=Dense(class_n,activation='softmax')(x)
m=Model(input_l,output_l)
m.compile(optimizer=Adam(learning_rate=0.0001),loss=sparse_categorical_crossentropy,metrics=['acc'])

call_bk=[ModelCheckpoint('b_m.keras',monitor='val_acc',mode='max',save_best_only=True,verbose=1),
         EarlyStopping(monitor='val_loss',patience=3,restore_best_weights=True)]
m.fit(tr_ds,validation_data=val_ds,epochs=8,callbacks=call_bk)
