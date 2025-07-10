#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 10:11:37 2025

@author: ihanjo
"""

import streamlit as st
import pandas as pd
import time

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    time.sleep(5)
    return df

st.write("데이터 로딩 시작...")
df = load_data('bike.csv')
st.write('데이터 로딩 완료!! :sunglasses:')
st.dataframe(df)
