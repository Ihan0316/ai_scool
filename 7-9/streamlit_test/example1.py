import streamlit as st
import pandas as pd

with open('bike.csv', 'r') as file:
    columns = ['대여일자', '대여소번호', '대여소명', '대여구분코드', '성별', '연령대코드', '이용건수', '운동량', '탄소량', '이동거리(M)', '이용시간(분)']

    df = pd.read_csv(file, names=columns, skiprows=1)
    df.index = range(1, len(df) + 1)

    st.title('Sample DataFrame')
    st.dataframe(df)