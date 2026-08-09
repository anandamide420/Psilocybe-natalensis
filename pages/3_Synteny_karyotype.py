"""Page 3 — whole-genome synteny / karyotype (P. natalensis vs P. cubensis).

Embeds the ORIGINAL interactive karyotype report (its own D3/SVG renderer and
segment/ribbon controls) inside a Streamlit component iframe. The Claude
frame-runtime chrome (preamble + theme/messaging glue) has been stripped so it
runs standalone, preserving the exact look and interactivity of the source HTML.
"""
import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Synteny / karyotype", layout="wide")

_LOGO = os.path.join(os.path.dirname(__file__), "..", "assets", "mg_logo.png")
st.logo(_LOGO, size="large", link="https://www.medicinalgenomics.com")

HTML_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "synteny_karyotype_standalone.html")

@st.cache_data
def load_html(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

st.title("Whole-genome synteny — P. natalensis → P. cubensis karyotype")
st.caption("Interactive report — the original renderer, embedded. Our draft ONT contigs "
           "(P. natalensis, this study) are placed onto the P. cubensis “Penis Envy” "
           "chromosome-level reference (GCF_017499595.1). Use the in-page controls to switch "
           "views and click a contig/segment for detail.")

try:
    html = load_html(HTML_PATH)
    components.html(html, height=1400, scrolling=True)
except FileNotFoundError:
    st.error("synteny_karyotype_standalone.html not found in assets/.")
