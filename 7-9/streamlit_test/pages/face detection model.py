import cv2
import streamlit as st
import numpy as np

st.set_page_config(layout="centered")

cascade_file = cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"

uploaded_file = st.file_uploader(
    "이미지 파일을 업로드 해 주세요", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # 이미지 읽기 및 얼굴 인식
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cascade_file)
    face_list = cascade.detectMultiScale(
        image_gs, scaleFactor=1.1, minNeighbors=1, minSize=(150, 150)
    )

    # 인식 후 이미지 만들기
    img_copy = image.copy()
    for (x, y, w, h) in face_list:
        cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 0, 255), 3)

    # 두 컬럼(한 줄)에 이미지 표시
    col1, col2 = st.columns(2)
    with col1:
        st.image(image_rgb, caption="업로드된 이미지", use_container_width=True)
    with col2:
        st.image(cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB), caption="인식된 얼굴", use_container_width=True)

    # 얼굴 좌표 및 저장 버튼
    st.write("인식한 얼굴:", face_list)
    if len(face_list) > 0:
        if st.button("이미지 저장"):
            cv2.imwrite("face_detected.jpg", img_copy)
            st.success("이미지가 정상적으로 저장되었습니다!")
    else:
        st.write("얼굴이 인식되지 않았습니다")
else:
    st.write("이미지를 업로드 해 주세요")
