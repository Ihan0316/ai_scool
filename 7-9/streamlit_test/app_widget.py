import streamlit as st

# 1. 버튼(Button)
if st.button('눌러보세요'):
    st.write('버튼이 눌렸습니다!')

# 2. 셀렉트 박스 (Selectbox)
option = st.selectbox(
    '가장 좋아하는 동물은?',
    ('강아지', '고양이', '앵무새')
)
st.write(f'선택 : {option}')

# 3. 슬라이더 (Slider)
age = st.slider('나이를 선택하세요', 0, 100, 25)
st.write(f'당신의 나이는 {age}세 입니다.')

# 4. 텍스트 입력 (Text Input)
name = st.text_input('이름을 입력하세요', '홍길동')
st.write(f'안녕하세요, {name}님!')