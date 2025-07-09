import streamlit as st
import pandas as pd

df = pd.read_csv('bike.csv')
df.index = range(1, len(df) + 1)

st.subheader('서울시 공공자전거 2020년 12월 데이터 🚴🏻📊')
st.dataframe(df)