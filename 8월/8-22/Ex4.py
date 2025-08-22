import cv2
import numpy as np

img = cv2.imread('../../data/data2.png', cv2.IMREAD_UNCHANGED)
tr_img = img[(img.shape[0]//3*2):,:,3]
# print(img.shape, tr_img.shape)

# print(img.shape)
#
# cv2.imshow('img1',img[:,:,0])
# cv2.imshow('img2',img[:,:,1])
# cv2.imshow('img3',img[:,:,2])
# cv2.imshow('img4',img[:,:,3])
# cv2.waitKey(0)

cv2.imshow('img', tr_img)

se = np.uint8([[0, 1, 1, 1, 0],
               [1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1],
               [0, 1, 1, 1, 0]])

# 모폴로지 연산
d1 = cv2.dilate(tr_img, se, iterations=1) # 팽창 메소드
d2 = cv2.erode(tr_img, se, iterations=1) # 침식 메소드
d3 = cv2.dilate(cv2.erode(tr_img, se, iterations=1),se, iterations=1) # 열기
d4 = cv2.erode(cv2.dilate(tr_img, se, iterations=1),se, iterations=1) # 닫기

cv2.imshow('d1_img', d1)
cv2.imshow('d2_img', d2)
cv2.imshow('d3_img', d3)
cv2.imshow('d4_img', d4)

cv2.waitKey(0)