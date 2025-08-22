import cv2
import numpy as np

img = cv2.imread('../../data/data1.jpg')
im_sw = img.copy()

# 배경이다 cv2.GC_BGD(확정 배경)
# 배경일꺼야 cv2.GC_PR_BGD()

# 물체이다 cv2.GC_FGD(확정 물체)
# 물체일꺼야 cv2.GC_PR_FGD()

mask_img = np.zeros((im_sw.shape[0], im_sw.shape[1]), np.uint8)
mask_img[:,:]=cv2.GC_PR_BGD

def f(event, x, y, f, p):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(im_sw, (x, y), 10, (255, 0, 0), -1)
        cv2.circle(mask_img, (x, y), 10, cv2.GC_FGD, -1)

    elif event == cv2.EVENT_MOUSEMOVE and f == cv2.EVENT_FLAG_LBUTTON:
        cv2.circle(im_sw, (x, y), 10, (255, 0, 0), -1)
        cv2.circle(mask_img, (x, y), 10, cv2.GC_FGD, -1)

    elif event == cv2.EVENT_RBUTTONUP:
        cv2.circle(im_sw, (x, y), 10, (0, 0, 255), -1)
        cv2.circle(mask_img, (x, y), 10, cv2.GC_BGD, -1)

    elif event == cv2.EVENT_MOUSEMOVE and f == cv2.EVENT_FLAG_RBUTTON:
        cv2.circle(im_sw, (x, y), 10, (0, 0, 255), -1)
        cv2.circle(mask_img, (x, y), 10, cv2.GC_BGD, -1)
    cv2.imshow('main', im_sw)

cv2.imshow('main', im_sw)
cv2.setMouseCallback('main',f)

while True:
    key = cv2.waitKey(1)
    if key == 27:
        break
f_h = np.zeros((1, 65), np.float64) # 물체
b_h = np.zeros((1, 65), np.float64) # 배경
cv2.grabCut(img, mask_img, None, f_h, b_h, 5, cv2.GC_INIT_WITH_MASK)
end_mask_img = np.where((mask_img == cv2.GC_BGD)|(mask_img == cv2.GC_PR_BGD), 0, 1).astype('uint8')
grab_img = img * end_mask_img[:,:,np.newaxis]
print(grab_img.shape)
cv2.imshow('out_img', grab_img)
r, th_img = cv2.threshold(cv2.cvtColor(grab_img, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY)
cv2.imshow('mask_img_ck', th_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
