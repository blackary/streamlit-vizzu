import pandas as pd
import streamlit as st
from ipyvizzu import Chart, Config, Data, Style
from ipyvizzustory import Slide, Step, Story

from streamlit_vizzu import VizzuChart


@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv(
        "https://raw.githubusercontent.com/vizzuhq/vizzu-workshops/main/2022-11-11-PyData-NYC/data/trump_2020_05.csv"
    )


data = Data()

data.add_data_frame(get_data())

chart = Chart(width="100%", height="360px", display="manual")

chart.animate(data)

vchart = VizzuChart(chart, key="vizzu")

vchart.animate(
    Data.filter("record.Firsttweet === 'Igen' && record.Dummy === 'Nem'"),
    Config(
        {
            "channels": {
                "y": {
                    "set": ["tweets"],
                },
                "x": {"set": ["Period", "year", "month"]},
                "color": "Period",
            },
            "title": "Trump started tweeting in May '09",
        }
    ),
)

vchart.show()
