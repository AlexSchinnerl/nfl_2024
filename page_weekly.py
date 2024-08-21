import streamlit as st
from datetime import datetime
from load_and_transform import schedule, my_bets
from form_functions import name_submit, send_form

st.set_page_config(
    page_title="Wöchentliche Tipps",
    layout="wide"
    )

# thisDay = datetime.today().strftime("%Y-%m-%d") # for live
thisDay = datetime(2024, 9, 6)

thisWeek = list(schedule.loc[schedule["Date"]<thisDay, "Week"])[-1]
thisWeek = 1
lastWeek = thisWeek-1

thisWeek_DF = schedule.loc[schedule["Week"]==thisWeek, ["Game Nr.", "Date", "Location", "Home Team", "Away Team"]]
lastWeek_DF = my_bets.loc[my_bets["Week"]==lastWeek, ["Game Nr.", "Home Team", "Score Home", "Score Guest", "Away Team"]]












st.header("Wöchentliche Tipps")

colA, colB = st.columns(2)
with colA:
    if thisWeek == 1:
        pass
    else:
        st.subheader(f"Ergebnisse für Woche {lastWeek}")
        st.dataframe(lastWeek_DF, hide_index=True, height=600)

    st.subheader(f"Spielplan für Woche {thisWeek}")
    st.dataframe(thisWeek_DF, hide_index=True, height=600)

with colB:
    st.subheader("Hier Tipps auswählen")
    with st.form("Place Bet"):
        selected_teams = []
        for pairing in zip(thisWeek_DF["Home Team"], thisWeek_DF["Away Team"], thisWeek_DF["Game Nr."]):
            chosen_winner = st.selectbox(
                label=f"Game Nr.: {pairing[2]} {pairing[0]} vs. {pairing[1]}", 
                options=pairing[0:2], 
                index=None, 
                placeholder="Bitte Gewinner auswählen"
                )
            selected_teams.append(chosen_winner)
        player_name, weekly_submitted = name_submit("Tipps absenden")
    if weekly_submitted:
        selected_teams.append(player_name)
        send_form(mailText=selected_teams[:-1], subject=f"bets_{selected_teams[-1]}_week_{thisWeek}")