import cv2
import numpy as np

img = cv2.imread('../../data/data1.jpg')
re_img = cv2.resize(img, (0, 0), fx=0.4, fy=0.4)
gry_img = cv2.cvtColor(re_img, cv2.COLOR_BGR2GRAY)

# 가우시안 블러 처리(ksize로 흐림 정도 설정)
g1 = cv2.GaussianBlur(gry_img, (3, 3), 0, 0)
g2 = cv2.GaussianBlur(gry_img, (5, 5), 0, 0)
g3 = cv2.GaussianBlur(gry_img, (7, 7), 0, 0)
g4 = cv2.GaussianBlur(gry_img, (9, 9), 0, 0)
g5 = cv2.GaussianBlur(gry_img, (15, 15), 0, 0)

g_all = np.hstack((gry_img, g1, g2, g3, g4, g5))

cv2.imshow('g_all', g_all)

k = np.array([[-1, 0, 0],
              [0, 0, 0],
              [0, 0, 1]])

gry_img16 = np.int16(gry_img)

# 변화된 이미지
t1 = np.uint8(np.clip(cv2.filter2D(gry_img16, -1, k)+128, 0, 255))
t2 = np.uint8(cv2.filter2D(gry_img16, -1, k)+128)
t3 = cv2.filter2D(gry_img16, -1, k)

cv2.imshow('t1', t1)
cv2.imshow('t2', t2)
cv2.imshow('t3', t3)

cv2.waitKey(0)
