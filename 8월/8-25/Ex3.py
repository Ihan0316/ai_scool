import cv2
img=cv2.imread('./day4/data4-1.jpg')
gry_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
sift=cv2.SIFT_create()
#ck=cv2.SIFT()-> ck.create()
ck=cv2.SIFT()
sift2=ck.create()
#print(sift2)
kp,des=sift2.detectAndCompute(gry_img,None)
gry_img_ck=cv2.drawKeypoints(gry_img,kp,None,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow('kp1_img',gry_img_ck)

img2=cv2.imread('./day4/data4-2.jpg')#이미지 로드
gry_img2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)#이미지 명암화
sift2_2=cv2.SIFT().create()#검출자(기술자) 생성
kp,des=sift2_2.detectAndCompute(gry_img2,None)#특징 검출 및 기술
gry_img_ck2=cv2.drawKeypoints(gry_img2,kp,None,
                              flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)#시각화
cv2.imshow('kp2_img',gry_img_ck2)
cv2.waitKey(0)
