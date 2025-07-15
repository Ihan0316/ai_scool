import streamlit as st
import pickle

# 스타일 및 한글 라벨 매핑
CATEGORY_LABELS = {1: '저체중', 2: '정상', 3: '비만'}
CATEGORY_COLORS = {1: 'blue', 2: 'green', 3: 'red'}

# 페이지 설정 부분 수정
st.set_page_config(
    page_title="BMI 예측기",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="collapsed"
)
st.title('💪 BMI 예측기')
st.markdown("#### 키(cm)와 몸무게(kg)를 입력하면 BMI 분류 결과를 알려드립니다.")
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50; /* 초록색 버튼 */
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
    }
    .stTextInput>input {
        border-radius: 8px;
        border-color: #ccc;
    }
</style>
""", unsafe_allow_html=True)
# 기존 form 코드 수정
with st.form("bmi_form"):
    col1, col2 = st.columns([0.45, 0.45])  # 컬럼 비율 조정
    with col1:
        height = st.slider('📏 키 (cm)', min_value=130, max_value=210, value=170, step=1, help="150~200 cm 범위 권장")
    with col2:
        weight = st.slider('⚖️ 몸무게 (kg)', min_value=30, max_value=150, value=65, step=1, help="30~120 kg 범위 권장")
    submitted = st.form_submit_button("🔮 예측하기", use_container_width=True)

# 모델 로드
with open('model/bmi_predict.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

# 예측 및 결과 표시
if submitted:
    # 입력값 검증
    try:
        h = float(height)
        w = float(weight)
        if h <= 0 or w <= 0:
            st.error("키와 몸무게는 0보다 커야 합니다.")
        elif h > 200 or w > 200:
            st.error("입력값이 비현실적입니다. 다시 확인해주세요.")
        else:
            pred = loaded_model.predict([[h, w]])[0]
            bmi_value = w / ((h / 100) ** 2)
            label = CATEGORY_LABELS.get(pred, "알 수 없음")
            color_hex = "#007BFF" if pred == 1 else "#28A745" if pred == 2 else "#DC3545"

            st.markdown(
                f"""
                       <div style="padding:2em; border-radius:15px; background-color:#000000; box-shadow: 0px 4px 8px rgba(0,0,0,0.1);">
                           <h3 style="color:{color_hex};">🎯 예측 결과: <b>{label}</b></h3>
                           <ul style="font-size:1.1em;">
                               <li>📊 BMI 수치: {bmi_value:.2f}</li>
                               <li>📏 키: {h:.1f} cm</li>
                               <li>⚖️ 몸무게: {w:.1f} kg</li>
                           </ul>
                       </div>
                       """,
                unsafe_allow_html=True
            )

            # BMI 범위 설명 추가
            st.info("💡 **BMI 해설**\n- 저체중: BMI < 18.5\n- 정상: 18.5 ≤ BMI ≤ 24.9\n- 비만: BMI ≥ 25")


    except ValueError:
        st.error("❗️ 숫자만 입력해주세요.")
    else:
        st.info("📝 키와 몸무게를 입력 후 '🔮 예측하기' 버튼을 눌러주세요.")

