import streamlit as st
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.scatter([1,2,3], [1,2,3])

st.pyplot(fig)