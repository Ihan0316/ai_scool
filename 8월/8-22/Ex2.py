import cv2
import numpy as np
import matplotlib.pyplot as plt
from timm.data import get_img_extensions

img = cv2.imread('../../data/data1.jpg')

hb = cv2.calcHist([img],[0],None,[256],[0,256])
hg = cv2.calcHist([img],[1],None,[256],[0,256])
hr = cv2.calcHist([img],[2],None,[256],[0,256])

bimg = img[:,:,0]
gimg = img[:,:,1]
rimg = img[:,:,2]
print(bimg.shape, gimg.shape, bimg.shape)
print(img.shape)
b_rg = bimg.reshape(-1)
plt.hist(b_rg)
plt.show()
plt.plot(hb, 'b-')
plt.show()