// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

class IpyVizzu
{
    constructor()
    {
        IpyVizzu.inhibitScroll = false;
        IpyVizzu.nbconvert = false;
        document.addEventListener('wheel', (evt) => { IpyVizzu.inhibitScroll = true }, true);
        document.addEventListener('keydown', (evt) => { IpyVizzu.inhibitScroll = true }, true);
        document.addEventListener('touchstart', (evt) => { IpyVizzu.inhibitScroll = true }, true);

        this.elements = {};
        this.charts = {};

        this.snapshots = {};
        this.displays = {};

        this.events = {};
        this.loaded = {};
        this.libs = {};
    }

    static clearInhibitScroll(element)
    {
        if (IpyVizzu.nbconvert) IpyVizzu._hide(element);
        IpyVizzu.inhibitScroll = false;
    }

    createChart(element, chartId, vizzulib, divWidth, divHeight) {
        this.elements[chartId] = document.createElement("div");
        this.elements[chartId].style.cssText = `width: ${divWidth}; height: ${divHeight};`;
        this.loaded[chartId] = import(vizzulib);
        this.charts[chartId] = this.loaded[chartId].then(Vizzu => {
            this.libs[chartId] = Vizzu.default;
            return new Vizzu.default(this.elements[chartId]).initializing
        });
        this._moveHere(chartId, element);
    }

    animate(element, chartId, displayTarget, scrollEnabled, getChartTarget, chartAnimOpts)
    {
        if (IpyVizzu.nbconvert) IpyVizzu._hide(element);
        if (displayTarget === 'end') this._moveHere(chartId, element);
        this.charts[chartId] = this.charts[chartId].then(chart => {
            if (displayTarget === 'actual') this._moveHere(chartId, element);
            this._scroll(chartId, scrollEnabled);
            let chartTarget = getChartTarget(this.libs[chartId]);
            if (typeof chartTarget === 'string') chartTarget = this.snapshots[chartTarget];
            return chart.animate(chartTarget, chartAnimOpts);
        });
    }

    store(element, chartId, id)
    {
        if (IpyVizzu.nbconvert) IpyVizzu._hide(element);
        this.charts[chartId] = this.charts[chartId].then(chart => {
            this.snapshots[id] = chart.store();
            return chart;
        });
    }

    feature(element, chartId, name, enabled)
    {
        if (IpyVizzu.nbconvert) IpyVizzu._hide(element);
        this.charts[chartId] = this.charts[chartId].then(chart => {
            chart.feature(name, enabled);
            return chart;
        });
    }

    setEvent(element, chartId, id, event, handler)
    {
        if (IpyVizzu.nbconvert) IpyVizzu._hide(element);
        this.charts[chartId] = this.charts[chartId].then(chart => {
            this.events[id] = handler;
            chart.on(event, this.events[id]);
            return chart;
        });
    }

    clearEvent(element, chartId, id, event)
    {
        if (IpyVizzu.nbconvert) IpyVizzu._hide(element);
        this.charts[chartId] = this.charts[chartId].then(chart => {
            chart.off(event, this.events[id]);
            return chart;
        });
    }

    log(element, chartId, chartProperty)
    {
        if (IpyVizzu.nbconvert) IpyVizzu._hide(element);
        this.charts[chartId] = this.charts[chartId].then(chart => {
            console.log(chart[chartProperty])
            return chart;
        });
    }

    _moveHere(chartId, element)
    {
        if (IpyVizzu.nbconvert) IpyVizzu._display(this.elements[chartId], element);
        element.append(this.elements[chartId]);
    }

    _scroll(chartId, enabled)
    {
        if (!IpyVizzu.inhibitScroll && enabled) {
            this.elements[chartId].scrollIntoView({ behavior: "auto", block: "center" });
        }
    }

    static _hide(element) {
        document.getElementById(element.selector.substring(1)).parentNode.style.display = 'none';
    }

    static _display(prevElement, element) {
        if (prevElement.parentNode) {
            prevElement.parentNode.style.display = "none";
        }
        document.getElementById(element.selector.substring(1)).parentNode.style.display = 'flex';
        document.getElementById(element.selector.substring(1)).parentNode.style.margin = 'auto';
    }
}

window.IpyVizzu = IpyVizzu;
window.ipyvizzu = new window.IpyVizzu();

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  // Only run the render code the first time the component is loaded.
  const {div_id, script} = event.detail.args

  lines = script.split("\n")
  const isCreateChartLine = (line) => line.indexOf("ipyvizzu.createChart") != -1;
  idx = lines.findIndex(isCreateChartLine)
  create_chart_lines = lines.slice(0, idx + 1)
  other_lines = lines.slice(idx + 1)
  //create_chart = lines.filter(line => line.indexOf("window.ipyvizzu.createChart") != -1)[0]
  //other_lines = lines.filter(line => line.indexOf("window.ipyvizzu.createChart") == -1)

  //script_lines = script.split("\n")

  if (!window.rendered) {
    // You most likely want to get the data passed in like this

    //console.log(html)

    root = document.getElementById("root")

    element = document.createElement("div")
    element.id = div_id

    root.append(element)

    //eval(script_lines[0])
    //eval(script)
    //create_chart = script.split("\n").filter(line => line.indexOf("window.ipyvizzu.createChart") != -1)[0]
    eval(create_chart_lines.join("\n"))

    //root.innerHTML = "<h1>Yo!</h1>"

    //root.innerHTML = "<div id='500910c'></div>"

    //root.innerHTML = html

    /*
    window.ipyvizzu.createChart(document.getElementById("500910c"), 'f5e861a', 'https://cdn.jsdelivr.net/npm/vizzu@~0.6.0/dist/vizzu.min.js', '700px', '600px');
    window.ipyvizzu.animate(document.getElementById("500910c"), 'f5e861a', 'manual', false, lib => { return {"data": {"series": [{"name": "a", "type": "measure", "values": [4.0, 5.0, 6.0, 7.0, 8.0]}, {"name": "b", "type": "measure", "values": [10.0, 20.0, 30.0, 40.0, 50.0]}, {"name": "c", "type": "measure", "values": [100.0, 50.0, -30.0, -50.0, -70.0]}]}} }, undefined);
    window.ipyvizzu.animate(document.getElementById("500910c"), 'f5e861a', 'manual', false, lib => { return {"config": lib.presets.bar({'x': ['a'], 'y': ['b'], 'title': 'A vs B'})} }, undefined);

    element = document.createElement("div")

    element.innerHTML = html

    //console.log(html)
    document.body.appendChild(element)
    */

    // You'll most likely want to pass some data back to Python like this
    // sendValue({output1: "foo", output2: "bar"})
    window.rendered = true
  }

  eval(other_lines.join("\n"))
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight(500)
