import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data
from ipyvizzu.chart import Chart

from streamlit_vizzu import VizzuChart

data_frame = pd.read_csv("https://raw.githubusercontent.com/vizzu-streamlit/streamlit-vizzu/main/sales2.csv")
data = Data()
data.add_data_frame(data_frame)

chart = Chart(width="100%", height="360px", display="manual")

chart.animate(data)

vchart = VizzuChart(chart, key="vizzu")

items: list[str] = st.multiselect(
    "Products",
    ["Shoes", "Handbags", "Gloves", "Accessories"],
    ["Shoes", "Handbags", "Gloves", "Accessories"],
)

col1, col2, col3, col4 = st.columns(4)

measure: str = col1.radio("Measure", ["Sales", "Revenue [$]"])  # type: ignore
compare_by = col2.radio("Compare by", ["Region", "Product", "Both"])
coords = col3.radio("Coordinate system", ["Cartesian (desktop)", "Polar (mobile)"])
order = col4.radio("Order items", ["Alphabetically", "By value"])

filter = " || ".join([f"record['Product'] == '{item}'" for item in items])
title = f"{measure} of " + ", ".join(items)

if compare_by == "Product":
    y = ["Product"]
    x = [measure]
    color = None

elif compare_by == "Region":
    y = [measure]
    x = ["Region"]
    color = ["Region"]

else:
    y = ["Product"]
    x = [measure, "Region"]
    color = ["Region"]


config = {
    "title": title,
    "y": y,
    "label": measure,
    "x": x,
    "color": color,
}

if coords == "Polar (mobile)":
    config["coordSystem"] = "polar"
else:
    config["coordSystem"] = "cartesian"
    
if order == "Alphabetically":
    config["sort"] = "none"
else:
    config["sort"] = "byValue"

vchart.animate(Data.filter(filter), Config(config), delay=0.1)
output = vchart.show()

st.write(output)
