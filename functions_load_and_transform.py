import pandas as pd

# player List of all participants and list of all teams
player_list = ["Alex", "Alina", "Evelyn", "Christopher", "Ludwig", "Manu", "Natalie", "Nikolai", "Sebastian", "Vero", "Viki", "Wolfgang"]
# player_list_with_MrMedian = player_list.copy()
# player_list_with_MrMedian.append("Mr.Median")

# Load Data
schedule = pd.read_csv("data/schedule.csv", delimiter=";")
schedule["Date"] = pd.to_datetime(schedule["Date"], format="%Y.%m.%d %H:%M")

team_list = schedule["Home Team"].unique()

resultsDF = pd.read_csv("data/results.csv")
betsDF = pd.read_csv("data/bets_2024.csv")
scoringDF = pd.read_csv("data/scoring.csv")
scoringDF = scoringDF.drop(player_list, axis=1)
for player in player_list:
    scoringDF = scoringDF.rename(columns={f"score_{player}":player})

team_scores_DF = pd.read_csv("data/teams_scores.csv")
team_scores_DF["w-d-l"] = "(" + team_scores_DF["Wins"].astype((str)) + "-" + team_scores_DF["Draws"].astype((str)) + "-" + team_scores_DF["Losses"].astype((str)) + ")"
team_scores_DF["Teams (w-d-l)"] = team_scores_DF["Team"] + " " + team_scores_DF["w-d-l"]

# playoff_teams_DF = pd.read_csv("data/playoffTipps.csv", delimiter=";")

# # create additional Dataframes
playerDF = pd.DataFrame(data={"Spieler":player_list}) # sums up 


# my_bets = pd.DataFrame(columns=player_list)
# my_bets = pd.concat([schedule, my_bets], axis=1)

# for player in player_list:
#     scoringDF[player] = betsDF.apply(calc_score, axis=1)
