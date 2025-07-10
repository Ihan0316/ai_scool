import streamlit as st

# 페이지 정의
main_page = st.Page("main_page.py", title="Main Page", icon="🎈")
page_2 = st.Page("page_2.py", title="Page 2", icon="❄️")
page_3 = st.Page("page_3.py", title="Page 3", icon="🎉")

# 메뉴 구성
nv = st.navigation([main_page, page_2, page_3])

# 선택된 페이지 실행
nv.run()