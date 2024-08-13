import pandas as pd

# Helper functions to apply on the different DFs
# Most of them use a player variable, which will come from a loop through all players
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
# 2 Functions for the extra points
def calc_playoffPoints(row):
    if row[player] == row["Playoff Team"]:
        return 2
    else:
        return 0
def calc_SuperbowlPoints(row):
    if row[player] == row["Superbowl"]:
        return 10
    else:
        return 0
# checks who won the Week
def check_weeklyWinner(row):
    if row[player] == row["maxPoints"]:
        return 1
    else:
        return 0
# 3 Functions for Team evaluation
def lucky_team(row):
    if row[player] == row["Winner"]:
        if row["Winner"] == 1: 
            return row["Home Team"]
        else:
            return row["Away Team"]
def unlucky_team(row):
    if row[player] != row["Winner"]:
        if row["Winner"] == 1: 
            return row["Away Team"]
        else:
            return row["Home Team"]
def teamCount_per_player(row):
    if row[player] == 1:
        return row["Home Team"]
    else:
        return row["Away Team"]

# Load Data
betsDF = pd.read_csv("season_2024/data/bets.csv", delimiter=";")
betsDF["Date"] = pd.to_datetime(betsDF["Date"], format="%d.%m.%Y %H:%M")
playoffDF = pd.read_csv("season_2024/data/playoffTipps.csv", delimiter=";")
superbowlDF = pd.read_csv("season_2024/data/superbowl.csv", delimiter=";")
# player List of all participants and list of all teams
player_list = ["Alex", "Alina", "Evelyn", "Christopher", "Ludwig", "Manu", "Natalie", "Nikolai", "Sebastian", "Vero", "Viki", "Wolfgang"]
player_list_with_MrMedian = player_list.copy()
player_list_with_MrMedian.append("Mr.Median")
team_list = betsDF["Home Team"].unique()

# create additional Dataframes
playerDF = pd.DataFrame(data={"Player":player_list}) # sums up 
scoringDF = pd.DataFrame(columns=player_list) # collect the points for each game
scoringDF["Week Count"] = betsDF["Round Number"]
playoffScoresDF = pd.DataFrame(columns=player_list) # playoff pre-bets
playoffScoresDF["Teams"] = playoffDF["Teams"]
playoffScoresDF["Division"] = playoffDF["Division"]

# Dataframes for Team evaluation
lucky_teamDF = pd.DataFrame(columns=player_list)
unlucky_teamDF = pd.DataFrame(columns=player_list)
bets_per_teamDF = pd.DataFrame(columns=player_list)

# Transform Dataframes
betsDF["Winner"] = betsDF.apply(check_winner, axis=1)

placed_bets = []
playoff_scores = []
superbowl_scores = []

for player in player_list:
    placed_bets.append(betsDF[player].value_counts().sum())
    scoringDF[player] = betsDF.apply(calc_score, axis=1)
    playoffScoresDF[f"{player}"] = playoffDF.apply(calc_playoffPoints, axis=1)
    playoff_scores.append(playoffScoresDF[f"{player}"].sum())
    superbowl_scores.append(superbowlDF.apply(calc_SuperbowlPoints, axis=1)[0])
    
    lucky_teamDF[player] = betsDF.apply(lucky_team, axis=1)
    unlucky_teamDF[player] = betsDF.apply(unlucky_team, axis=1)
    bets_per_teamDF[player] = betsDF.apply(teamCount_per_player, axis=1)

playoff_scores.extend(["Playoff Score"])
superbowl_scores.extend(["Superbowl Score"])
scoringDF.loc[max(scoringDF.index)+1] = playoff_scores
scoringDF.loc[max(scoringDF.index)+1] = superbowl_scores
playerDF["Gesamtpunkte"] = scoringDF[player_list].sum().to_list()
playerDF["Punkte Regular Season"] = scoringDF[player_list][:-15].sum().to_list() # Regular Season
playerDF["Playoff Punkte"] = [scoringDF[player_list][-15:-3].sum().to_list()[i]
                              + scoringDF[player_list].iloc[[-2]].sum().to_list()[i]
                              for i in range(12)]  # Playoffs inklusive Vorab Tipp
playerDF["Superbowl Punkte"] = scoringDF[player_list].iloc[[-3,-1]].sum().to_list() # Superbowl inklusive Vorab Tipp
playerDF["Abgegebene Tipps"] = placed_bets

lucky_teamDF = lucky_teamDF.apply(pd.value_counts)
lucky_teamDF = lucky_teamDF.fillna(0)
unlucky_teamDF = unlucky_teamDF.apply(pd.value_counts)
unlucky_teamDF = unlucky_teamDF.fillna(0)
bets_per_teamDF = bets_per_teamDF.apply(pd.value_counts)
bets_per_teamDF = bets_per_teamDF.fillna(0)

# Group Dataframes per week
weekly_groupedDF = scoringDF.groupby("Week Count", as_index=False).sum()
weekly_groupedDF["Mr.Median"] = weekly_groupedDF[player_list].apply(lambda x: x.median(), axis=1)
weekly_groupedDF["maxPoints"] = weekly_groupedDF[player_list].apply(lambda x: x.max(), axis=1)
massimo_possibile = betsDF[["Match Number", "Round Number"]].groupby(["Round Number"], as_index=False).count()["Match Number"].to_list()
massimo_possibile.extend([28, 10])
weekly_groupedDF["Massimo Possibile"] = massimo_possibile
# split into Regular Season, Playoffs and Extra Points (Pre-Bets)
regSeasonDF = weekly_groupedDF[:-6]
playoffSeasonDF = weekly_groupedDF[18:22]
extrapointsDF = weekly_groupedDF[-2:]
# create weekly winner
weekly_winnerDF = pd.DataFrame(columns=player_list)
for player in player_list:
    weekly_winnerDF[player] = regSeasonDF.apply(check_weeklyWinner, axis=1)
# Transform Playoff Scores DF
groupedPlayoff = playoffScoresDF.groupby("Division").sum()
groupedPlayoff["Mr.Median"] = groupedPlayoff[player_list].apply(lambda x: x.median(), axis=1)
groupedPlayoff = groupedPlayoff.transpose()