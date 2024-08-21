import streamlit as st
from load_and_transform import player_list, scoringDF, playerDF

st.set_page_config(
    page_title="Zwischenstand",
    layout="wide"
    )

st.header("Zwischenstand")

selected_week = st.slider(label="Woche auswählen",value=17, min_value=1, max_value=18) # value=thisWeek

playerDF["Gesamtpunkte"] = scoringDF.loc[scoringDF["Week"]<=selected_week, player_list].sum().to_list()
# playerDF["Last Week"] = scoringDF.loc[scoringDF["Week"]<=selected_week-1, player_list].sum().to_list()
playerDF["Wöchentliche Punkte"] = scoringDF.loc[scoringDF["Week"]==selected_week, player_list].sum().to_list()


cols1, cols2 = st.columns([1,2])

with cols1:
    st.dataframe(playerDF, hide_index=True)

with cols2:
    y_options = st.multiselect(label="Graph filtern", options=["Gesamtpunkte", "Wöchentliche Punkte"], default=["Gesamtpunkte"])
    st.bar_chart(playerDF, x="Spieler", y=y_options, stack=False)