"""Page 3 — genome-wide proteome comparison (reproduces the 'Coding changes' page, table view)."""
import json, os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Coding changes — genome-wide", layout="wide")
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "coding_changes_genomewide.json")

@st.cache_data
def load():
    with open(DATA_PATH) as f:
        return json.load(f)

D = load()
df = pd.DataFrame(D["genes"])
for c in ["protein_pct_id", "nt_pct_id", "nonsyn_fraction_pct", "copy_number",
          "loss_of_function_flag", "confident_LoF_flag", "n_synonymous",
          "n_nonsynonymous", "n_aa_changes", "start", "end"]:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

st.title("Genome-wide coding changes — *P. natalensis* vs *P. cubensis*")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Genes compared", f"{len(df):,}")
c2.metric("Median protein % id", f"{df['protein_pct_id'].median():.1f}%")
c3.metric("Confident LoF genes", f"{int((df['confident_LoF_flag']==1).sum()):,}")
c4.metric("Multi-copy genes", f"{int((df['copy_number']>1).sum()):,}")

st.sidebar.header("Filters")
contigs = ["(all)"] + sorted(df["contig"].dropna().unique().tolist())
contig = st.sidebar.selectbox("Contig", contigs)
maxpid = st.sidebar.slider("Max protein % identity", 0, 100, 100,
                           help="Show genes AT OR BELOW this identity — surface the most divergent.")
only_lof = st.sidebar.checkbox("Confident loss-of-function only", value=False)
search = st.sidebar.text_input("Search product / locus_tag")

view = df.copy()
if contig != "(all)":
    view = view[view["contig"] == contig]
view = view[view["protein_pct_id"].fillna(101) <= maxpid]
if only_lof:
    view = view[view["confident_LoF_flag"] == 1]
if search:
    s = search.lower()
    view = view[view["product"].str.lower().str.contains(s, na=False) |
                view["locus_tag"].str.lower().str.contains(s, na=False)]

st.subheader(f"{len(view):,} genes")
st.dataframe(
    view[["locus_tag", "gene_symbol", "product", "contig", "start", "end",
          "protein_pct_id", "nonsyn_fraction_pct", "copy_number",
          "confident_LoF_flag", "n_aa_changes"]],
    use_container_width=True, hide_index=True, height=460,
)

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Protein identity distribution")
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.hist(df["protein_pct_id"].dropna(), bins=50, color="#2166ac")
    ax.axvline(df["protein_pct_id"].median(), color="#b2182b", ls="--", lw=1,
               label=f"median {df['protein_pct_id'].median():.1f}%")
    ax.set_xlabel("protein % identity"); ax.set_ylabel("genes"); ax.legend(fontsize=7)
    for s in ["top", "right"]: ax.spines[s].set_visible(False)
    st.pyplot(fig)
with col_b:
    st.subheader("Divergence vs gene density by contig")
    g = df.groupby("contig")["protein_pct_id"].median().sort_values()
    fig2, ax2 = plt.subplots(figsize=(5, 3))
    ax2.barh(g.index.astype(str), g.values, color="#4a7")
    ax2.set_xlabel("median protein % id"); ax2.set_xlim(80, 100)
    for s in ["top", "right"]: ax2.spines[s].set_visible(False)
    st.pyplot(fig2)

st.download_button("Download filtered table (CSV)",
                   view.to_csv(index=False).encode(), "coding_changes_filtered.csv", "text/csv")
st.caption(f"Column legend: {D['columns_legend']}")
