import streamlit as st

# pg = st.navigation([
#     st.Page("page_vorab.py"),
#     st.Page("page_weekly.py"),
#     st.Page("page_standing.py"),
#     st.Page("page_help.py")
#     ])
# pg.run()


pages = {
    "Your account": [
        st.Page("page_vorab.py", title="Create your account"),
        st.Page("page_weekly.py", title="Manage your account"),
    ],
    "Resources": [
        st.Page("page_standing.py", title="Learn about us"),
        st.Page("page_help.py", title="Try it out"),
    ],
}

pg = st.navigation(pages)
pg.run()