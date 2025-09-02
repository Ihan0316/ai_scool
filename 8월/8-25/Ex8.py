import cv2
import numpy as np

cam = cv2.VideoCapture(0)
c=0
run=True
while run:
    ret,img=cam.read()
    if ret==False:
        print("캡처 불가")
        break
    if not c:
        cv2.imshow('img',img)
    key=cv2.waitKey(1)
    if key==ord('c'):
        cut=img.copy()
        c=1
        cv2.imshow('cut',cut)
        def f(event,x,y,f,p):
            global ix,iy,nx,ny,cut
            if event==cv2.EVENT_LBUTTONDOWN:
                ix,iy=x,y
            elif event==cv2.EVENT_LBUTTONUP:
                nx,ny=x,y
                cut=cut[iy:ny,ix:nx]
            cv2.imshow('cut',cut)
        cv2.setMouseCallback('cut',f)
        cv2.destroyWindow('img')
    
    if key==ord('a') and c:
        cv2.destroyWindow('cut')
        c=0
    if key==ord('s'):
        cv2.imwrite('./day4/cam_cut_img.jpg',cut)
        break
    if key==27:
        run=False
else:
    cam.release()
    cv2.destroyAllWindows()
    del run
    exit(1)

gry_cut=cv2.cvtColor(cut,cv2.COLOR_BGR2GRAY)
gry_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

sift=cv2.SIFT().create()
cut_kp,cut_des=sift.detectAndCompute(gry_cut,None)
img_kp,img_des=sift.detectAndCompute(gry_img,None)

flann_matcher=cv2.DescriptorMatcher().create(cv2.DescriptorMatcher_FLANNBASED)
knn_matcher=flann_matcher.knnMatch(cut_des,img_des,2)

T=0.5
m_l=[ck_des for ck_des,new_des in knn_matcher if ck_des.distance/new_des.distance<T]#특징 매칭 정리

mc_img=np.empty(
    (max(cut.shape[0],img.shape[0]),cut.shape[1]+img.shape[1],3),np.uint8)
cv2.drawMatches(cut,cut_kp,img,img_kp,m_l,mc_img,
                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imshow('end_img',mc_img)
cv2.waitKey()
cv2.destroyAllWindows()