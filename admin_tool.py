import streamlit as st
import pandas as pd
import re
from functions_load_and_transform import schedule, player_list, team_list, thisWeek, thisWeek_DF, lastWeek, lastWeek_DF
from admin_send_mail import send_weekly_mail

html = f"""\
<!DOCTYPE html>
<html lang="de">
  <body>
  <h2>Link zur Übersicht:</h2>
  <br>
  <a href="https://nfl2024-tippspiel.streamlit.app/standing">https://nfl2024-tippspiel.streamlit.app/standing</a> 
  <br>
  <br>
  <h2>Ergebnisse der Woche {lastWeek}:</h2>
  <br>
  {lastWeek_DF.to_html(index=False)}
  <br>
  <br>
  <h2>Tabelle für Woche {thisWeek}:</h2>
  <br>
  {thisWeek_DF.to_html(index=False)}
  </body>
</html>
"""

def check_winner(row): # winner column in game Data
    if row["Score Home"] == 0 and row["Score Guest"] == 0:
        return 0
    else:
        if row["Score Home"] > row["Score Guest"]:
            return row["Home Team"]
        elif row["Score Home"] < row["Score Guest"]:
            return row["Away Team"]
        else:
            return "Draw"

def check_looser(row):
    if row["Score Home"] == 0 and row["Score Guest"] == 0:
        return 0
    else:
        if row["Score Home"] > row["Score Guest"]:
            return row["Away Team"]
        elif row["Score Home"] < row["Score Guest"]:
            return row["Home Team"]
        else:
            return "Draw"
            
def calculate_w_d_l():
    team_scores_DF = pd.read_csv("data/teams.csv")
    results_DF = pd.read_csv("data/results.csv")

    count_draws = dict(zip(team_list, [0]*len(team_list)))
    draw_dict = results_DF.loc[results_DF["Winner"]=="Draw", ["Home Team", "Away Team"]].value_counts().to_dict()

    for team in draw_dict:
        count_draws[team[0]] += 1
        count_draws[team[1]] += 1

    for team in team_list:
        if team in list(results_DF.loc[results_DF["Winner"]==team, "Winner"]):
            team_scores_DF.loc[team_scores_DF["Team"]==team, "Wins"] = results_DF.loc[results_DF["Winner"]==team, "Winner"].value_counts()[0]
        if team in list(results_DF.loc[results_DF["Looser"]==team, "Looser"]):
            team_scores_DF.loc[team_scores_DF["Team"]==team, "Losses"] = results_DF.loc[results_DF["Looser"]==team, "Looser"].value_counts()[0]
        team_scores_DF.loc[team_scores_DF["Team"]==team, "Draws"] = count_draws[team]
    
    team_scores_DF["Games Played"] = team_scores_DF["Wins"]+team_scores_DF["Draws"]+team_scores_DF["Losses"]

    team_scores_DF.to_csv("data/teams.csv", index=False)
    # return team_scores_DF

def bets_input(week_nr, player, bets):
    df = pd.read_csv("data/bets_2024.csv")
    df.loc[df["Week"] == week_nr, player] = bets
    df.to_csv("data/bets_2024.csv", index=False)

def po_input(player, bets):
    df = pd.read_csv("data/playoffBets.csv")
    df[player] = bets
    df.to_csv("data/playoffBets.csv", index=False)

def score_input(week_nr, home_team_list, away_team_list):
    df = pd.read_csv("data/results.csv")
    df.loc[df["Week"] == week_nr, "Score Home"] = home_team_list
    df.loc[df["Week"] == week_nr, "Score Guest"] = away_team_list
    df.loc[df["Week"] == week_nr, "Winner"] = df.apply(check_winner, axis=1)
    df.loc[df["Week"] == week_nr, "Looser"] = df.apply(check_looser, axis=1)
    df.to_csv("data/results.csv", index=False)

def calc_scoring_csv():
    betsDF = pd.read_csv("data/bets_2024.csv")
    resultsDF = pd.read_csv("data/results.csv")
    scoringDF = pd.concat([betsDF[player_list], resultsDF[["Winner", "Week", "Game Nr."]]], axis=1)
    for player in player_list:
        # scoringDF[f"score_{player}"] = scoringDF.apply(lambda row: 1 if row[player] == row["Winner"] else 0, axis=1)
        scoringDF[f"score_{player}"] = scoringDF.apply(lambda row: 1 if row[player] == row["Winner"] else 0, axis=1)

    scoringDF.to_csv("data/scoring.csv", index=False)

