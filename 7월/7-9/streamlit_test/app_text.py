import streamlit as st

st.title("제목 (Title)")
st.header("헤더 (Header)")
st.subheader("서브헤더 (Subheader)")
st.text("일반 텍스트 (Text)")
st.markdown("`Markdown` **지원**합니다.")
st.code("print('Hello, Streamlit!')")

code1 = '''
import streamlit as st
st.title("제목")
st.header("헤더")
'''

st.code(code1, language='python')