import cv2
import numpy as np

data=np.array([[0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,1,1,1,1,1,0,0,0],
               [0,0,1,0,0,0,1,0,0,0],
               [0,0,1,0,0,0,1,0,0,0],
               [0,0,1,0,0,0,1,0,0,0],
               [0,0,1,1,1,1,1,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0],],dtype=np.float32
)
ux=np.array([[-1,0,1]])
uy=np.array([[-1,0,1]]).T
k=cv2.getGaussianKernel(3,1)
g=np.outer(k,k.T)
dx=cv2.filter2D(data,cv2.CV_32F,ux)
dy=cv2.filter2D(data,cv2.CV_32F,uy)

dyy=dy*dy
dxx=dx*dx
dyx=dy*dx

gdyy=cv2.filter2D(dyy,cv2.CV_32F,g)
gdxx=cv2.filter2D(dxx,cv2.CV_32F,g)
gdyx=cv2.filter2D(dyx,cv2.CV_32F,g)

C=(gdyy*gdxx-gdyx*gdyx)-0.04*(gdyy+gdxx)*(gdyy+gdxx)
#비최대 억제

for i in range(1,C.shape[0]-1):
    for j in range(1,C.shape[1]-1):
        if C[j,i]>0.1 and sum(sum(C[j,i]>C[j-1:j+2,i-1:i+2]))==8:
            data[j,i]=9
            

np.set_printoptions(precision=2)
import matplotlib.pyplot as plt

print(dy)
plt.subplot(3,3,1)
plt.title('dy')
plt.imshow(dy)
plt.axis('off')

print(dx)
plt.subplot(3,3,2)
plt.title('dx')
plt.imshow(dx)
plt.axis('off')

print(dyy)
plt.subplot(3,3,3)
plt.title('dyy')
plt.imshow(dyy)
plt.axis('off')

print(dxx)
plt.subplot(3,3,4)
plt.title('dxx')
plt.imshow(dxx)
plt.axis('off')

print(dyx)
plt.subplot(3,3,5)
plt.title('dyx')
plt.imshow(dyx)
plt.axis('off')

print(gdyy)
plt.subplot(3,3,6)
plt.title('gdyy')
plt.imshow(gdyy)
plt.axis('off')

print(gdxx)
plt.subplot(3,3,7)
plt.title('gdxx')
plt.imshow(gdxx)
plt.axis('off')

print(gdyx)
plt.subplot(3,3,8)
plt.title('gdyx')
plt.imshow(gdyx)
plt.axis('off')

print(C)
plt.subplot(3,3,9)
plt.title('C')
plt.imshow(C)
plt.axis('off')

plt.show()

print(data)
plt.imshow(data)
plt.title('data')
plt.axis('off')
plt.show()