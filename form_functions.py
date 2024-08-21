import streamlit as st
from mail_function import send_mail_function

import keyring
MYKEY = keyring.get_password("alxMail", "alex")
# MYKEY = st.secrets["my_key"]

def name_submit(button_description):
    col1a, col1b = st.columns(2)
    with col1a:
        player_name = st.text_input("Name eingeben", placeholder="Hier euren Namen eintragen")
    with col1b:
        st.write("\n")
        st.write("\n")
        submitted = st.form_submit_button(button_description)
    return player_name, submitted

def send_form(mailText, subject):
    try:
        send_mail_function(mail_key=MYKEY, mailText=mailText, subject=subject)
        st.success("Tipps abgeschickt!")
    except Exception:
        st.error("Fehler beim Übermitteln")