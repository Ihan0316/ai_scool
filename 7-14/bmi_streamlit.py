import streamlit as st
import pickle

# 스타일 및 한글 라벨 매핑
CATEGORY_LABELS = {1: '저체중', 2: '정상', 3: '비만'}
CATEGORY_COLORS = {1: 'blue', 2: 'green', 3: 'red'}

st.set_page_config(page_title="BMI 예측기", page_icon=":weight_lifter:", layout="centered")
st.title('💪 BMI 예측기')
st.markdown("#### 키(cm)와 몸무게(kg)를 입력하면 BMI 분류 결과를 알려드립니다.")

# 입력 폼
with st.form("bmi_form"):
    col1, col2 = st.columns(2)
    with col1:
        height = st.text_input('키 (cm)', placeholder="예: 170")
    with col2:
        weight = st.text_input('몸무게 (kg)', placeholder="예: 65")
    submitted = st.form_submit_button("예측하기")

# 모델 로드
with open('./bmi_predict.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

# 예측 및 결과 표시
if submitted:
    # 입력값 검증
    try:
        h = float(height)
        w = float(weight)
        if h <= 0 or w <= 0:
            st.error("키와 몸무게는 0보다 커야 합니다.")
        elif h > 201 or w > 101:
            st.error("입력값이 비현실적입니다. 다시 확인해주세요.")
        else:
            pred = loaded_model.predict([[h, w]])[0]
            bmi_value = w / ((h / 100) ** 2)
            label = CATEGORY_LABELS.get(pred, "알 수 없음")
            color = CATEGORY_COLORS.get(pred, "gray")
            st.markdown(
                f"""
                <div style="padding:1.5em; border-radius:10px; background-color:#eeeee; border:1px solid #eee;">
                    <h3 style="color:{color};">예측 결과: <b>{label}</b></h3>
                    <ul>
                        <li><b>BMI 수치:</b> {bmi_value:.2f}</li>
                        <li><b>키:</b> {h:.1f} cm</li>
                        <li><b>몸무게:</b> {w:.1f} kg</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
    except ValueError:
        st.error("숫자만 입력해주세요.")
else:
    st.info("키와 몸무게를 입력 후 '예측하기' 버튼을 눌러주세요.")