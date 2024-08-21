import streamlit as st

pg = st.navigation([
    st.Page("page_vorab.py"),
    st.Page("page_weekly.py"),
    st.Page("page_standing.py"),
    st.Page("page_help.py")
    ])
pg.run()
