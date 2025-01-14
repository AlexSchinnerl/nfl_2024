import streamlit as st
from functions_load_and_transform import player_list, thisWeek
import pandas as pd

st.set_page_config(
    layout="wide"
    )

playoff_DF = pd.read_csv("data/playoff_view.csv")
playoff_DF.set_index("Players", inplace=True)

st.header("Playoff Scores")
st.dataframe(playoff_DF.sort_values("Gesamtpunkte", ascending=False))

from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge 
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import TreeLayout

nodes = [
    StreamlitFlowNode(id='1', pos=(0, 0), data={'content': 'Chiefs'}, node_type='input', source_position='right'),
    StreamlitFlowNode(id='2', pos=(0, 0), data={'content': 'Texans vs. Chargers'}, node_type='input', source_position='right'),
    StreamlitFlowNode(id='3', pos=(0, 0), data={'content': 'Ravens vs. Steelers'}, node_type='input', source_position='right'),
    StreamlitFlowNode(id='4', pos=(0, 0), data={'content': 'Bills vs. Broncos'}, node_type='input', source_position='right'),
    StreamlitFlowNode(id='5', pos=(0, 0), data={'content': 'Eagles vs. Packers'}, node_type='input', source_position='right'),
    StreamlitFlowNode(id='6', pos=(0, 0), data={'content': 'Rams vs. Vikings'}, node_type='input', source_position='right'),
    StreamlitFlowNode(id='7', pos=(0, 0), data={'content': 'Buccaneers vs. Commanders'}, node_type='input', source_position='right'),
    StreamlitFlowNode(id='8', pos=(0, 0), data={'content': 'Lions'}, node_type='input', source_position='right'),
        
    StreamlitFlowNode(id='9', pos=(0, 0), data={'content': 'Chiefs vs. Texans'}, node_type='default', target_position='left', source_position='right'),
    StreamlitFlowNode(id='10', pos=(0, 0), data={'content': 'Bills vs. Ravens'}, node_type='default', target_position='left', source_position='right'),
    StreamlitFlowNode(id='11', pos=(0, 0), data={'content': 'Eagles vs. Rams'}, node_type='default', target_position='left', source_position='right'),
    StreamlitFlowNode(id='12', pos=(0, 0), data={'content': 'Lions vs. Rams'}, node_type='default', target_position='left', source_position='right'),

    StreamlitFlowNode(id='13', pos=(0, 0), data={'content': 'tbd'}, node_type='default', target_position='left', source_position='right'),
    StreamlitFlowNode(id='14', pos=(0, 0), data={'content': 'tbd'}, node_type='default', target_position='left', source_position='right'),

    StreamlitFlowNode(id='15', pos=(500, 50), data={'content': 'tbd'}, node_type='output', target_position='left'),
        ]

edges = [StreamlitFlowEdge('1-9', '1', '9', animated=True),
         StreamlitFlowEdge('2-9', '2', '9', animated=True),
        StreamlitFlowEdge('3-10', '3', '10', animated=True),
        StreamlitFlowEdge('4-10', '4', '10', animated=True),
        StreamlitFlowEdge('5-11', '5', '11', animated=True),
        StreamlitFlowEdge('6-11', '6', '11', animated=True),
        StreamlitFlowEdge('7-12', '7', '12', animated=True),
        StreamlitFlowEdge('8-12', '8', '12', animated=True),

        StreamlitFlowEdge('9-13', '9', '13', animated=True),
        StreamlitFlowEdge('10-13', '10', '13', animated=True),
        StreamlitFlowEdge('11-14', '11', '14', animated=True),
        StreamlitFlowEdge('12-14', '12', '14', animated=True),

        StreamlitFlowEdge('13-15', '13', '15', animated=True),
        StreamlitFlowEdge('14-15', '14', '15', animated=True),
        ]

state = StreamlitFlowState(nodes, edges)

streamlit_flow('tree_layout', state, layout=TreeLayout(direction='right'))