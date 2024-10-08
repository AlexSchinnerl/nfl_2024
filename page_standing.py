import streamlit as st
from functions_load_and_transform import player_list, schedule, betsDF, scoringDF, lastWeek, thisWeek
import pandas as pd

st.header("Zwischenstand")

# thisWeek = 6

week_view_list = list(range(1, thisWeek))
week_view_list.append("Summe")

scoringDF = scoringDF.drop("Game Nr.", axis=1)
scoringDF = scoringDF.drop("Winner", axis=1)

weekly_group = scoringDF.groupby("Week").sum()
week_view = weekly_group.transpose()#
week_view["Summe"] = week_view.sum(axis=1)
week_view = week_view[week_view_list]
week_view.columns = week_view.columns.map(str)

st.dataframe(week_view.sort_values("Summe", ascending=False), height=((11 + 1) * 35 + 3)) # 11 Reihen + 1 Überschrift * 35 für die Reihenhöhe + 3 für die Borders

st.subheader("Gesamtpunkte")
st.bar_chart(week_view, y="Summe", y_label="Gesamtpunkte")

selected_week = st.slider(label="Woche auswählen",value=lastWeek, min_value=1, max_value=lastWeek)
st.subheader(f"Punkte Woche: {selected_week}")
st.bar_chart(week_view, y=str(selected_week), y_label=f"Punkte", color=(53, 94, 59))



# Old Stuff - bei zeiten löschen

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