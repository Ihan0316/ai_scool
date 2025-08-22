import cv2
import numpy as np

oj_img = cv2.imread('../../data/data1.jpg')
img = cv2.cvtColor(oj_img, cv2.COLOR_BGR2RGB)
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

print(img.shape)

# 이미지 리사이징(f 값을 통해 비율 설정)
tr_img1 = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
print(tr_img1.shape)

# 이미지 리사이징(dsize로 픽셀 설정)
tr_img2 = cv2.resize(img, (100, 100))
print(tr_img2.shape)

def g_tr(f, g=1.0):
    s_f = f / 255.0
    return np.uint8(255 * (s_f ** g))
end_img = np.hstack((g_tr(tr_img1, 0.5), g_tr(tr_img1, 0.7), g_tr(tr_img1, 2.0), g_tr(tr_img1, 3.0)))
cv2.imshow('oj_img', img)
cv2.imshow('end_img', end_img)
cv2.waitKey(0)