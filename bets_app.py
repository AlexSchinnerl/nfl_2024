import streamlit as st

pg = st.navigation([
    st.Page(page="page_vorab.py", title="Vorab Tipps"),
    st.Page(page="page_weekly.py", title="Wöchentliche Tipps"),
    st.Page(page="page_standing.py", title="Zwischenstand"),
    st.Page(page="page_help.py", title="Anleitung")
    ])
pg.run()
