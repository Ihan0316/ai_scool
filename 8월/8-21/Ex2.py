import cv2

# 이미지 준비
img = cv2.imread('./data/data1.jpg')

# 색상 정의 
r = (0, 0, 255)  # 빨간색
g = (0, 255, 0)  # 초록색
b = (255, 0, 0)  # 파란색

ck=[r,g]

# 이벤트 함수 정의
def draw(event, x, y, f, p):
    global ix, iy
    if event == cv2.EVENT_MOUSEMOVE and f == cv2.EVENT_FLAG_LBUTTON:
        cv2.circle(img, (x, y), 5, ck[0], -1)
    elif event == cv2.EVENT_RBUTTONDOWN:
       ck.reverse()
    cv2.imshow('Image', img)

cv2.imshow('Image', img) # 화면 생성(윈도우 생성으로 변환 가능)
cv2.setMouseCallback('Image', draw) # 콜백 함수 정의

run=True

while run: # 무한 루프
    key = cv2.waitKey(1)
    if key == ord('a'):
        run = False

else:
    # 자원 정리 목적
    cv2.destroyAllWindows()