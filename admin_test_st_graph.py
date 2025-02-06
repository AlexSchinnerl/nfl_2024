import streamlit as st
import pandas as pd
import numpy as np


df = pd.read_csv("data/teams_incl_LON_LAT.csv")
df["size"] = df["Wins"]*10000
df["color"] = df["Division"].apply(lambda x: "#D50A0A" if x == "AFC" else "#013369")
st.dataframe(df)

st.map(
    df,
    latitude="lat",
    longitude="lon",
    size="size",
    color="color"
    )


# red #D50A0A
# blue #013369