st.set_page_config(
    layout="wide"
    )


st.title("Admin Tool")

with st.sidebar:
    week_nr = st.number_input("Spielwoche:", value=0, key="Spielwoche_bets")
    st.subheader("Email verschicken")
    send_email = st.button("Send Email", help="Email mit Ergebnissen und Spielplan verschicken")
    if send_email:
        try:
            send_weekly_mail(html_text=html, lastWeek=lastWeek, thisWeek=thisWeek)
            st.success("Mail abgeschickt!")
        except Exception:
            st.error("Fehler beim Übermitteln")
        

betsInput, scoreInput = st.columns([1,1])
with betsInput:
    st.subheader("Bets Eingabe")
    st.write(f"Eingabe für Woche: {week_nr}")
    # week_nr_tipps = st.number_input("Spielwoche:", value=0, key="Spielwoche_bets")
    with st.form("Tipps", clear_on_submit=True):
        cola, colb = st.columns([1,2])
        with cola:
            player = st.selectbox("Spieler auswählen", player_list, index=None, placeholder="Pick one")
        with colb:
            bets_list = st.text_input("Tipps eingeben", placeholder="Liste aus der Mail kopieren")
            bets_list = bets_list.replace("[", "").replace("'", "").replace("]", "").replace("\n", "")
            bets_list = re.sub(" \(\d-\d-\d\)", "", bets_list)
            bets_list = [x.strip() for x in bets_list.split(",")]

        bets_submit = st.form_submit_button("Tipps erfassen")

    if bets_submit:
        # bets_input(week_nr=week_nr_tipps, player=player, bets=bets_list)
        bets_input(week_nr=week_nr, player=player, bets=bets_list)
        st.dataframe(pd.read_csv("data/bets_2024.csv"))
    
    st.subheader("Playoff vorab Input")
    st.write("Vorab Tipps eingeben")
    with st.form("Playoff Vorab", clear_on_submit=True):
        cola1, colb1 = st.columns([1,2])
        with cola1:
            player = st.selectbox("Spieler auswählen", player_list, index=None, placeholder="Pick one", key="Player_PO_vorab")
        with colb1:
            po_list = st.text_input("Playoff Tipps eingeben", placeholder="Liste aus der Mail kopieren")
            po_list = po_list.replace("[", "").replace("'", "").replace("]", "").replace("\n", "")
            # po_list = re.sub(" \(\d-\d-\d\)", "", po_list)
            po_list = [x.strip() for x in po_list.split(",")]

        playoff_submit = st.form_submit_button("Playoff Tipps erfassen")

    if playoff_submit:
        po_input(player=player, bets=po_list)
        st.dataframe(pd.read_csv("data/playoffBets.csv"))


with scoreInput:
    st.subheader("Ergebnis Eingeben")
    st.write(f"Eingabe für Woche: {week_nr}")
    with st.form("Score", clear_on_submit=True):
        col1, col2 = st.columns(2)
        score_home_list = []
        score_away_list = []
        # filtered_DF = schedule.loc[schedule["Week"] == week_nr_score, ["Home Team", "Away Team"]]
        filtered_DF = schedule.loc[schedule["Week"] == week_nr, ["Home Team", "Away Team"]]
        for h_team, a_team in zip(filtered_DF["Home Team"], filtered_DF["Away Team"]):
            score_home = col1.number_input(f"{h_team}", value=0)
            score_home_list.append(score_home)
            score_away = col2.number_input(f"{a_team}", value=0)
            score_away_list.append(score_away)
        
        score_submit = st.form_submit_button("Submit")

    if score_submit:
        # score_input(week_nr=week_nr_score, home_team_list=score_home_list, away_team_list=score_away_list)
        score_input(week_nr=week_nr, home_team_list=score_home_list, away_team_list=score_away_list)
        calc_scoring_csv()
        calculate_w_d_l()
        st.dataframe(pd.read_csv("data/scoring.csv"))
        st.dataframe(pd.read_csv("data/results.csv"))
        st.dataframe(pd.read_csv("data/teams.csv"))