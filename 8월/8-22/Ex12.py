import cv2

img = cv2.imread('../../data/data1.jpg')
gry_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 케니 에지 검출
eg = cv2.Canny(gry_img, 100, 100)

cv2.imshow('eg', eg)
cv2.waitKey(0)