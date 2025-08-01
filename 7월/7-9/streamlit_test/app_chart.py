import streamlit as st
import numpy as np
import pandas as pd

char_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)

st.line_chart(char_data)
st.bar_chart(char_data)