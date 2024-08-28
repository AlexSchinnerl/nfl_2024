import pandas as pd
from functions_load_and_transform import player_list, schedule

def create_empty_bets_csv():
    betsDF = pd.DataFrame(columns=player_list)
    betsDF[["Week", "Game Nr."]] = schedule[["Week", "Game Nr."]]
    betsDF.to_csv("data/bets_2024.csv", index=False)

def create_empty_results_csv():
    resultsDF = schedule[["Week", "Game Nr.", "Home Team", "Away Team"]].copy()
    resultsDF[["Score Home", "Score Guest", "Winner"]] = 0
    resultsDF.to_csv("data/results.csv", index=False)

def create_empty_scoring_csv():
    scoringDF = pd.DataFrame(columns=player_list) # collect the points for each game
    scoringDF[["Week", "Game Nr."]] = schedule[["Week", "Game Nr."]]
    scoringDF["Winner"] = 0
    for player in player_list:
        scoringDF[f"bet_{player}"] = 0
    scoringDF.to_csv("data/scoring.csv", index=False)
    
# create_empty_bets_csv()
# create_empty_results_csv()
# create_empty_scoring_csv()