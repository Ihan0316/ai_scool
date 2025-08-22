import cv2

oj_img = cv2.imread('../../data/data1.jpg')
img = oj_img.copy()

def cut(event, x, y, f, p):
    global sx, sy, ex, ey, img
    if event == cv2.EVENT_LBUTTONDOWN:
        sx, sy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        ex, ey = x, y
        img=img[sy:ey,sx:ex]
    cv2.imshow('img', img)


# cv2.namedWindow('img')
cv2.imshow('img', img)
cv2.setMouseCallback('img', cut)

run = True
while run:
    key = cv2.waitKey(1)
    if key==ord('a'):
        run = False
    if key==ord('c'):
        img = oj_img.copy()
        cv2.imshow('img', img)
else:
    cv2.destroyAllWindows()