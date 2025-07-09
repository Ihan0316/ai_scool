import streamlit as st

if 'count' not in st.session_state:
    st.session_state.count = 0

if st.button('카운트'):
    st.session_state.count += 1

st.write('버튼 클릭 횟수:', st.session_state.count)