import streamlit as st

st.title('BMI MODEL TEST')
st.header('아래의 란에 키, 몸무게를 입력해보세요!!')
height = st.text_input('키')
weight = st.text_input('몸무게')

# st.write()