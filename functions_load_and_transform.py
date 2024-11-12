import pandas as pd
from datetime import datetime

# player List of all participants and list of all teams
player_list = ["Alex", "Alina", "Evelyn", "Christopher", "Ludwig", "Manu", "Natalie", "Nikolai", "Sebastian", "Vero", "Viki", "Wolfgang"]
# player_list_with_MrMedian = player_list.copy()
# player_list_with_MrMedian.append("Mr.Median")

playoff_teams_DF = pd.read_csv("data/teams.csv", delimiter=",")
team_list = playoff_teams_DF["Team"].unique()

# Load Data
schedule = pd.read_csv("data/schedule.csv", delimiter=";")
schedule["Date"] = pd.to_datetime(schedule["Date"], format="%Y.%m.%d %H:%M")

thisDay = datetime.today().strftime("%Y-%m-%d") # for live

thisWeek = list(schedule.loc[schedule["Date"]>=thisDay, "Week"])[0]
thisWeek = 11 # for testing
lastWeek = thisWeek-1

resultsDF = pd.read_csv("data/results.csv")
betsDF = pd.read_csv("data/bets_2024.csv")
scoringDF = pd.read_csv("data/scoring.csv")
scoringDF = scoringDF.drop(player_list, axis=1)
for player in player_list:
    scoringDF = scoringDF.rename(columns={f"score_{player}":player})

team_scores_DF = pd.read_csv("data/teams.csv")
team_scores_DF["w-d-l"] = "(" + team_scores_DF["Wins"].astype((str)) + "-" + team_scores_DF["Draws"].astype((str)) + "-" + team_scores_DF["Losses"].astype((str)) + ")"
team_scores_DF["Teams (w-d-l)"] = team_scores_DF["Team"] + " " + team_scores_DF["w-d-l"]

def change_home_team_name(row):
    return team_scores_DF.loc[team_scores_DF["Team"] == row["Home Team"], "Teams (w-d-l)"].values[0]

def change_away_team_name(row):
    return team_scores_DF.loc[team_scores_DF["Team"] == row["Away Team"], "Teams (w-d-l)"].values[0]

thisWeek_DF = schedule.loc[schedule["Week"]==thisWeek, ["Game Nr.", "Date", "Home Team", "Away Team", "Location"]]
thisWeek_DF["Home Team"] = thisWeek_DF.apply(change_home_team_name, axis=1)
thisWeek_DF["Away Team"] = thisWeek_DF.apply(change_away_team_name, axis=1)


lastWeek_DF = resultsDF.loc[resultsDF["Week"]==lastWeek, ["Game Nr.", "Home Team", "Score Home", "Score Guest", "Away Team"]]
