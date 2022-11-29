from pathlib import Path
from typing import Any, Optional

import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
from ipyvizzu.chart import Animate, Animation, Chart, DisplayTemplate

# Tell streamlit that there is a component called streamlit_vizzu,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "streamlit_vizzu", path=str(frontend_dir)
)


# Create the python function that will be called
def streamlit_vizzu(
    chart: Any,
    key: Optional[str] = None,
    step: int = 0,
):
    """
    Add a descriptive docstring
    """
    # components.html(chart._repr_html_(), height=600)
    # st.write(chart._repr_html_())
    html = chart._repr_html_()
    soup = BeautifulSoup(html, "html.parser")
    # div_id = soup.find("div").get("id")
    div_id = f"{key}_vizzu"
    raw_script = soup.find("script").get_text()
    # st.code(raw_script)

    script = """
    window.ipyvizzu.createChart(document.getElementById("55861cd"), '4aa31fc', 'https://cdn.jsdelivr.net/npm/vizzu@~0.6.0/dist/vizzu.min.js', '100%', '360px');
    window.ipyvizzu.animate(document.getElementById("55861cd"), '4aa31fc', 'manual', false, lib => { return {"data": {"series": [{"name": "Region", "type": "dimension", "values": ["North", "North", "North", "North", "South", "South", "South", "South", "East", "East", "East", "East", "West", "West", "West", "West"]}, {"name": "Product", "type": "dimension", "values": ["Shoes", "Handbags", "Gloves", "Accessories", "Shoes", "Handbags", "Gloves", "Accessories", "Shoes", "Handbags", "Gloves", "Accessories", "Shoes", "Handbags", "Gloves", "Accessories"]}, {"name": "Sales", "type": "measure", "values": [4500.0, 7400.0, 2350.0, 8200.0, 3850.0, 6200.0, 3100.0, 10500.0, 2300.0, 3800.0, 7250.0, 5600.0, 4100.0, 6800.0, 3650.0, 7600.0]}, {"name": "Revenue [$]", "type": "measure", "values": [202500.0, 296000.0, 70500.0, 147600.0, 173250.0, 248000.0, 93000.0, 189000.0, 103500.0, 152000.0, 217500.0, 100800.0, 184500.0, 272000.0, 109500.0, 136800.0]}]}} }, undefined);
    window.ipyvizzu.animate(document.getElementById("55861cd"), '4aa31fc', 'manual', false, lib => { return {"data": {"filter": record => { return (record['Product'] == 'Shoes') }}, "config": {"x": "Region", "y": ["Sales", "Product"], "label": "Sales", "color": "Product", "title": "Sales of Shoes"}} }, undefined);
    window.ipyvizzu.animate(document.getElementById("55861cd"), '4aa31fc', 'manual', false, lib => { return {"data": {"filter": record => { return (record['Product'] == 'Shoes' || record['Product'] == 'Handbags') }}, "config": {"title": "Sales of Shoes & Handbags"}} }, {"delay": 0.1});
    """.replace(
        "55861cd", div_id
    )
    st.expander("Show sent code").code(script)

    st.expander("Show code").code(html, language="html")
    component_value = _component_func(
        div_id=div_id,
        script=script,
        step=step,
        key=key,
    )

    return component_value


class VizzuChart:
    def __init__(self, chart, key: Optional[str] = None):
        self.chart = chart
        self.key = key
        self.html = self.chart._repr_html_()
        self.animations: list[str] = []
        self.div_id = f"{self.key}_vizzu"
        self.chart_id = f"{self.key}_vizzu_chart"
        # self.show()

    def _repr_html_(self):
        return self.chart._repr_html_()

    # def show(self, script: Optional[str] = None):
    def show(self):
        # streamlit_vizzu(self)
        # div_id = self.chart._display_target.value
        soup = BeautifulSoup(self.html, "html.parser")
        raw_div_id = soup.find("div").get("id")
        raw_chart_id = self.chart._chart_id
        script = soup.find("script").get_text()
        script += "\n".join(self.animations)

        script = script.replace(raw_div_id, self.div_id)
        script = script.replace(raw_chart_id, self.chart_id)

        # st.expander("Show code").code(html, language="html")
        component_value = _component_func(
            div_id=self.div_id,
            script=script,
            key=self.key,
        )

        return component_value

    def animation_to_js(self, *animations: Animation, **options: Any):
        animation = self.chart._merge_animations(animations)
        animate = Animate(animation, options)
        return DisplayTemplate.ANIMATE.format(
            display_target=self.chart._display_target.value,
            chart_id=self.chart._chart_id,
            scroll=str(self.chart._scroll_into_view).lower(),
            **animate.dump(),
        )

    def animate(self, *animations, **options):
        js = self.animation_to_js(*animations, **options)

        self.animations = [js]

        # self.chart.animate(*args, **kwargs)
        # return self.show()
        # self.show()


