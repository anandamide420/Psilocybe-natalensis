"""Page 4 — psilocybin cluster in 3D.

Embeds the ORIGINAL interactive report (its own 3Dmol.js viewer + full control set:
gene picker, structure selector, color modes, superpose/flip, spin, reset, feature
and indel toggles) inside a Streamlit component iframe. The Claude frame-runtime
chrome (preamble + messaging glue) has been stripped so it runs standalone; the
bundled 3Dmol.js library and the full DATA payload are inline, so nothing loads
from the original host. This preserves every feature of the source HTML page.
"""
import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Psilocybin cluster — 3D", layout="wide")

_LOGO = os.path.join(os.path.dirname(__file__), "..", "assets", "mg_logo.png")
st.logo(_LOGO, size="large", link="https://www.medicinalgenomics.com")

HTML_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "cluster3d_standalone.html")

@st.cache_data
def load_html(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

st.title("Psilocybin cluster — coding changes in 3D")
st.caption("Interactive report — the original 3Dmol.js viewer, embedded. Full controls: gene · "
           "structure · color mode · superpose · flip · spin · reset · feature/indel toggles.")

try:
    html = load_html(HTML_PATH)
    components.html(html, height=1500, scrolling=True)
except FileNotFoundError:
    st.error("cluster3d_standalone.html not found in assets/.")
