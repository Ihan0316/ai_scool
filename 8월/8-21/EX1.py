import cv2

oj_img = cv2.imread('./data/data1.jpg')
ck_img = cv2.imread('./data/data1.jpg')

def draw(event, x, y, f, p):
    global ix, iy
    if event == cv2.EVENT_LBUTTONDOWN:
        ix, iy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        cv2.rectangle(ck_img, (ix,iy), (x,y), (0, 0, 255), 5)
    cv2.imshow('Image', ck_img)

cv2.imshow('Image', ck_img)
cv2.setMouseCallback('Image', draw)
while True:
    key = cv2.waitKey(1)
    if key == ord('a'):
        cv2.destroyAllWindows()
        break
    if key == ord('c'):
        ck_img = cv2.imread('./data/data1.jpg')
        cv2.imshow('Image', ck_img)