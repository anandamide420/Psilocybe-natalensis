"""Page 2 — barcoding phylogenies + assembly.

Embeds the ORIGINAL interactive report (its own D3/SVG tree renderer + toggle
controls) inside a Streamlit component iframe — the Claude frame-runtime chrome
(preamble + messaging glue) has been stripped so it runs standalone. This
preserves the exact look and interactivity of the source HTML page.
"""
import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Trees & assembly", layout="wide")

HTML_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "trees_standalone.html")

@st.cache_data
def load_html(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

st.title("Barcoding phylogenies & assembly")
st.caption("Interactive report — the original renderer, embedded. Use the in-page controls "
           "(Add our ONT runs · Layout · Scale · Labels · Shade · Support) and the Tree / Assembly tabs.")

try:
    html = load_html(HTML_PATH)
    components.html(html, height=1400, scrolling=True)
except FileNotFoundError:
    st.error("trees_standalone.html not found in assets/. Falling back to the native renderer is "
             "available in git history if needed.")
