import cv2
from keras.applications.resnet50 import ResNet50,preprocess_input,decode_predictions
import numpy as np

m=ResNet50(weights='imagenet')

img=cv2.imread('rabbit.jpg')
data=cv2.resize(img,(224,224)).reshape(1,224,224,3)
s_x=preprocess_input(data)#전처리기
#m.trainable=False
py=m.predict(s_x)
output=decode_predictions(py)[0]#후처리기
for i in range(5):
    cv2.putText(img,output[i][1]+':'+str(output[i][2]),(10,200+i*20),
                cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
cv2.imshow('img',img)
cv2.waitKey(0)