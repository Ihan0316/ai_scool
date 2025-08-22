import cv2
import cv2.dnn

img = cv2.imread('../../data/data1.jpg')
ck_img = img[300:400,300:500,:]
cv2.rectangle(img, (300, 300), (500, 400), (0, 255, 0),3)

img_re = cv2.resize(ck_img, (0, 0), fx=5, fy=5, interpolation=cv2.INTER_NEAREST)
cv2.imshow('oj_img', img)
cv2.imshow('ck_img', img_re)
cv2.waitKey()

img_re = cv2.resize(ck_img, (0, 0), fx=5, fy=5, interpolation=cv2.INTER_LINEAR)
cv2.imshow('ck_img', img_re)
cv2.waitKey()

img_re = cv2.resize(ck_img, (0, 0), fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
cv2.imshow('ck_img', img_re)
cv2.waitKey()