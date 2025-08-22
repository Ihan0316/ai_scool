import cv2
import numpy as np

c = 0
cam = cv2.VideoCapture(0)
ck = False
ix, iy, nx, ny = 0, 0, 0, 0
in_data = None

cv2.namedWindow('img')

while True:
    ret, img = cam.read()

    if not ret:
        print('캡쳐 불가')
        break

    cv2.imshow('img', img) # 컬러 이미지

    gry_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    all_img = [img, gry_img]

    key = cv2.waitKey(1)
    if key == 27:
        break
    if key == ord('s'):
        i = 0
        cut_img = all_img[0]
        cv2.imshow('cut_img', img)
        cv2.destroyWindow('img')

        def draw(event, x, y, f, p):
            global ix, iy, nx, ny, cut_img, img
            if event == cv2.EVENT_LBUTTONDOWN:
                ix, iy = x, y
            elif event == cv2.EVENT_LBUTTONUP:
                nx, ny = x, y
                cut_img = img[iy:ny,ix:nx]
            else:
                cv2.imshow('cut_img', cut_img)

            if event == cv2.EVENT_RBUTTONDOWN:
                global i
                i = (i + 1) % 2
                cut_img = all_img[i]
        cv2.setMouseCallback('cut_img', draw)
        while True:
            key = cv2.waitKey(1)
            if key == ord('a'):
                cv2.imwrite('cut_img.jpg', cut_img)
                cv2.destroyWindow('cut_img')
                cv2.imshow('img', img)
                break