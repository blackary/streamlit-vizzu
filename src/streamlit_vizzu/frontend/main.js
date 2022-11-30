// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  // Only run the render code the first time the component is loaded.
  const {div_id, script} = event.detail.args

  let lines = script.split("\n")
  const isCreateChartLine = (line) => line.indexOf("ipyvizzu.createChart") != -1;
  let idx = lines.findIndex(isCreateChartLine)
  let create_chart_lines = lines.slice(0, idx + 1)
  let other_lines = lines.slice(idx + 1)

  // Only run the createChart code the first time the component is loaded.
  if (!window.rendered) {
    const root = document.getElementById("root")

    const element = document.createElement("div")
    element.id = div_id

    root.append(element)

    eval(create_chart_lines.join("\n"))

    // Eventually we'll want to pass some data back
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
