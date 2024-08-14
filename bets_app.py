import streamlit as st
import pandas as pd
from datetime import datetime
from load_and_transform import schedule, betsDF, player_list, scoringDF, playerDF, team_list

st.set_page_config(layout="wide")
# st.set_page_config(runOnSave = True)

thisDay = datetime.today().strftime("%Y-%m-%d")
thisDay = datetime(2024, 9, 6)
st.write(thisDay)

# betsDF = pd.read_csv("season_2024/data/bets.csv", delimiter=";")
filtered_bets = schedule.loc[schedule["Date"]<thisDay].copy()
thisWeek = list(schedule.loc[schedule["Date"]<thisDay, "Week"])[-1]
thisWeek = 1
st.write(thisWeek)
lastWeek = thisWeek-1

# player_list = ["Alex", "Alina", "Evelyn", "Christopher", "Ludwig", "Manu", "Natalie", "Nikolai", "Sebastian", "Vero", "Viki", "Wolfgang"]
# team_list = betsDF["Home Team"].unique()


# scoringDF["Week Count"] = filtered_bets["Week"]




# # Transform Dataframes
# filtered_bets["Winner"] = filtered_bets.apply(check_winner, axis=1)
thisWeek_DF = schedule.loc[schedule["Week"]==thisWeek, ["Game Nr.", "Date", "Location", "Home Team", "Away Team"]]
lastWeek_DF = betsDF.loc[betsDF["Round Number"]==lastWeek, ["Game Nr.", "Home Team", "Score Home", "Score Guest", "Away Team"]]

st.header("NFL Tippspiel 2024")

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
    with st.form("place Bet"):
        st.subheader("Hier Gewinner auswählen")
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
    with open(f"submitted_bets/{selected_teams[-1]}_week_{thisWeek}_{datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')}.txt", "w") as f:
        for team in selected_teams[:-1]:
            f.write(f"{team},")
    st.write(selected_teams)
    weekly_bets_DF = pd.read_csv(f"data/bets_week{thisWeek}.csv")
    weekly_bets_DF[f"{selected_teams[-1]}"] = selected_teams[:-1]
    weekly_bets_DF.to_csv(f"data/bets_week{thisWeek}.csv")
    st.dataframe(weekly_bets_DF)



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




st.subheader("Zwischenstand")
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
