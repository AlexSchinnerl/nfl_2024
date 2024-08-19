import streamlit as st
import pandas as pd
from datetime import datetime
from load_and_transform import schedule, my_bets, playoff_teams_DF, player_list, scoringDF, playerDF, team_list
from mail_function import send_mail_function


def send_form(mailText, subject):
    try:
        send_mail_function(mail_key=MYKEY, mailText=mailText, subject=subject)
        st.success("Tipps abgeschickt!")
    except Exception:
        st.error("Fehler beim Übermitteln")

def name_submit(button_description):
    col1a, col1b = st.columns(2)
    with col1a:
        player_name = st.text_input("Name eingeben")
    with col1b:
        st.write("\n")
        st.write("\n")
        submitted = st.form_submit_button(button_description)
    return player_name, submitted

def playoff_checkboxes(df):
    for subdivision in sorted(df["Subdivision"].unique()):
        st.write(f"{subdivision}")
        for team in df.loc[df["Subdivision"]==subdivision, "Teams"]:
            check_team = st.checkbox(label=team, value=False)
            if check_team:
                selected_playoff_teams.append(team)

st.set_page_config(layout="wide")
# st.set_page_config(runOnSave = True)

# import keyring
# MYKEY = keyring.get_password("alxMail", "alex")
MYKEY = st.secrets["my_key"]

# thisDay = datetime.today().strftime("%Y-%m-%d") # for live
thisDay = datetime(2024, 9, 6)

# betsDF = pd.read_csv("season_2024/data/bets.csv", delimiter=";")
filtered_bets = schedule.loc[schedule["Date"]<thisDay].copy()
thisWeek = list(schedule.loc[schedule["Date"]<thisDay, "Week"])[-1]
thisWeek = 1
lastWeek = thisWeek-1

# # Transform Dataframes
# filtered_bets["Winner"] = filtered_bets.apply(check_winner, axis=1)
thisWeek_DF = schedule.loc[schedule["Week"]==thisWeek, ["Game Nr.", "Date", "Location", "Home Team", "Away Team"]]
lastWeek_DF = my_bets.loc[my_bets["Week"]==lastWeek, ["Game Nr.", "Home Team", "Score Home", "Score Guest", "Away Team"]]
afc_DF = playoff_teams_DF.loc[playoff_teams_DF["Division"]=="AFC"]
nfc_DF = playoff_teams_DF.loc[playoff_teams_DF["Division"]=="NFC"]

st.title("NFL Tippspiel 2024")

st.header("Vorab Tipps")

superbowl, playoff = st.columns(2)
with superbowl:
    st.subheader("Superbowl Vorab Tipp")
    with st.form("Place Superbowl Bet"):
        superbowl_bet = st.selectbox(label="Superbowl Tipp abgeben", options=team_list, index=None, placeholder="Hier Superbowl Sieger auswählen")
        player_name, superbowl_submitted = name_submit("Superbowl Tipp absenden")
    if superbowl_submitted:
        send_form(mailText=f"{player_name}: {superbowl_bet}", subject=f"Superbowl_vorab_{player_name}")

with playoff:
    st.subheader("Playoff Vorab Tipp")
    with st.form("Place Playoff Bet"):
        col1, col2 = st.columns(2)
        selected_playoff_teams = []
        with col1:
            st.subheader("AFC Playof Teams")
            playoff_checkboxes(afc_DF)
        with col2:
            st.subheader("NFC Playoff Teams")
            playoff_checkboxes(nfc_DF)
        player_name, playoff_submitted = name_submit("Playoff Tipps absenden")      
    if playoff_submitted:
        send_form(mailText=f"{player_name}: {selected_playoff_teams}", subject=f"Playoff_vorab_{player_name}")


st.header("Wöchentliche Tipps")

colA, colB = st.columns(2)
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

        
    # my_bets.loc[my_bets["Week"]==thisWeek, f"{selected_teams[-1]}"] = selected_teams[:-1]
    # my_bets.to_csv(f"data/betsDF.csv", index=False)
    # st.dataframe(my_bets)


    

# placed_bets = []

# for player in player_list:
#     placed_bets.append(filtered_bets[player].value_counts().sum())
#     scoringDF[player] = filtered_bets.apply(calc_score, axis=1)

# playerDF["Gesamtpunkte"] = scoringDF[player_list].sum().to_list()
# playerDF["Last Week"] = scoringDF.loc[scoringDF["Week Count"]<=lastWeek, player_list].sum().to_list()
# playerDF["Zuwachs"] = playerDF["Gesamtpunkte"]-playerDF["Last Week"]

# st.dataframe(scoringDF.loc[scoringDF["Week Count"]<=lastWeek])



# gameCount = filtered_bets["Match Number"].max()
# playerCount = len(player_list)

# # st.write(f"Bisher absolvierte Spiele: {filtered_bets['Match Number'].max()}")




st.header("Zwischenstand")
# col1, col2 = st.columns(2)
# with col1:
#     st.dataframe(playerDF.sort_values(by="Gesamtpunkte", ascending=False, ignore_index=True))
# with col2:
#     st.bar_chart(data=playerDF, x="Player", y=["Gesamtpunkte", "Last Week"]) #, stack=False

# weekly_groupedDF = scoringDF.groupby("Week Count", as_index=False).sum()




# col1, col2 = st.columns(2)

# with col1:
#     st.subheader(f"Spielplan für Woche {thisWeek}")
#     st.dataframe(thisWeek_DF, hide_index=True)
# with col2:
#     st.subheader(f"Ergebnisse für Woche {lastWeek}")
#     st.dataframe(lastWeek_DF, hide_index=True)


# st.data_editor(
#     thisWeek_DF,
#     column_config={
#         "Tipp": st.column_config.SelectboxColumn(
#             "Tipp",
#             help="Place Bets",
#             width="medium",
#             options=[["Team A", "Team B"]]
#         )
#     },
#     hide_index=True,
# )
