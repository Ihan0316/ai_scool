import cv2
import numpy as np

cam = cv2.VideoCapture(0)
if cam.isOpened()==False:
    print("인식 안됨")
    exit(1)
else:
    print("카메라 인식됨")

while True:
    cam.read()
    ret, img = cam.read()
    if ret == False:
        print("캡쳐 불가")
        break
    cv2.imshow("Camera", img)
    key = cv2.waitKey(1)
    print(key)
    if key == 27:
        break
cam.release()
cv2.destroyAllWindows()