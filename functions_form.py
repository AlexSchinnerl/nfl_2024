import pandas as pd
import streamlit as st
from functions_mail import send_mail_function
from functions_key import MYKEY

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

def bets_input(week_nr, player, bets):
    df = pd.read_csv("data/bets_2024.csv")
    df.loc[df["Week"] == week_nr, player] = bets
    df.to_csv("data/bets_2024.csv", index=False)