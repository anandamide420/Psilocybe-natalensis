"""
Psilocybe natalensis genome portal — Streamlit multipage app.

Home / landing page. The four analysis pages live in pages/:
  1_Genome_reanalysis.py   — ONT sequencing run QC (reads, yield, coverage, mash ID)
  2_Trees_and_assembly.py  — barcoding phylogenies + assembly stats
  3_Coding_changes.py      — genome-wide P. natalensis vs P. cubensis proteome comparison
  4_Psilocybin_cluster_3D.py — psilocybin biosynthesis cluster, 3D structures + variants

Deploy: drop this folder into the same repo/server that serves the pathogen/KASP
Streamlit tools, or run standalone:  streamlit run Home.py
Requires: streamlit, py3Dmol, stmol, ipython_genutils, pandas, matplotlib, biopython
"""
import streamlit as st

st.set_page_config(page_title="P. natalensis genome portal", layout="wide")

st.title("*Psilocybe natalensis* — genome & pathway portal")
st.markdown(
    "An in-house Oxford Nanopore assembly of *Psilocybe natalensis*, compared against the "
    "*P. cubensis* reference. Use the sidebar to open each analysis."
)

st.subheader("Pages")
st.markdown("""
| Page | What it shows |
|---|---|
| **1 · Genome re-analysis** | ONT run QC — per-barcode read comparison, yield, per-channel output, coverage & identity, mash species ID |
| **2 · Trees & assembly** | Barcoding-locus phylogenies (ITS / EF1α / RPB1 / RPB2), specimen highlighted, + assembly statistics (yield, contigs, N50, fungal vs contaminant separation) |
| **3 · Coding changes (genome-wide)** | Proteome-wide amino-acid divergence table, 12,589 genes vs *P. cubensis* |
| **4 · Psilocybin cluster in 3D** | The psiD/psiH/psiM/psiT2/psiR cluster: substitutions painted on AlphaFold/ESMFold structures |
""")

st.info(
    "**Caveats (apply throughout):** structures are AlphaFold/ESMFold models, not experimental. "
    "Variant calls are against the *P. cubensis* reference from a **draft** ONT assembly. "
    "Low-confidence (low-pLDDT) regions are least reliable in both model and alignment.",
    icon="⚠️",
)

st.caption("Data extracted from the standalone interactive HTML reports (MGC/Latest).")
