import streamlit as st
# import pandas as pd
from datetime import datetime
from load_and_transform import betsDF, player_list, scoringDF, playerDF, team_list

st.set_page_config(layout="wide")
# st.set_page_config(runOnSave = True)

# def check_winner(row): # winner column in game Data
#     if row["Score Home"] > row["Score Guest"]:
#         return 1
#     else:
#         return 2
# def calc_score(row): # check if player guessed correctly
#     if row[player] == row["Winner"]:
#         return 1
#     else:
#         return 0

thisDay = datetime.today().strftime("%Y-%m-%d")
thisDay = "2023-10-13"
st.write(thisDay)

# betsDF = pd.read_csv("season_2024/data/bets.csv", delimiter=";")
filtered_bets = betsDF.loc[betsDF["Date"]<thisDay].copy()
thisWeek = filtered_bets["Round Number"].max()
lastWeek = thisWeek-1

# player_list = ["Alex", "Alina", "Evelyn", "Christopher", "Ludwig", "Manu", "Natalie", "Nikolai", "Sebastian", "Vero", "Viki", "Wolfgang"]
# team_list = betsDF["Home Team"].unique()


scoringDF["Week Count"] = filtered_bets["Round Number"]




# # Transform Dataframes
# filtered_bets["Winner"] = filtered_bets.apply(check_winner, axis=1)
thisWeek_DF = filtered_bets.loc[filtered_bets["Round Number"]==thisWeek, ["Game Nr.", "Date", "Location", "Home Team", "Away Team"]]
lastWeek_DF = filtered_bets.loc[filtered_bets["Round Number"]==lastWeek, ["Game Nr.", "Home Team", "Score Home", "Score Guest", "Away Team"]]
# thisWeek_DF["Tipp"] = ""

st.header("NFL Tippspiel 2024")

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

colA, colB = st.columns(2)

with colA:
    st.subheader(f"Ergebnisse für Woche {lastWeek}")
    st.dataframe(lastWeek_DF, hide_index=True, height=600)

    st.subheader(f"Spielplan für Woche {thisWeek}")
    st.dataframe(thisWeek_DF, hide_index=True, height=600)


with colB:
    with st.form("place Bet"):
        st.subheader("Hier Gewinner auswählen")
        # col1, col2 = st.columns(2)
        # with col1:
        selected_teams = []
        for pairing in zip(thisWeek_DF["Home Team"], thisWeek_DF["Away Team"], thisWeek_DF["Game Nr."]):
            chosen_winner = st.selectbox(label=f"Game Nr.: {pairing[2]} {pairing[0]} vs. {pairing[1]}", options=pairing[0:2])
            selected_teams.append(chosen_winner)
        col1a, col1b = st.columns(2)
        with col1a:
            player_name = st.text_input("Name eingeben")
        with col1b:
            st.write("\n")
            st.write("\n")
            submitted = st.form_submit_button("Tipps absenden")
        if submitted:
            selected_teams.append(player_name)
            st.write(selected_teams)

# st.write(selected_teams)

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




# st.subheader("Zwischenstand")
# col1, col2 = st.columns(2)
# with col1:
#     st.dataframe(playerDF.sort_values(by="Gesamtpunkte", ascending=False, ignore_index=True))
# with col2:
#     st.bar_chart(data=playerDF, x="Player", y=["Gesamtpunkte", "Last Week"]) #, stack=False

# weekly_groupedDF = scoringDF.groupby("Week Count", as_index=False).sum()