import streamlit as st
from functions_load_and_transform import player_list, schedule, betsDF, scoringDF, lastWeek


# -------------------------
import pandas as pd

st.header("Zwischenstand")

with st.sidebar:
    selected_week = st.slider(label="Woche auswählen",value=lastWeek, min_value=1, max_value=18) # value=thisWeek
    y_options = st.multiselect(label="Graph filtern", options=["Gesamtpunkte", "Wöchentliche Punkte"], default=["Gesamtpunkte"])

playerDF = pd.DataFrame(data={"Spieler":player_list}) # sums up 
playerDF["Gesamtpunkte"] = scoringDF.loc[scoringDF["Week"]<=selected_week, player_list].sum().to_list()
# playerDF["Last Week"] = scoringDF.loc[scoringDF["Week"]<=selected_week-1, player_list].sum().to_list()
playerDF["Wöchentliche Punkte"] = scoringDF.loc[scoringDF["Week"]==selected_week, player_list].sum().to_list()




st.write(f"Ausgewählte Woche: {selected_week}")
st.dataframe(playerDF, hide_index=True)
st.bar_chart(playerDF, x="Spieler", y=y_options, stack=False)