import cv2
import numpy as np
def load_img(*imgs):
    end_l=[]
    for img in imgs:
        img_data=cv2.imread(img)
        gry_img=cv2.cvtColor(img_data,cv2.COLOR_BGR2GRAY)
        end_l.append((img_data,gry_img))
    return end_l
d=load_img('./day4/data4-1.jpg','./day4/data4-2.jpg')
ck_img=d[0][0][190:350,440:560]
gry_ck_img=d[0][1][190:350,440:560]
new_img=d[1][0]
gry_new_img=d[1][1]

sift=cv2.SIFT().create()
ck_kp,ck_des=sift.detectAndCompute(gry_ck_img,None)#특징 기술
new_kp,new_des=sift.detectAndCompute(gry_new_img,None)     

flann_matcher=cv2.DescriptorMatcher().create(cv2.DescriptorMatcher_FLANNBASED)#특징 1차매칭
knn_matcher=flann_matcher.knnMatch(ck_des,new_des,2)
T=0.5 #정리 기준
m_l=[ck_des for ck_des,new_des in knn_matcher if ck_des.distance/new_des.distance<T]#특징 매칭 정리
#print(ck_kp[52].pt)
#for gm in m_l:
    #print(i.queryIdx)#기준 키포인트의 인덱스
    #print(i.trainIdx)#확인 키포인트의 인덱스
kp_ck=np.float32([ck_kp[gm.queryIdx].pt for gm in m_l])
kp_new=np.float32([new_kp[gm.trainIdx].pt for gm in m_l])    

H,_=cv2.findHomography(kp_ck,kp_new,cv2.RANSAC)

h1,w1=ck_img.shape[0],ck_img.shape[1]
h2,w2=new_img.shape[0],new_img.shape[1]

box1=np.float32([[0,0],[0,h1-1],[w1-1,h1-1],[w1-1,0]]).reshape(4,1,2)
box2=cv2.perspectiveTransform(box1,H)

new_img=cv2.polylines(new_img,[np.int32(box2)],True,(0,255,0),8)
mc_img=np.empty(
    (max(ck_img.shape[0],new_img.shape[0]),ck_img.shape[1]+new_img.shape[1],3),np.uint8)
cv2.drawMatches(ck_img,ck_kp,new_img,new_kp,m_l,mc_img,
                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imshow('end_img',mc_img)
cv2.waitKey(0)
cv2.destroyAllWindows()