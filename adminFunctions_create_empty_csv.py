import pandas as pd
from functions_load_and_transform import player_list, schedule, team_list

def create_empty_bets_csv():
    betsDF = pd.DataFrame(columns=player_list)
    betsDF[["Week", "Game Nr."]] = schedule[["Week", "Game Nr."]]
    betsDF.to_csv("data/bets_2024.csv", index=False)

def create_empty_results_csv():
    resultsDF = schedule[["Week", "Game Nr.", "Home Team", "Away Team"]].copy()
    resultsDF[["Score Home", "Score Guest", "Winner"]] = 0
    resultsDF.to_csv("data/results.csv", index=False)

def create_empty_teams_scores_csv():
    team_scores_DF = pd.DataFrame(columns=["Wins", "Draws", "Losses", "Games Played", "Team"])
    team_scores_DF["Team"] = team_list
    team_scores_DF[["Wins", "Draws", "Losses", "Games Played"]] = 0
    team_scores_DF.to_csv("data/teams_scores.csv", index=False)

    

# def create_empty_scoring_csv():
#     scoringDF = pd.DataFrame(columns=player_list) # collect the points for each game
#     scoringDF[["Week", "Game Nr."]] = schedule[["Week", "Game Nr."]]
#     scoringDF["Winner"] = 0
#     for player in player_list:
#         scoringDF[f"bet_{player}"] = 0
#     scoringDF.to_csv("data/scoring.csv", index=False)
    
# create_empty_bets_csv()
# create_empty_results_csv()
# create_empty_scoring_csv()
# create_empty_teams_scores_csv()