import pandas as pd

# Helper functions to apply on the different DFs
# Most of them use a player variable, which will come from a loop through all players

# def check_winner(row): # winner column in game Data
#     if row["Score Home"] > row["Score Guest"]:
#         return row["Home Team"]
#     else:
#         return row["Away Team"]
    
def check_winner(row): # winner column in game Data
    if row["Score Home"] > row["Score Guest"]:
        return 1
    else:
        return 2

def calc_score(row): # check if player guessed correctly
    if row[player] == row["Winner"]:
        return 1
    else:
        return 0

# Load Data
betsDF = pd.read_csv("data/bets.csv", delimiter=";")
betsDF["Date"] = pd.to_datetime(betsDF["Date"], format="%d.%m.%Y %H:%M")
betsDF["Winner"] = betsDF.apply(check_winner, axis=1)

schedule = pd.read_csv("data/schedule.csv", delimiter=";")
schedule["Date"] = pd.to_datetime(schedule["Date"], format="%Y.%m.%d %H:%M")
schedule["Score Home"] = 0
schedule["Score Guest"] = 0
schedule["Winner"] = schedule.apply(check_winner, axis=1)

playoff_teams_DF = pd.read_csv("data/playoffTipps.csv", delimiter=";")

# player List of all participants and list of all teams
player_list = ["Alex", "Alina", "Evelyn", "Christopher", "Ludwig", "Manu", "Natalie", "Nikolai", "Sebastian", "Vero", "Viki", "Wolfgang"]
# player_list_with_MrMedian = player_list.copy()
# player_list_with_MrMedian.append("Mr.Median")
team_list = schedule["Home Team"].unique()

# # create additional Dataframes
playerDF = pd.DataFrame(data={"Spieler":player_list}) # sums up 


scoringDF = pd.DataFrame(columns=player_list) # collect the points for each game
scoringDF["Week"] = schedule["Week"]

my_bets = pd.DataFrame(columns=player_list)
my_bets = pd.concat([schedule, my_bets], axis=1)

for player in player_list:
    scoringDF[player] = betsDF.apply(calc_score, axis=1)
