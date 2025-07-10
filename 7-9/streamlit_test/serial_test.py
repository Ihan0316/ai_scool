import streamlit as st

# def unserializable_data():
#     return lambda x: x

# #👇 results in an exception when enforceSerializableSessionState is on
# st.session_state.unserializable = unserializable_data()

# slider = st.slider(
#     label='My Slider', min_value=1,
#     max_value=10, value=5, key='my_slider')
#
# st.session_state.my_slider = 7

if 'my_button' not in st.session_state:
    st.session_state.my_button = True

st.button('My button', key='my_button')