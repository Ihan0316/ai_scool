import streamlit as st

# 세션 초기화
if 'key' not in st.session_state:
    st.session_state['key'] = 'hgd'

# 다른 방식 으로 세션 초기화
if 'key' not in st.session_state:
    st.session_state.key = 'hgd'

# 쓰기
st.write(st.session_state.key)

# 출력
st.session_state.key = 'value2'     # Attribute API
st.session_state['key'] = 'value2'  # 딕셔너리 방식 API

st.write(st.session_state)

# 그냥 써도 출력은 가능하나 명시적으로 표현하는것이 좋음
# st.session_state

# 에러 발생
# st.write(st.session_state['value'])

# 키 하나를 삭제하기
del st.session_state['key']

# 키가 있는 모든 위젯은 자동으로 들어감
st.text_input("Your name", key="name")

# .키를 넣어 출력
# st.session_state.name

# 콜백 함수
def form_callback(): # 함수 이름을 form_callback 으로 설정, 매개변수 는 없음
    st.write(st.session_state.my_slider) # st.session_state.my_slider의 값을 쓰기
    st.write(st.session_state.my_checkbox) # st.session_state.my_checkbox의 값을 쓰기

# 폼에 어떤 값을 넣을지 설정
with st.form(key='my_form'): # 폼의 키를 my_form 으로 설정
    slider_input = st.slider('My slider', 0, 10, 5, key='my_slider') # slider 이름을 My slider로 지정, 0~10 범위로 지정, 디폴트 값을 5로 지정, key 값을 my_slider로 설정
    checkbox_input = st.checkbox('Yes or No', key='my_checkbox')    # checkbox의 값을 Yes or No로 설정, key 값을 my_checkbox로 설정
    submit_button = st.form_submit_button(label='Submit', on_click=form_callback) # form_submit_button의 label을 Submit 으로 설정, on_click(클릭시 실행 함수)를 form_callback 으로 설정