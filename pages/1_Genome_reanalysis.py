"""Page 1 — ONT sequencing run QC (reproduces the 'Mushroom Genome Sequencing — re-analysis' page)."""
import json, os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Genome re-analysis — QC", layout="wide")
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "genome_reanalysis.json")

@st.cache_data
def load():
    with open(DATA_PATH) as f:
        return json.load(f)

D = load()
st.title("Genome re-analysis — sequencing run QC")

# ---- top metrics ----
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total reads (all)", f"{D.get('total_reads_all'):,}")
c2.metric("Reads before (MinKNOW)", f"{D.get('before_total'):,}")
c3.metric("Run span", f"{D.get('t_span_h', 0):.1f} h")
# top-line species call: nearest mash hit across barcodes
ms = D.get("mash_species", {})
top = None
for bc, hits in (ms.items() if isinstance(ms, dict) else []):
    if hits:
        h0 = hits[0]
        if top is None or h0.get("dist", 1) < top[1]:
            top = (h0.get("sp", "?").replace("_", ". "), h0.get("dist", 1))
c4.metric("Mash top hit", top[0] if top else "—",
          f"dist {top[1]:.3f}" if top else None)

tab1, tab2, tab3, tab4 = st.tabs(["Per-barcode comparison", "Yield & length", "Coverage & identity", "Species (mash)"])

with tab1:
    st.subheader("Per-barcode read comparison")
    comp = pd.DataFrame(D.get("comparison", []))
    st.dataframe(comp, use_container_width=True, hide_index=True)
    # bar chart of pass reads by barcode if columns present
    numcols = [c for c in comp.columns if comp[c].astype(str).str.replace(",", "").str.isnumeric().all()]
    if "barcode" in comp.columns and "pass_reads" in comp.columns:
        fig, ax = plt.subplots(figsize=(9, 3.2))
        pr = pd.to_numeric(comp["pass_reads"].astype(str).str.replace(",", ""), errors="coerce")
        ax.bar(range(len(comp)), pr, color="#2166ac")
        ax.set_ylabel("pass reads")
        ax.set_xticks(range(len(comp)))
        ax.set_xticklabels(comp["barcode"], rotation=60, ha="right", fontsize=6)
        for s in ["top", "right"]: ax.spines[s].set_visible(False)
        st.pyplot(fig)

with tab2:
    st.subheader("Cumulative yield")
    yc = D.get("yield_cum_mb", {})
    if isinstance(yc, dict) and yc:
        # dict of {series: [values]} or {x:[],y:[]}
        st.json(yc, expanded=False)
    lh = D.get("len_hist", {})
    if lh:
        st.subheader("Read-length histogram")
        # len_hist expected {'bins':[], 'counts':[]} or similar
        try:
            keys = list(lh.keys())
            fig, ax = plt.subplots(figsize=(9, 3.2))
            if "counts" in lh and ("bins" in lh or "edges" in lh):
                x = lh.get("bins", lh.get("edges"))
                ax.bar(range(len(lh["counts"])), lh["counts"], color="#4a7", width=1.0)
                ax.set_xlabel("length bin"); ax.set_ylabel("reads")
            else:
                st.json(lh, expanded=False)
            for s in ["top", "right"]: ax.spines[s].set_visible(False)
            st.pyplot(fig)
        except Exception:
            st.json(lh, expanded=False)

    st.subheader("Per-channel output")
    cr = D.get("channel_reads", [])
    if cr:
        ch = [c[0] for c in cr]; rd = [c[1] for c in cr]
        fig, ax = plt.subplots(figsize=(9, 2.8))
        ax.bar(ch, rd, color="#4a7", width=1.0)
        ax.set_xlabel(f"flow-cell channel (n={len(cr)})"); ax.set_ylabel("reads")
        ax.set_title(f"{sum(rd):,} reads across {len(cr)} active channels", fontsize=9, loc="left")
        for s in ["top", "right"]: ax.spines[s].set_visible(False)
        st.pyplot(fig)

with tab3:
    st.subheader("Coverage distribution")
    st.json(D.get("covdist", {}), expanded=False)
    st.subheader("Alignment identity")
    st.json(D.get("identity", {}), expanded=False)

with tab4:
    st.subheader("Mash species identification")
    ms = D.get("mash_species", {})
    if isinstance(ms, dict):
        st.json(ms, expanded=True)
    st.subheader("Pairwise mash distances")
    st.json(D.get("mash_pairwise", {}), expanded=False)

st.caption("QC metrics parsed from the ONT re-analysis report. JSON blocks shown raw where the "
           "original chart geometry wasn't reconstructed; tell the agent which charts you want rendered natively.")
