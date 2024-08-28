import pandas as pd

def calc_score(row): # check if player guessed correctly
    if row[player] == row["Winner"]:
        return 1
    else:
        return 0

# player List of all participants and list of all teams
player_list = ["Alex", "Alina", "Evelyn", "Christopher", "Ludwig", "Manu", "Natalie", "Nikolai", "Sebastian", "Vero", "Viki", "Wolfgang"]
# player_list_with_MrMedian = player_list.copy()
# player_list_with_MrMedian.append("Mr.Median")

# Load Data
# betsDF = pd.read_csv("data/bets.csv", delimiter=";")
# betsDF["Date"] = pd.to_datetime(betsDF["Date"], format="%d.%m.%Y %H:%M")
# betsDF["Winner"] = betsDF.apply(check_winner, axis=1)

schedule = pd.read_csv("data/schedule.csv", delimiter=";")
schedule["Date"] = pd.to_datetime(schedule["Date"], format="%Y.%m.%d %H:%M")

team_list = schedule["Home Team"].unique()

resultsDF = pd.read_csv("data/results.csv")
betsDF = pd.read_csv("data/bets_2024.csv")

scoringDF = pd.DataFrame(columns=player_list) # collect the points for each game
scoringDF[["Week", "Game Nr."]] = schedule[["Week", "Game Nr."]]
scoringDF["Winner"] = resultsDF["Winner"]
for player in player_list:
    scoringDF[f"bet_{player}"] = betsDF[player]
    scoringDF[player] = scoringDF.apply(calc_score, axis=1)

scoringDF[["Winner", "Alex", "Evelyn", "bet_Alex", "bet_Evelyn"]].head(20)

# schedule["Score Home"] = 0
# schedule["Score Guest"] = 0
# schedule["Winner"] = schedule.apply(check_winner, axis=1)

playoff_teams_DF = pd.read_csv("data/playoffTipps.csv", delimiter=";")

# # create additional Dataframes
playerDF = pd.DataFrame(data={"Spieler":player_list}) # sums up 


# my_bets = pd.DataFrame(columns=player_list)
# my_bets = pd.concat([schedule, my_bets], axis=1)

# for player in player_list:
#     scoringDF[player] = betsDF.apply(calc_score, axis=1)
