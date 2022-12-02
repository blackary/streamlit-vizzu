from pathlib import Path
from typing import Any, Optional

import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
from ipyvizzu.chart import Animate, Animation, Chart, DisplayTarget, DisplayTemplate

# Tell streamlit that there is a component called streamlit_vizzu,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "streamlit_vizzu", path=str(frontend_dir)
)


class VizzuChart:
    def __init__(
        self, chart: Chart, key: Optional[str] = None, return_clicks: bool = True
    ):
        self.chart = chart
        if self.chart._display_target != DisplayTarget.MANUAL:
            st.error("VizzuChart only works with charts with display='manual'")
            st.stop()
        self.key = key or "vizzu"
        self.div_id = f"{self.key}_vizzu"
        self.chart_id = f"{self.key}_vizzu_chart"
        self.html = self.chart._repr_html_()
        self.animations: list[str] = []
        self.return_clicks = return_clicks

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

        component_value = _component_func(
            div_id=self.div_id,
            chart_id=self.chart_id,
            script=script,
            return_clicks=self.return_clicks,
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
