import streamlit as st
from functions_load_and_transform import player_list, schedule, betsDF, scoringDF, lastWeek, thisWeek
import pandas as pd

# st.header("Zwischenstand")

# with st.sidebar:
#     selected_week = st.slider(label="Woche auswählen",value=lastWeek, min_value=1, max_value=18) # value=thisWeek
#     y_options = st.multiselect(label="Graph filtern", options=["Gesamtpunkte", "Wöchentliche Punkte"], default=["Gesamtpunkte"])

# playerDF = pd.DataFrame(data={"Spieler":player_list}) # sums up 
# playerDF["Gesamtpunkte"] = scoringDF.loc[scoringDF["Week"]<=selected_week, player_list].sum().to_list()
# playerDF["Wöchentliche Punkte"] = scoringDF.loc[scoringDF["Week"]==selected_week, player_list].sum().to_list()

# st.write(f"Ausgewählte Woche: {selected_week}")
# st.dataframe(playerDF, hide_index=True)
# st.bar_chart(playerDF, x="Spieler", y=y_options, stack=False)


# import streamlit as st
# from functions_load_and_transform import player_list, schedule, betsDF, scoringDF, lastWeek
# import pandas as pd

st.header("Zwischenstand")

with st.sidebar:
    selected_week = st.slider(label="Woche auswählen",value=lastWeek, min_value=1, max_value=18) # value=thisWeek
    y_options = st.multiselect(label="Graph filtern", options=["Gesamtpunkte", "Wöchentliche Punkte"], default=["Gesamtpunkte"])

week_view_list = list(range(1, selected_week+1))
week_view_list.append("Summe")
scoringDF = scoringDF.drop("Game Nr.").drop("Winner")
# weekly_group = scoringDF.groupby("Week", as_index=False).sum()
weekly_group = scoringDF.groupby("Week").sum()
week_view = weekly_group.transpose()#
week_view["Summe"] = week_view.sum(axis=1)
week_view = week_view[week_view_list]
week_view.columns = week_view.columns.map(str)

st.dataframe(week_view)#.sort_values("Summe", ascending=False))

st.subheader("Gesamtpunkte")
st.bar_chart(week_view, y="Summe", y_label="Gesamtpunkte")
st.subheader(f"Punkte Woche: {selected_week}")
st.bar_chart(week_view, y=str(selected_week), y_label=f"Punkte", color=(53, 94, 59))