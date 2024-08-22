import streamlit as st
from datetime import datetime
from functions_load_and_transform import schedule, my_bets, playoff_teams_DF, player_list, scoringDF, playerDF, team_list
from functions_mail import send_mail_function

def send_form(mailText, subject):
    try:
        send_mail_function(mail_key=MYKEY, mailText=mailText, subject=subject)
        st.success("Tipps abgeschickt!")
    except Exception:
        st.error("Fehler beim Übermitteln")

def name_submit(button_description):
    col1a, col1b = st.columns(2)
    with col1a:
        player_name = st.text_input("Name eingeben", placeholder="Hier euren Namen eintragen")
    with col1b:
        st.write("\n")
        st.write("\n")
        submitted = st.form_submit_button(button_description)
    return player_name, submitted

def playoff_checkboxes(df):
    for subdivision in sorted(df["Subdivision"].unique()):
        st.write(f"{subdivision}")
        for team in df.loc[df["Subdivision"]==subdivision, "Teams"]:
            check_team = st.checkbox(label=team, value=False)
            if check_team:
                selected_playoff_teams.append(team)

st.set_page_config(
    page_title="NFL Tippspiel",
    layout="wide"
    )

import keyring
MYKEY = keyring.get_password("alxMail", "alex")
# MYKEY = st.secrets["my_key"]

# thisDay = datetime.today().strftime("%Y-%m-%d") # for live
thisDay = datetime(2024, 9, 6)

# betsDF = pd.read_csv("season_2024/data/bets.csv", delimiter=";")
filtered_bets = schedule.loc[schedule["Date"]<thisDay].copy()
thisWeek = list(schedule.loc[schedule["Date"]<thisDay, "Week"])[-1]
thisWeek = 1
lastWeek = thisWeek-1

# # Transform Dataframes
# filtered_bets["Winner"] = filtered_bets.apply(check_winner, axis=1)
thisWeek_DF = schedule.loc[schedule["Week"]==thisWeek, ["Game Nr.", "Date", "Location", "Home Team", "Away Team"]]
lastWeek_DF = my_bets.loc[my_bets["Week"]==lastWeek, ["Game Nr.", "Home Team", "Score Home", "Score Guest", "Away Team"]]
afc_DF = playoff_teams_DF.loc[playoff_teams_DF["Division"]=="AFC"]
nfc_DF = playoff_teams_DF.loc[playoff_teams_DF["Division"]=="NFC"]


with open("textfiles/vorab_explain.md") as f:
    vorab_text = f.read()

with open("textfiles/ablauf_tippspiel.md") as f:
    how2_text = f.read()





st.title("NFL Tippspiel 2024")

vorab, weekly, standings, help_page = st.tabs(["Vorab Tipps", "Wöchentliche Tipps", "Zwischenstand", "Anleitung"])

with vorab:
    st.header("Vorab Tipps")

    superbowl, playoff = st.columns(2)
    
    with superbowl:
        st.subheader("Superbowl Vorab Tipp")
        with st.form("Place Superbowl Bet"):
            superbowl_bet = st.selectbox(label="Superbowl Tipp abgeben", options=team_list, index=None, placeholder="Hier Superbowl Sieger auswählen")
            player_name, superbowl_submitted = name_submit("Superbowl Tipp absenden")
        if superbowl_submitted:
            send_form(mailText=f"{player_name}: {superbowl_bet}", subject=f"Superbowl_vorab_{player_name}")

        st.divider()
        st.markdown(vorab_text)

    with playoff:
        st.subheader("Playoff Vorab Tipp")
        with st.form("Place Playoff Bet"):
            col1, col2 = st.columns(2)
            selected_playoff_teams = []
            with col1:
                st.subheader("AFC Playoff Teams")
                playoff_checkboxes(afc_DF)
            with col2:
                st.subheader("NFC Playoff Teams")
                playoff_checkboxes(nfc_DF)
            player_name, playoff_submitted = name_submit("Playoff Tipps absenden")      
        if playoff_submitted:
            send_form(mailText=f"{player_name}: {selected_playoff_teams}", subject=f"Playoff_vorab_{player_name}")










with weekly:
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










with standings:
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
# ["Zuwachs", "Last Week"]

# maximal mögliche Punkte




with help_page:
    st.markdown(how2_text)