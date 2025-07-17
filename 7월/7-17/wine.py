import streamlit as st
import joblib
import numpy as np

st.title("와인 정보 입력🍷")

# st.함수("나타낼 내용", 시작값, 끝값, 디폴트 값, step=단계 지정....)
alcohol = st.number_input("alcohol", 8.0, 14.9, step=0.1)
sugar = st.number_input("sugar", 0.6, 65.8, step=0.1)
pH = st.number_input("pH", 2.72, 4.01, step=0.01)

if st.button("와인 예측하기"):

    input_data = np.array([[alcohol, sugar, pH]])
    # 모델 불러오기
    model_filename = './model/wine.joblib'
    load_model = joblib.load(model_filename)
    # 예측
    pred = load_model.predict(input_data)
    if pred[0] == 0:
        pred = '화이트 와인'

    else:
        pred = '레드 와인'
    st.success(f"예상 와인: {pred}")