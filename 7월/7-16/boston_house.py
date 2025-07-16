import streamlit as st
import joblib
import numpy as np

st.title("1. 주택 정보 입력")

# 1. 입력값 받기 (모델 feature 순서에 맞게)
crim = st.slider("범죄율 (CRIM)", 0.0, 100.0, 10.0)
zn = st.slider("25,000평방미터 초과 거주지역 비율 (ZN)", 0.0, 100.0, 0.0)
indus = st.slider("비상업지역 넓이 비율 (INDUS)", 0.0, 30.0, 5.0)
chas = st.selectbox("찰스강 경계 여부 (CHAS)", [0, 1], format_func=lambda x: "예" if x==1 else "아니오")
nox = st.slider("일산화질소 농도 (NOX)", 0.0, 1.0, 0.5)
rm = st.slider("방의 개수 (RM)", 1.0, 10.0, 6.0)
age = st.slider("1940년 이전 건축 비율 (AGE)", 0.0, 100.0, 50.0)
dis = st.slider("직업센터까지 거리 (DIS)", 0.0, 15.0, 5.0)
rad = st.slider("고속도로 접근 용이성 (RAD)", 1, 24, 1)
tax = st.slider("재산세 비율 (TAX)", 100, 800, 300)
ptratio = st.slider("교사와 학생 수 비율 (PTRATIO)", 10.0, 30.0, 15.0)
b = st.slider("흑인 거주 비율 (B)", 0.0, 400.0, 350.0)
lstat = st.slider("하위 계층 비율 (LSTAT)", 0.0, 40.0, 10.0)

st.markdown("## 2. 옵션 선택")
# (RAD는 위에서 이미 입력받음)

if st.button("가격 예측하기"):
    # 입력값을 numpy array로 변환 (2차원)
    input_data = np.array([[rm, chas, rad, zn, indus, age, tax, b, crim, lstat, ptratio, dis, nox]])
    # 모델 불러오기
    model_filename = './model/boston_reg_all.joblib'
    load_model = joblib.load(model_filename)
    # 예측
    pred = load_model.predict(input_data)
    st.success(f"예상 주택 가격: {pred[0]:.2f} (단위: $1000)")
