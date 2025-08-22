import cv2
import numpy as np

cam = cv2.VideoCapture(0)
while True:
    ret, img = cam.read()
    if not ret:
        print('캡쳐 불가')
        break

    gry_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('og_img', gry_img)

    s = cv2.GaussianBlur(gry_img,(15,15),0,0)
    cv2.imshow('s', s)

    k = np.array([[-1, 0, 0], [0, 0, 0], [0, 0, 1]])
    ck_1_img = cv2.filter2D(gry_img, -1, k)

    gry_img16 = np.int16(gry_img)
    e = np.uint8(np.clip(cv2.filter2D(gry_img16, -1, k)+128, 0, 255))
    cv2.imshow('ck_1_img', ck_1_img)
    cv2.imshow('e',e)

    key = cv2.waitKey(1)
    if key==27:
        break

cam.release()
cv2.destroyAllWindows()