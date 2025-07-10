import cv2
import streamlit as st
import numpy as np

st.set_page_config(layout="centered")

# 캐스케이드 파일의 경로 지정하기
cascade_file = cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_file)

uploaded_file = st.file_uploader(
    "이미지 파일을 업로드 해 주세요", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # 업로드된 이미지 파일 읽어오기
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    st.image(uploaded_file, caption="업로드된 이미지", use_column_width=True)

    # 그레이스케일로 변환하기
    image_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 얼굴 인식 특징 파일 읽어 들이기
    cascade = cv2.CascadeClassifier(cascade_file)
    # 얼굴 인식 실행하기
    face_list = cascade.detectMultiScale(
        image_gs, scaleFactor=1.1, minNeighbors=1, minSize=(150, 150)
    )

    if len(face_list) > 0:
        # 인식한 부분 표시하기
        st.write("인식한 얼굴:", face_list)
        color = (0, 0, 255)
        for face in face_list:
            x, y, w, h = face
            cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness=8)
        # 결과 이미지 표시
        st.image(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
            caption="인식된 얼굴",
            use_column_width=True,
        )

        # Save button
        if st.button("이미지 저장"):
            cv2.imwrite("face_detected.jpg", image)
            st.success("이미지가 정상적으로 저장되었습니다!")
    else:
        st.write("얼굴이 인식되지 않았습니다")
else:
    st.write("이미지를 업로드 해 주세요")
