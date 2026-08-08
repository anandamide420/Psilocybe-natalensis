"""Page 2 — barcoding phylogenies + assembly stats (reproduces the 'Trees & assembly' page)."""
import json, os, io
import streamlit as st
from Bio import Phylo

st.set_page_config(page_title="Trees & assembly", layout="wide")
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "trees_assembly.json")

@st.cache_data
def load():
    with open(DATA_PATH) as f:
        return json.load(f)

D = load()
figs = D.get("figs", {})
newicks = D.get("newicks", [])

st.title("Barcoding phylogenies & assembly")

# newick index → locus label (established earlier: specimen-containing trees are the odd indices)
LOCUS = {1: "ITS", 3: "EF1α", 5: "RPB1", 7: "RPB2"}
SPECIMEN_PATTERNS = ["SAMPLE_Pnat", "Pnat_specimen", "OUR SPECIMEN"]

st.sidebar.header("Controls")
avail = {i: LOCUS.get(i, f"tree {i}") for i in range(len(newicks))}
# prefer the specimen-containing trees
choice = st.sidebar.selectbox("Locus / tree", list(avail.keys()),
                              index=1 if len(newicks) > 1 else 0,
                              format_func=lambda i: avail[i])
show_support = st.sidebar.checkbox("Show branch support", value=False)

st.subheader(f"Phylogeny — {avail.get(choice)}")
try:
    tree = Phylo.read(io.StringIO(newicks[choice]), "newick")
    # highlight the specimen tip
    def label(clade):
        n = clade.name or ""
        for p in SPECIMEN_PATTERNS:
            if p in n:
                return "★ OUR SPECIMEN"
        return n
    fig = None
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, max(4, tree.count_terminals() * 0.16)))
    Phylo.draw(tree, axes=ax, do_show=False, label_func=label,
               show_confidence=show_support)
    st.pyplot(fig)
except Exception as e:
    st.error(f"Could not render tree {choice}: {e}")
    st.text(newicks[choice][:500])

st.divider()
st.header("Assembly statistics")
asm = D.get("assembly", {})
tiles = asm.get("tiles", [])
if tiles:
    # render as metric grid, 4 per row
    for i in range(0, len(tiles), 4):
        cols = st.columns(4)
        for col, t in zip(cols, tiles[i:i+4]):
            col.metric(t["label"], t["value"])
    for note in asm.get("notes", []):
        st.caption(note)

with st.expander("Figure metadata (from report)"):
    st.json(figs, expanded=False)

st.caption("Trees rebuilt from the report's embedded newick strings. Specimen tip highlighted as "
           "★ OUR SPECIMEN. Even-indexed newicks are reference-only trees; odd indices carry the specimen.")
