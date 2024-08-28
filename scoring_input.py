import streamlit as st
import pandas as pd
from functions_load_and_transform import schedule, player_list


def bets_input(week_nr, player, bets):
    df = pd.read_csv("data/bets_2024.csv")
    df.loc[df["Week"] == week_nr, player] = bets
    df.to_csv("data/bets_2024.csv", index=False)

last_week = 1

filtered_DF = schedule.loc[schedule["Week"] == last_week, ["Home Team", "Away Team"]]

st.header("Admin Tool")


st.subheader("Bets Eingabe")

with st.form("Tipps"):

    cola, colb = st.columns([1,2])
    with cola:
        player = st.selectbox("Spieler auswählen", player_list)
    with colb:
        bets_list = st.text_input("Tipps eingeben")
        bets_list = bets_list.replace("[", "").replace("'", "").replace("]\n", "")
        bets_list = bets_list.split(",")

    bets_submit = st.form_submit_button("Tipps erfassen")

if bets_submit:
    bets_input(week_nr=1, player=player, bets=bets_list)


st.dataframe(pd.read_csv("data/bets_2024.csv"))


st.subheader("Ergebnis Eingeben")



with st.form("Score"):
    col1, col2 = st.columns(2)
    score_home_list = []
    score_away_list = []
    for h_team, a_team in zip(filtered_DF["Home Team"], filtered_DF["Away Team"]):
        score_home = col1.number_input(f"{h_team}", value=0)
        score_home_list.append(score_home)
        score_away = col2.number_input(f"{a_team}", value=0)
        score_away_list.append(score_away)
    
    submitted = st.form_submit_button("Submit")

if submitted:
    schedule.loc[schedule["Week"] == last_week, "Score Home"] = score_home_list
    schedule.loc[schedule["Week"] == last_week, "Score Guest"] = score_away_list
    st.dataframe(filtered_DF)
    st.dataframe(schedule)