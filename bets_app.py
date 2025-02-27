import streamlit as st

st.set_page_config(
    layout="wide"
    )
pg = st.navigation([
    st.Page(page="page_playoffs.py", title="Playoff Tipps", url_path="playoffs"),
    # st.Page(page="page_vorab.py", title="Vorab Tipps", url_path="vorab"),
    # st.Page(page="page_weekly.py", title="Wöchentliche Tipps", url_path="weekly"),
    st.Page(page="page_standing.py", title="Regular Season - Endstand", url_path="standing"),
    st.Page(page="page_help.py", title="Anleitung", url_path="help"),
    ])
pg.run()


# ---------------------------------

# CSS hack für Sidebar Größe
# st.markdown(
#     """
#     <style>
#         section[data-testid="stSidebar"] {
#             width: 400px !important; # Set the width to your desired value
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

