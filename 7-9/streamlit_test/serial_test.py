import streamlit as st

def unserializable_data():
    return lambda x: x

#👇 results in an exception when enforceSerializableSessionState is on
st.session_state.unserializable = unserializable_data()