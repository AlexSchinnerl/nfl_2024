import streamlit as st

with open("textfiles/ablauf_tippspiel.md") as f:
    how2_text = f.read()

st.markdown(how2_text)