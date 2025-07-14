import cv2
import streamlit as st
import numpy as np
from PIL import Image
import io

# 입력 파일
image_file = st.file_uploader("이미지 파일을 선택하세요", type=["jpeg", "jpg", "png"])

# 캐스케이드 파일의 경로 지정하기
cascade_file = "./static/haarcascade_frontalface_alt.xml"

if image_file is not None:
    # 파일 바이트를 numpy 배열로 변환
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if image is not None:
        # 그레이스케일로 변환하기
        image_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 얼굴 인식 특징 파일 읽어 들이기
        cascade = cv2.CascadeClassifier(cascade_file)
        # 얼굴 인식 실행하기
        face_list = cascade.detectMultiScale(image_gs, scaleFactor=1.1, minNeighbors=1, minSize=(150, 150))

        if len(face_list) > 0:
            # 인식한 부분 표시하기
            print(face_list)
            color = (0, 0, 255)
            for face in face_list:
                x, y, w, h = face
                cv2.rectangle(image, (x, y), (x+w, y+h), color, thickness=8)
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        else:
            print("얼굴이 인식되지 않았습니다")
    else:
        st.error("이미지를 불러오는데 실패했습니다")
else:
    st.warning("이미지 파일을 업로드해주세요")