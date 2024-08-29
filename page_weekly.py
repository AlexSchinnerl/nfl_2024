import streamlit as st
from datetime import datetime
from functions_load_and_transform import schedule, team_scores_DF, resultsDF
from functions_form import name_submit, send_form

thisDay = datetime.today().strftime("%Y-%m-%d") # for live
# week_count = list(schedule.loc[schedule["Date"]<thisDay, "Week"])[-1]
if thisDay <= schedule.iloc[15][6].strftime("%Y-%m-%d"):
    thisWeek = 1
else:
    list(schedule.loc[schedule["Date"]<thisDay, "Week"])[-1]

# thisWeek = 2 # for testing

lastWeek = thisWeek-1

def change_home_team_name(row):
    return team_scores_DF.loc[team_scores_DF["Team"] == row["Home Team"], "Teams (w-d-l)"].values[0]

def change_away_team_name(row):
    return team_scores_DF.loc[team_scores_DF["Team"] == row["Away Team"], "Teams (w-d-l)"].values[0]

thisWeek_DF = schedule.loc[schedule["Week"]==thisWeek, ["Game Nr.", "Date", "Home Team", "Away Team", "Location"]]
thisWeek_DF["Home Team"] = thisWeek_DF.apply(change_home_team_name, axis=1)
thisWeek_DF["Away Team"] = thisWeek_DF.apply(change_away_team_name, axis=1)


lastWeek_DF = resultsDF.loc[resultsDF["Week"]==lastWeek, ["Game Nr.", "Home Team", "Score Home", "Score Guest", "Away Team"]]



st.header("Wöchentliche Tipps")

colA, colB = st.columns([2,1])
with colA:
    if thisWeek == 1:
        pass
    else:
        st.subheader(f"Ergebnisse für Woche {lastWeek}")
        st.dataframe(lastWeek_DF, hide_index=True, height=600)

    st.subheader(f"Spielplan für Woche {thisWeek}")
    st.dataframe(thisWeek_DF, hide_index=True, height=600)

with colB:
    st.subheader("Hier Tipps auswählen")
    with st.form("Place Bet"):
        selected_teams = []
        for pairing in zip(thisWeek_DF["Home Team"], thisWeek_DF["Away Team"], thisWeek_DF["Game Nr."]):
            chosen_winner = st.selectbox(
                label=f"Game Nr.: {pairing[2]} {pairing[0]} vs. {pairing[1]}", 
                options=pairing[0:2], 
                index=None, 
                placeholder="Bitte Gewinner auswählen"
                )
            selected_teams.append(chosen_winner)
        player_name, weekly_submitted = name_submit("Tipps absenden")
    if weekly_submitted:
        selected_teams.append(player_name)
        send_form(mailText=selected_teams[:-1], subject=f"bets_{selected_teams[-1]}_week_{thisWeek}")