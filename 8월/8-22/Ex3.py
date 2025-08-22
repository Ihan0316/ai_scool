import cv2

img = cv2.imread('../../data/data1.jpg')
gry_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 밝기를 파악하여 영역을 선정

t,th_img = cv2.threshold(gry_img, 119, 255, cv2.THRESH_OTSU)
cv2.imshow('th_img', th_img)
cv2.waitKey(0)

t1,th_img = cv2.threshold(gry_img, 119, 255, cv2.THRESH_BINARY)
cv2.imshow('th_img', th_img)
cv2.waitKey(0)

t2,th_img = cv2.threshold(gry_img, 119, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('th_img', th_img)
cv2.waitKey(0)

print(t, t1, t2)

cv2.imshow('img', img)
# cv2.imshow('gry_img', gry_img)
cv2.waitKey(0)