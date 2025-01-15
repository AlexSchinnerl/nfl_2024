import streamlit as st
import pandas as pd

from functions_load_and_transform import player_list, thisWeek, lastWeek, thisWeek_DF, lastWeek_DF
from functions_form import name_submit, send_form

st.header("Road to Superbowl")
st.image("PlayoffTree.png")


st.header("Playoff Tipps")

colA, colB = st.columns([2,1])
with colA:
    st.subheader("Playoff Punktestand")

    playoff_DF = pd.read_csv("data/playoff_view.csv")
    playoff_DF.set_index("Players", inplace=True)

    st.dataframe(playoff_DF.sort_values("Gesamtpunkte", ascending=False))

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

col_A, col_B = st.columns([2,1])
with col_A:
    st.subheader(f"Ergebnisse für Woche {lastWeek}")
    st.dataframe(lastWeek_DF, hide_index=True, height=600)
with col_B:
    st.subheader(f"Spielplan für Woche {thisWeek}")
    st.dataframe(thisWeek_DF, hide_index=True, height=600)


# from streamlit_flow import streamlit_flow
# from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge 
# from streamlit_flow.state import StreamlitFlowState
# from streamlit_flow.layouts import TreeLayout

# nodes = [
#     StreamlitFlowNode(id='1', pos=(66, 0), data={'content': 'Chiefs'}, node_type='input', source_position='right'),
#     StreamlitFlowNode(id='2', pos=(0, 100), data={'content': 'Texans vs. Chargers'}, node_type='input', source_position='right'),
#     StreamlitFlowNode(id='3', pos=(0, 200), data={'content': 'Ravens vs. Steelers'}, node_type='input', source_position='right'),
#     StreamlitFlowNode(id='4', pos=(0, 300), data={'content': 'Bills vs. Broncos'}, node_type='input', source_position='right'),

#     StreamlitFlowNode(id='5', pos=(960, 0), data={'content': 'Lions'}, node_type='input', source_position='left'),
#     StreamlitFlowNode(id='6', pos=(960, 100), data={'content': 'Buccaneers vs. Commanders'}, node_type='input', source_position='left'),
#     StreamlitFlowNode(id='7', pos=(960, 200), data={'content': 'Rams vs. Vikings'}, node_type='input', source_position='left'),
#     StreamlitFlowNode(id='8', pos=(960, 300), data={'content': 'Eagles vs. Packers'}, node_type='input', source_position='left'),

        
#     StreamlitFlowNode(id='9', pos=(150, 150), data={'content': 'Chiefs vs. Texans'}, node_type='default', target_position='left', source_position='right'),
#     StreamlitFlowNode(id='10', pos=(150, 250), data={'content': 'Bills vs. Ravens'}, node_type='default', target_position='left', source_position='right'),
#     StreamlitFlowNode(id='11', pos=(790, 150), data={'content': 'Lions vs. Commanders'}, node_type='default', target_position='right', source_position='left'),
#     StreamlitFlowNode(id='12', pos=(790, 250), data={'content': 'Eagles vs. Rams'}, node_type='default', target_position='right', source_position='left'),

#     StreamlitFlowNode(id='13', pos=(300, 200), data={'content': 'AFC Conference Finals'}, node_type='default', target_position='left', source_position='right'),
#     StreamlitFlowNode(id='14', pos=(620, 200), data={'content': 'NFC Conference Finals'}, node_type='default', target_position='right', source_position='left'),

#     StreamlitFlowNode(id='15', pos=(485, 200), data={'content': 'Superbowl LIX'}, node_type='default', source_position='left', target_position='right'),
#         ]

# edges = [StreamlitFlowEdge('1-9', '1', '9', animated=True),
#          StreamlitFlowEdge('2-9', '2', '9', animated=True),
#         StreamlitFlowEdge('3-10', '3', '10', animated=True),
#         StreamlitFlowEdge('4-10', '4', '10', animated=True),
#         StreamlitFlowEdge('5-11', '5', '11', animated=True),
#         StreamlitFlowEdge('6-11', '6', '11', animated=True),
#         StreamlitFlowEdge('7-12', '7', '12', animated=True),
#         StreamlitFlowEdge('8-12', '8', '12', animated=True),

#         StreamlitFlowEdge('9-13', '9', '13', animated=True),
#         StreamlitFlowEdge('10-13', '10', '13', animated=True),
#         StreamlitFlowEdge('11-14', '11', '14', animated=True),
#         StreamlitFlowEdge('12-14', '12', '14', animated=True),

#         StreamlitFlowEdge('13-15', '13', '15', animated=True),
#         StreamlitFlowEdge('14-15', '14', '15', animated=True),
#         ]

# state = StreamlitFlowState(nodes, edges)

# # streamlit_flow('tree_layout', state, layout=TreeLayout(direction='right'))
# streamlit_flow('static_flow',
#                 state,
#                 fit_view=True,
#                 show_minimap=False,
#                 show_controls=True,
#                 pan_on_drag=False,
#                 allow_zoom=True)
