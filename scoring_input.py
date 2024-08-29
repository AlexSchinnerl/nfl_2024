import streamlit as st
import pandas as pd
from functions_load_and_transform import schedule, player_list, team_list

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
    
def bets_input(week_nr, player, bets):
    df = pd.read_csv("data/bets_2024.csv")
    df.loc[df["Week"] == week_nr, player] = bets
    df.to_csv("data/bets_2024.csv", index=False)

def score_input(week_nr, home_team_list, away_team_list):
    df = pd.read_csv("data/results.csv")
    df.loc[df["Week"] == week_nr, "Score Home"] = home_team_list
    df.loc[df["Week"] == week_nr, "Score Guest"] = away_team_list
    df.loc[df["Week"] == week_nr, "Winner"] = df.apply(check_winner, axis=1)
    df.to_csv("data/results.csv", index=False)

def calc_scoring_csv():
    betsDF = pd.read_csv("data/bets_2024.csv")
    resultsDF = pd.read_csv("data/results.csv")
    scoringDF = pd.concat([betsDF[player_list], resultsDF[["Winner", "Week", "Game Nr."]]], axis=1)
    for player in player_list:
        # scoringDF[f"score_{player}"] = scoringDF.apply(lambda row: 1 if row[player] == row["Winner"] else 0, axis=1)
        scoringDF[f"score_{player}"] = scoringDF.apply(lambda row: 1 if row[player] == row["Winner"] else 0, axis=1)

    scoringDF.to_csv("data/scoring.csv", index=False)

def team_score_counter(row, teams_dict):
    if not row["Winner"] == "0":
        teams_dict[row["Home Team"]][3] +=1
        teams_dict[row["Away Team"]][3] +=1
        if row["Winner"] == "Draw":
            teams_dict[row["Home Team"]][1] +=1
            teams_dict[row["Away Team"]][1] +=1
        else:
            if row["Winner"] == row["Home Team"]:
                teams_dict[row["Home Team"]][0] +=1
                teams_dict[row["Away Team"]][2] +=1
            else:
                teams_dict[row["Away Team"]][0] +=1
                teams_dict[row["Home Team"]][2] +=1

def get_team_scoring():
    df = pd.read_csv("data/results.csv")
    teams_dict = {}
    for team in team_list:
        teams_dict[team] = [0, 0, 0, 0] # Wins, Draws, Losses, Games Played
    df.apply(team_score_counter, teams_dict=teams_dict, axis=1)
    return teams_dict

st.header("Admin Tool")
st.subheader("Bets Eingabe")
week_nr_tipps = st.number_input("Spielwoche:", value=0, key="Spielwoche_bets")
with st.form("Tipps", clear_on_submit=True):
    cola, colb = st.columns([1,2])
    with cola:
        player = st.selectbox("Spieler auswählen", player_list, index=None, placeholder="Pick one")
    with colb:
        bets_list = st.text_input("Tipps eingeben", placeholder="Liste aus der Mail kopieren")
        bets_list = bets_list.replace("[", "").replace("'", "").replace("]", "").replace("\n", "")
        bets_list = [x.strip() for x in bets_list.split(",")]

    bets_submit = st.form_submit_button("Tipps erfassen")

if bets_submit:
    bets_input(week_nr=week_nr_tipps, player=player, bets=bets_list)
    st.dataframe(pd.read_csv("data/bets_2024.csv"))


st.subheader("Ergebnis Eingeben")
week_nr_score = st.number_input("Spielwoche:", value=0)    
with st.form("Score", clear_on_submit=True):
    col1, col2 = st.columns(2)
    score_home_list = []
    score_away_list = []
    filtered_DF = schedule.loc[schedule["Week"] == week_nr_score, ["Home Team", "Away Team"]]
    for h_team, a_team in zip(filtered_DF["Home Team"], filtered_DF["Away Team"]):
        score_home = col1.number_input(f"{h_team}", value=0)
        score_home_list.append(score_home)
        score_away = col2.number_input(f"{a_team}", value=0)
        score_away_list.append(score_away)
    
    score_submit = st.form_submit_button("Submit")

if score_submit:
    score_input(week_nr=week_nr_score, home_team_list=score_home_list, away_team_list=score_away_list)
    calc_scoring_csv()
    teams_dict = get_team_scoring()
    team_scores_DF = pd.DataFrame.from_dict(teams_dict, orient="index", columns=["Wins", "Draws", "Losses", "Games Played"])
    team_scores_DF["Team"] = team_scores_DF.index
    team_scores_DF.to_csv("data/teams_scores.csv", index=False)

    st.dataframe(pd.read_csv("data/scoring.csv"))
    st.dataframe(pd.read_csv("data/results.csv"))