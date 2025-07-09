import streamlit as st
import pandas as pd

df = pd.read_csv('bike.csv')
df.index = range(1, len(df) + 1)

st.title('Sample DataFrame')
st.dataframe(df)