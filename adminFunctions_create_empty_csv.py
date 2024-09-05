import pandas as pd
from functions_load_and_transform import player_list, schedule, team_list

def create_empty_bets_csv():
    betsDF = pd.DataFrame(columns=player_list)
    betsDF[["Week", "Game Nr."]] = schedule[["Week", "Game Nr."]]
    betsDF.to_csv("data/bets_2024.csv", index=False)

def create_empty_results_csv():
    resultsDF = schedule[["Week", "Game Nr.", "Home Team", "Away Team"]].copy()
    resultsDF[["Score Home", "Score Guest", "Winner", "Looser"]] = 0
    resultsDF.to_csv("data/results.csv", index=False)

def clear_teams_csv():
    team_scores_DF = pd.read_csv("data/teams.csv")
    team_scores_DF[["Wins", "Draws", "Losses", "Games Played"]] = 0
    team_scores_DF.to_csv("data/teams.csv", index=False)

def create_empty_po_csv():
    po_DF = pd.DataFrame(columns=player_list)
    po_DF["PO Participant"] = 0
    po_DF.to_csv("data/playoffBets.csv", index=False)
      
# create_empty_bets_csv()
# create_empty_results_csv()
# clear_teams_csv()
# create_empty_po_csv()