"""Page 1 — ONT sequencing run QC.

Embeds the ORIGINAL interactive report (its own d3/SVG renderer: cumulative-yield
curve, read-length histogram, coverage heatmap, per-barcode comparison table, mash
species panel) inside a Streamlit component iframe. The Claude frame-runtime chrome
(preamble + messaging glue) has been stripped so it runs standalone; the data
payload (embedded <script id="payload">) and renderer are inline, so nothing loads
from the original host. This restores every chart the native rebuild only stubbed.
"""
import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Genome re-analysis — QC", layout="wide")

_LOGO = os.path.join(os.path.dirname(__file__), "..", "assets", "mg_logo.png")
st.logo(_LOGO, size="large", link="https://www.medicinalgenomics.com")

HTML_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "genome_reanalysis_standalone.html")

@st.cache_data
def load_html(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

st.title("Genome re-analysis — sequencing run QC")
st.info(
    "Scope note: this QC report covers a small **~550 Mb Rapid-library pilot run**. "
    "The main assembly (see Trees & assembly) is from the later **17 Gb Ligation-based** "
    "libraries — this page is retained as the earlier pilot QC.",
    icon="ℹ️",
)
st.caption("Interactive report — the original renderer, embedded. Tabs: Per-barcode comparison · "
           "Yield & length · Coverage & identity · Species (mash).")

try:
    html = load_html(HTML_PATH)
    components.html(html, height=1400, scrolling=True)
except FileNotFoundError:
    st.error("genome_reanalysis_standalone.html not found in assets/.")
