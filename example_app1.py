import pandas as pd
import streamlit as st
from ipyvizzu.animation import Config, Data
from ipyvizzu.chart import Chart

from streamlit_vizzu import VizzuChart

data_frame = pd.read_csv(
    "https://raw.githubusercontent.com/vizzuhq/ipyvizzu/main/docs/examples/stories/sales/sales.csv",
    dtype={"tenure": str},
)
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

col1, col2, col3 = st.columns(3)

measure: str = col1.radio("Measure", ["Sales", "Revenue [$]"])  # type: ignore
compare_by = col2.radio("Campare by", ["Region", "Product", "Both"])
coords = col3.radio("Coordinate system", ["Cartesian", "Polar"])

filter = " || ".join([f"record['Product'] == '{item}'" for item in items])
title = f"{measure} of " + ", ".join(items)

if compare_by == "Product":
    x = ["Product"]
    y = [measure]
    color = None

elif compare_by == "Region":
    x = [measure]
    y = ["Region"]
    color = ["Region"]

else:
    x = ["Product"]
    y = [measure, "Region"]
    color = ["Region"]


config = {
    "title": title,
    "y": y,
    "label": measure,
    "x": x,
    "color": color,
}

if coords == "Polar":
    config["coordSystem"] = "polar"
    config["sort"] = "byValue"
else:
    config["coordSystem"] = "cartesian"
    config["sort"] = "none"

vchart.animate(Data.filter(filter), Config(config), delay=0.1)
output = vchart.show()

st.write(output)
