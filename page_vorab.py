import streamlit as st
from functions_load_and_transform import playoff_teams_DF, team_list
from functions_form import name_submit, send_form

def playoff_checkboxes(df):
    for subdivision in sorted(df["Subdivision"].unique()):
        st.write(f"{subdivision}")
        for team in df.loc[df["Subdivision"]==subdivision, "Teams"]:
            check_team = st.checkbox(label=team, value=False)
            if check_team:
                selected_playoff_teams.append(team)

afc_DF = playoff_teams_DF.loc[playoff_teams_DF["Division"]=="AFC"]
nfc_DF = playoff_teams_DF.loc[playoff_teams_DF["Division"]=="NFC"]

with open("textfiles/vorab_explain.md") as f:
    vorab_text = f.read()


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