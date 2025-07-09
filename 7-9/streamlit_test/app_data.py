import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'col1':[1,2,3,4],
    'col2':[10, 20, 30, 40]
})

st.dataframe(df)
st.table(df)
st.metric(label="온도", value="25℃", delta="1.5℃")