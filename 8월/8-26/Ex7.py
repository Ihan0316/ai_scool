# 0. 모듈호출
import cv2
import numpy as np
from keras.models import load_model
import os
# 1. 상수값 및 변수값 설정
MODEL_PATH='./m.keras'
CANVAS_SIZE=200
BRUSH_RACIUS=7
LINE_SIZE=15
PAD_N=10
WINDOW_NAME='main'
# 2. 전역 지역 상태 결정
img=np.ones((CANVAS_SIZE,CANVAS_SIZE),dtype=np.uint8)*255
cp_img=img.copy()
prev_pt=[None,None]

def f(event,x,y,f,p):
    global prev_pt,img
    if x<0 or y<0 or img.shape[0] <= y or img.shape[1]<=x:
        return
    if event==cv2.EVENT_LBUTTONDOWN:
        prev_pt=[x,y]
        cv2.circle(img,(x,y),BRUSH_RACIUS,0,-1)
    elif event==cv2.EVENT_MOUSEMOVE and f==cv2.EVENT_FLAG_LBUTTON:
        if prev_pt[0] is not None:
            cv2.line(img,(prev_pt[0],prev_pt[1]),(x,y),0,LINE_SIZE)
        prev_pt=[x,y]
    elif event ==cv2.EVENT_LBUTTONUP:
        prev_pt=[None,None]
                   
# 딥러닝 모델을 이용한 비전 시스템
# 1. 전처리 정리
def pre_28_28(in_img,pad=10):
    img=in_img.copy()
    img=255-img
    _,th=cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ys,xs=np.where(th>0)
    x0,x1=xs.min(),xs.max()
    y0,y1=ys.min(),ys.max()
    
    h,w=th.shape
    x0=max(0,x0-pad)
    y0=max(0,y0-pad)
    x1=min(w,x1+pad)
    y1=min(h,y1+pad)
    
    crop= th[y0:y1+1,x0:x1+1]
    
    ch,cw=crop.shape
    if ch>=cw:
        new_h=20
        new_w=max(1,int(round(cw*(20/ch))))
    else:
        new_w=20
        new_h=max(1,int(round(ch*(20/cw))))
        
    resized=cv2.resize(crop,(new_w,new_h),interpolation=cv2.INTER_AREA)
    
    canvas=np.zeros((28,28),dtype=np.uint8)
    x_off=(28-new_w)//2
    y_off=(28-new_h)//2
    canvas[y_off:y_off+new_h,x_off:x_off+new_w]=resized
    
    M=cv2.moments(canvas,binaryImage=True)
    if M['m00']>0:
        cx=int(M['m10']/M['m00'])
        cy=int(M['m01']/M['m00'])
        dx=14-cx
        dy=14-cy
        T=np.float32([[1,0,dx],[0,1,dy]])
        canvas=cv2.warpAffine(canvas,T,(28,28),
                              flags=cv2.INTER_NEAREST,borderMode=cv2.BORDER_CONSTANT,
                       borderValue=0)
    return canvas 

# 2. 모델 동작을 위한 main 정리
def predict_m(m,canvas):
    x=canvas.astype('float32')/255.0
    X=x.reshape(1,28*28)
    py=m.predict(X)
    out = py.argmax(axis=1)[0]
    return out
# 3. main 동작
def main():
    global img,cp_img
    
    m=load_model(MODEL_PATH)
    m.trainable=False
    
    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME,f)
    
    while True:
        cv2.imshow(WINDOW_NAME,img)
        key=cv2.waitKey(1)
        if key==27:
            break
        if key==ord('r'):
            img=cp_img.copy()
        if key==ord('y'):
            pre_img=pre_28_28(img)
            out=predict_m(m,pre_img)
            print(out)
        
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()