import keyring
MYKEY = keyring.get_password("alxMail", "alex")

# import streamlit as st
# MYKEY = st.secrets["my_key"]