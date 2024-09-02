import streamlit as st
from functions_load_and_transform import player_list, playerDF, schedule, betsDF, scoringDF


# -------------------------
import pandas as pd

# def calc_score(row): # check if player guessed correctly
#     if row[player] == row["Winner"]:
#         return 1
#     else:
#         return 0

# scoringDF = pd.DataFrame(columns=player_list) # collect the points for each game
# scoringDF["Week"] = schedule["Week"]
# for player in player_list:
#     scoringDF[player] = betsDF.apply(calc_score, axis=1)

# ---------------------------------

# CSS hack für Sidebar Größe
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)


st.header("Zwischenstand")

st.write("Im Moment noch Testdaten aus der Saison 2023/24")

with st.sidebar:
    selected_week = st.slider(label="Woche auswählen",value=17, min_value=1, max_value=18) # value=thisWeek
    y_options = st.multiselect(label="Graph filtern", options=["Gesamtpunkte", "Wöchentliche Punkte"], default=["Gesamtpunkte"])


playerDF["Gesamtpunkte"] = scoringDF.loc[scoringDF["Week"]<=selected_week, player_list].sum().to_list()
# playerDF["Last Week"] = scoringDF.loc[scoringDF["Week"]<=selected_week-1, player_list].sum().to_list()
playerDF[f"Punkte in Woche: {selected_week}"] = scoringDF.loc[scoringDF["Week"]==selected_week, player_list].sum().to_list()


cols1, cols2 = st.columns([1,2])

with cols1:
    st.dataframe(playerDF, hide_index=True)

with cols2:
    st.bar_chart(playerDF, x="Spieler", y=y_options, stack=False)