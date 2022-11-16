# streamlit-vizzu

Bidirectional streamlit component for interacting with vizzu animations

## Installation instructions 

```sh
pip install streamlit-vizzu
```

## Usage instructions

```python
import streamlit as st

from streamlit_vizzu import streamlit_vizzu

value = streamlit_vizzu()

st.write(value)
