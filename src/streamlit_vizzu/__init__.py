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


class VizzuChart:
    def __init__(self, chart, key: Optional[str] = None):
        self.chart = chart
        self.key = key
        self.html = self.chart._repr_html_()
        self.animations: list[str] = []
        self.div_id = f"{self.key}_vizzu"
        self.chart_id = f"{self.key}_vizzu_chart"

    def _repr_html_(self):
        return self.chart._repr_html_()

    def show(self):
        soup = BeautifulSoup(self.html, "html.parser")
        raw_div_id: str = soup.find("div").get("id")  # type: ignore
        raw_chart_id = self.chart._chart_id
        script = soup.find("script").get_text()  # type: ignore
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

    def animate(self, *animations: Animation, **options: Any):
        js = self.animation_to_js(*animations, **options)
        js = js.replace("(element,", f"(document.getElementById('{self.div_id}'),")
        self.animations.append(js)


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
    chart = Chart(width="100%", height="360px", display="manual")

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
