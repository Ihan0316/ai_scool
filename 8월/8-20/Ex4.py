import cv2

data = cv2.VideoCapture('/Users/ihanjo/Library/CloudStorage/GoogleDrive-ihann5726@gmail.com/내 드라이브/인공지능 사관학교/Coding/8월/8-20/m_v.avi')

if data.isOpened() == False:
    print("비디오 파일 열기 실패")
    exit(1)

while True:
    ret, img = data.read()
    if ret == False:
        print("비디오 파일 읽기 실패")
        break

    cv2.imshow("Video", img)

    key = cv2.waitKey(30)
    if key == 27:
        break