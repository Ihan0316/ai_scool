import cv2

# 카메라 확인
cam = cv2.VideoCapture(0)
if cam.isOpened()==False:
    print("인식 안됨")
    exit(1)

# 동작 확인
ret, img = cam.read()
if ret == False:
    print("캡쳐 불가")
    exit(1)
# 동영상 저장을 위한 설정
codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
fps = 30
h,w = img.shape[:2]
m_v = cv2.VideoWriter('./Coding/8월/8-20/m_v.avi', codec, fps, (w, h))

if m_v.isOpened() == False:
    print("비디오 생성 실패")
    exit(1)

# 실시간 영상 출력
while True:
    cam.read()
    ret, img = cam.read()
    if ret == False:
        print("캡쳐 불가")
        break
    m_v.write(img)
    cv2.imshow("Camera", img)

    key = cv2.waitKey(1)
    print(key)
    if key == 27:
        break
cam.release()
m_v.release()
cv2.destroyAllWindows()