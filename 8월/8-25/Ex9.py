import cv2
import numpy as np

c=0
ck=False
ix,iy,nx,ny=0,0,0,0
cam=cv2.VideoCapture(0)
cv2.namedWindow('img')
while True:
    ret,img=cam.read()
    if ret==False:
        print("캡처 불가")
        break
    gry_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key=cv2.waitKey(1)
    if key==27:
        break
    if key==ord('c'):
        cut=img.copy()
        cv2.destroyWindow('img')
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
        while True:
            if cv2.waitKey(1)==ord('a'):
                cv2.destroyWindow('cut')
                cv2.imwrite('./day4/cam_cut_img.jpg',cut)
                cv2.imshow('img',img)
                ck=True
                break
    if ck:
        ck_img=cut
        gry_ck_img=cv2.cvtColor(ck_img,cv2.COLOR_BGR2GRAY)
        
        sift=cv2.SIFT().create()
        ck_kp,ck_des=sift.detectAndCompute(gry_ck_img,None)
        new_kp,new_des=sift.detectAndCompute(gry_img,None)
        
        flann_matcher=cv2.DescriptorMatcher().create(cv2.DescriptorMatcher_FLANNBASED)#특징 1차매칭
        knn_matcher=flann_matcher.knnMatch(ck_des,new_des,2)
        T=0.9 #정리 기준
        m_l=[ck_des for ck_des,new_des in knn_matcher if ck_des.distance/new_des.distance<T]#특징 매칭 정리

        kp_ck=np.float32([ck_kp[gm.queryIdx].pt for gm in m_l])
        kp_new=np.float32([new_kp[gm.trainIdx].pt for gm in m_l])
        
        try:
            H,_=cv2.findHomography(kp_ck,kp_new,cv2.RANSAC)
            h1,w1=ck_img.shape[0],ck_img.shape[1]
            h2,w2=img.shape[0],img.shape[1]
            box1=np.float32([[0,0],[0,h1-1],[w1-1,h1-1],[w1-1,0]]).reshape(4,1,2)
            box2=cv2.perspectiveTransform(box1,H)
        except:
            new_img=cv2.polylines(img,[np.int32(box2)],True,(0,255,0),8)
            mc_img=np.empty((max(ck_img.shape[0],new_img.shape[0]),
                             ck_img.shape[1]+new_img.shape[1],3),np.uint8)
            cv2.drawMatches(ck_img,ck_kp,new_img,new_kp,m_l,mc_img,
                            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            cv2.imshow('img',mc_img)
            continue
        new_img=cv2.polylines(img,[np.int32(box2)],True,(0,255,0),8)
        mc_img=np.empty((max(ck_img.shape[0],new_img.shape[0]),
                             ck_img.shape[1]+new_img.shape[1],3),np.uint8)
        cv2.drawMatches(ck_img,ck_kp,new_img,new_kp,m_l,mc_img,
                            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv2.imshow('img',mc_img)
    else:
        cv2.imshow('img',img)
        continue
cam.release()
cv2.destroyAllWindows()      