def main():
    import pandas as pd
    from st_vizzu import Config, Data, bar_chart

    df = pd.DataFrame(
        {
            "a": [4, 5, 6, 7, 8],
            "b": [10, 20, 30, 40, 50],
            "c": [100, 50, -30, -50, -70],
        }
    )

    chart = bar_chart(df, ["a"], ["b"], "A vs B")

    st.write("## Example")
    # chart._repr_html_()
    # value = streamlit_vizzu(chart)
    vchart = VizzuChart(chart, key="vizzu")

    vchart.show()

    st.write("## Animate")

    vchart.animate(Data.filter(None), Config({"title": "NO FILTER"}), delay=2)

    # st.write(value)


def main2():
    import pandas as pd
    from st_vizzu import Chart, Config, Data, bar_chart

    data_frame = pd.read_csv(
        "https://raw.githubusercontent.com/vizzuhq/ipyvizzu/main/docs/examples/stories/sales/sales.csv",
        dtype={"tenure": str},
    )
    data = Data()
    data.add_data_frame(data_frame)

    # chart = Chart(width="100%", height="360px", display="manual")
    chart = Chart(width="100%", height="360px")

    chart.animate(data)

    chart.animate(
        Data.filter("record['Product'] == 'Shoes'"),
        Config(
            {
                "x": "Region",
                "y": ["Sales", "Product"],
                "label": "Sales",
                "color": "Product",
                "title": "Sales of Shoes",
            }
        ),
    )

    chart.animate(
        Data.filter("record['Product'] == 'Shoes' || record['Product'] == 'Handbags'"),
        Config({"title": "Sales of Shoes & Handbags"}),
        delay=0.1,
    )

    chart.animate(
        Data.filter("record['Product'] != 'Accessories'"),
        Config({"title": "Sales of Shoes, Handbags & Gloves"}),
        delay=0.1,
    )

    chart.animate(
        Data.filter(None), Config({"title": "Sales of All Products"}), delay=2
    )

    chart.animate(
        Config(
            {
                "y": ["Revenue [$]", "Product"],
                "label": "Revenue [$]",
                "title": "Revenue of All Products",
            }
        ),
        delay=2,
    )

    chart.animate(Config({"x": ["Region", "Revenue [$]"], "y": "Product"}), delay=3)

    chart.animate(Config({"x": "Revenue [$]", "y": "Product"}))

    chart.animate(Config({"coordSystem": "polar", "sort": "byValue"}), delay=1)

    # chart.show()

    step = st.slider("Step", 0, 9, 0)
    streamlit_vizzu(chart, key="a_key", step=step)


def main3():
    import pandas as pd
    from st_vizzu import Chart, Config, Data, bar_chart

    data_frame = pd.read_csv(
        "https://raw.githubusercontent.com/vizzuhq/ipyvizzu/main/docs/examples/stories/sales/sales.csv",
        dtype={"tenure": str},
    )
    data = Data()
    data.add_data_frame(data_frame)

    # chart = Chart(width="100%", height="360px", display="manual")
    chart = Chart(width="100%", height="360px", display="manual")

    chart.animate(data)

    vchart = VizzuChart(chart, key="vizzu")

    if st.button("Step 1"):
        vchart.animate(
            Data.filter("record['Product'] == 'Shoes'"),
            Config(
                {
                    "x": "Region",
                    "y": ["Sales", "Product"],
                    "label": "Sales",
                    "color": "Product",
                    "title": "Sales of Shoes",
                }
            ),
        )

    if st.button("Step 2"):
        vchart.animate(
            Data.filter(
                "record['Product'] == 'Shoes' || record['Product'] == 'Handbags'"
            ),
            Config({"title": "Sales of Shoes & Handbags"}),
            delay=0.1,
        )

    if st.button("Add handbags"):
        vchart.animate(
            Data.filter("record['Product'] != 'Accessories'"),
            Config({"title": "Sales of Shoes, Handbags & Gloves"}),
            delay=0.1,
        )

    if st.button("All products"):
        vchart.animate(
            Data.filter(None), Config({"title": "Sales of All Products"}), delay=2
        )

    if st.button("Revenue"):
        vchart.animate(
            Config(
                {
                    "y": ["Revenue [$]", "Product"],
                    "label": "Revenue [$]",
                    "title": "Revenue of All Products",
                }
            ),
            delay=2,
        )

    if st.button("Region"):
        vchart.animate(
            Config({"x": ["Region", "Revenue [$]"], "y": "Product"}), delay=3
        )

    if st.button("Revenue by product"):
        vchart.animate(Config({"x": "Revenue [$]", "y": "Product"}))

    if st.button("Polar"):
        vchart.animate(Config({"coordSystem": "polar", "sort": "byValue"}), delay=1)

    vchart.show()


if __name__ == "__main__":
    main3()
