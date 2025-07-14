import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Haar Cascade 분류기 로드
cascade_file = cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"

face_cascade = cv2.CascadeClassifier(cascade_file)

def detect_faces(image_pil): # Renamed 'image' to 'image_pil' for clarity
    # 1. PIL Image를 NumPy 배열 (RGB)로 변환
    img_rgb = np.array(image_pil.convert('RGB'))

    # 2. RGB 이미지를 그레이스케일로 변환
    #    PIL Image는 RGB 순서로 데이터를 저장하므로, cv2.COLOR_RGB2GRAY를 사용해야 합니다.
    #    이전 코드에서 COLOR_BGR2GRAY를 두 번 사용한 것이 문제의 원인이었습니다.
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # 얼굴 검출 (그레이스케일 이미지 사용)
    # detectMultiScale의 인자들은 튜닝이 필요할 수 있습니다.
    # 1.1: scaleFactor, 4: minNeighbors
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # 원본 컬러 이미지(img_rgb)에 사각형을 그립니다.
    # OpenCV는 BGR 순서를 사용하므로, RGB인 img_rgb를 BGR로 변환하여 그립니다.
    img_bgr_for_drawing = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

    for (x, y, w, h) in faces:
        # 사각형 그리기: 이미지, 시작점, 끝점, 색상(BGR), 두께
        cv2.rectangle(img_bgr_for_drawing, (x, y), (x+w, y+h), (0, 255, 0), 2) # 초록색 사각형

    # 결과 이미지는 BGR 형태이므로, Streamlit 출력을 위해 RGB로 변환하여 반환
    return img_bgr_for_drawing, faces


def run_webcam():
    FRAME_WINDOW = st.image([]) # 웹캠 스트림을 표시할 Streamlit 위젯

    # 웹캠 비디오 캡처 객체 생성
    # Streamlit Cloud에서는 cv2.VideoCapture(0)이 작동하지 않을 수 있습니다.
    # 로컬 개발 환경에서는 보통 작동합니다.
    # 클라우드 환경에서는 st.camera_input()을 사용하는 것이 더 적합합니다.
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("웹캠을 열 수 없습니다. 카메라가 연결되어 있고 다른 앱에서 사용 중이 아닌지 확인하세요.")
        return # 웹캠 열기 실패 시 함수 종료

    st.write("웹캠이 실행 중입니다. 'q' 키 (터미널) 또는 Streamlit 사이드바 옵션 변경으로 중지하세요.")

    while True:
        ret, frame_bgr = cap.read() # BGR 형식으로 프레임 읽기 (OpenCV 기본)

        if not ret:
            st.write("프레임을 읽을 수 없습니다. 웹캠 스트림을 종료합니다.")
            break

        # detect_faces 함수는 PIL Image를 기대하지만,
        # 웹캠 프레임은 numpy array (BGR)이므로 PIL Image로 먼저 변환해야 합니다.
        # 또한, detect_faces 내부에서 RGB -> GRAY 변환을 처리하므로, 여기서는 바로 PIL로 변환
        frame_rgb_for_pil = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB) # BGR을 RGB로 변환 (PIL Image용)
        pil_image_from_frame = Image.fromarray(frame_rgb_for_pil)

        # 얼굴 감지 및 사각형 그리기
        # detect_faces는 BGR 이미지를 반환하도록 수정되었으므로, 바로 Streamlit에 전달 가능
        result_img_bgr, _ = detect_faces(pil_image_from_frame)

        # Streamlit은 RGB 이미지를 기대하므로, 결과 이미지가 BGR이라면 RGB로 변환하여 표시
        FRAME_WINDOW.image(cv2.cvtColor(result_img_bgr, cv2.COLOR_BGR2RGB))

        # Streamlit 앱 내에서는 cv2.waitKey가 일반적으로 작동하지 않습니다.
        # 웹캠 중지는 주로 다른 사이드바 옵션 선택이나 앱 새로고침으로 이루어집니다.
        # 로컬에서 터미널에서 실행 시 'q'로 종료하려면 이 주석을 해제할 수 있습니다:
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release() # 웹캠 자원 해제
    cv2.destroyAllWindows() # 열린 OpenCV 창 닫기 (웹캠 스트림의 경우 필요 없을 수 있음)


def main():
    st.title("Haar Cascade 얼굴 인식 프로그램")
    st.write("이미지 파일에서 얼굴을 인식하거나 웹캠으로 실시간 얼굴을 탐지합니다.")

    st.sidebar.title("옵션 선택")
    app_mode = st.sidebar.selectbox("모드 선택",["이미지로부터", "웹캠으로부터"])

    if app_mode == "이미지로부터":
        st.header("🖼️ 이미지에서 얼굴 인식")
        upload_file = st.file_uploader("이미지 파일을 업로드 하세요...", type=['jpg','png', 'jpeg'])

        if upload_file is not None:
            image = Image.open(upload_file)
            st.image(image, caption='업로드된 이미지', use_column_width=True)

            if st.button('얼굴 인식 시작'): # 버튼 이름 변경하여 일관성 유지
                st.info('얼굴 인식 중... 잠시 기다려 주세요.')
                result_img, result_faces = detect_faces(image)
                st.image(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB), caption='얼굴 인식 결과', use_column_width=True)
                st.success(f'{len(result_faces)}개의 얼굴을 찾았습니다!')

    # elif 대신 새로운 if 문으로 분리하여 각 모드별로 실행되도록 함
    # Streamlit의 selectbox는 단일 값만 반환하므로, if/elif로 연결하는 것이 맞습니다.
    # 이전 코드에서 else if app_mode == "웹캠으로부터"는 잘못된 문법이었습니다.
    # if/elif/else 구조로 다시 연결하는 것이 더 적합합니다.
    elif app_mode == "웹캠으로부터": # 여기서 elif로 연결해야 함
        st.header("📸 웹캠으로 실시간 얼굴 인식")
        st.write("웹캠으로 실시간 얼굴을 탐지합니다. '얼굴 인식 시작' 버튼을 누르세요.")

        if st.button('웹캠 얼굴 인식 시작'): # 버튼 이름 변경
            st.warning("웹캠을 중지하려면 Streamlit 사이드바에서 다른 옵션을 선택하거나, 페이지를 새로고침(R) 하세요.")
            run_webcam() # 웹캠 실행 함수 호출


if __name__ == "__main__":
    main()