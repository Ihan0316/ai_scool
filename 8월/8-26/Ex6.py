import cv2
import numpy as np
from keras.models import load_model

m=load_model('m.keras')

img = np.ones((200, 200), dtype=np.uint8) * 255
cp_img = img.copy()

def f(event,x,y,f,p):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 7, (0, 0, 0), -1)
    elif event == cv2.EVENT_MOUSEMOVE and f==cv2.EVENT_FLAG_LBUTTON:
        cv2.circle(img, (x, y), 7, (0, 0, 0), -1)

def mk_num():
    num = img
    num = 255-cv2.resize(num, (28,28))
    print(num)
    return num

def end_f(py):
    out = py.argmax(axis=1)
    return out

cv2.namedWindow('w')
cv2.setMouseCallback('w', f)
while True:
    cv2.imshow( 'w', img)
    key = cv2.waitKey(1)
    if key == 27:
        break
    if key == ord('r'):
        img = cp_img.copy()
    if key == ord('y'):
        ck_data = mk_num()
        s_x = ck_data.reshape(-1, 28*28)/255.0
        py = m.predict(s_x)
        out = end_f(py)
cv2.destroyAllWindows()