"""Page 3 — genome-wide coding changes.

Embeds the ORIGINAL interactive report (its own d3/SVG scatter: protein-identity vs
DNA-identity for all 12,589 genes, gene-group highlighting, psilocybin-gene stars,
search box, named-function / LoF filters, per-gene hover) inside a Streamlit
component iframe. The Claude frame-runtime chrome (preamble + messaging glue) has
been stripped so it runs standalone; the full gene payload (const G) and renderer
are inline, so nothing loads from the original host.

NOTE: this asset is ~14 MB (all 12,589 genes inline). It loads fine in a browser but
is the heaviest page — first paint may take a couple of seconds.
"""
import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Coding changes — genome-wide", layout="wide")

_LOGO = os.path.join(os.path.dirname(__file__), "..", "assets", "mg_logo.png")
st.logo(_LOGO, size="large", link="https://www.medicinalgenomics.com")

HTML_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "coding_changes_standalone.html")

@st.cache_data
def load_html(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

st.title("Coding changes — P. natalensis vs P. cubensis")
st.caption("Interactive report — the original d3 scatter, embedded. Every gene = one point "
           "(protein vs DNA identity). Highlight gene groups, star the psilocybin locus, search, "
           "and filter by named-function / LoF.")

try:
    html = load_html(HTML_PATH)
    components.html(html, height=1600, scrolling=True)
except FileNotFoundError:
    st.error("coding_changes_standalone.html not found in assets/.")
