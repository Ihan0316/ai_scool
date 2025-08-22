import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('../../data/data3.jpg')

# 그레이스케일로 변환
gry_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gry_hist = cv2.calcHist([gry_img], [0], None, [256], [0, 256])
cv2.imshow( 'gry_hist', gry_img)
plt.plot(gry_hist)

# 히스토그램 평활화
e_img = cv2.equalizeHist(gry_img)
e_hist = cv2.calcHist([e_img], [0], None, [256], [0, 256])
cv2.imshow( 'e_hist', e_img)
plt.plot(e_hist)

plt.show()
cv2.waitKey(0)