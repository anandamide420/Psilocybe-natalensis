"""
Psilocybe natalensis genome portal — Streamlit multipage app.

Home / landing page. The four analysis pages live in pages/:
  1_Genome_reanalysis.py   — ONT sequencing run QC (reads, yield, coverage, mash ID)
  2_Trees_and_assembly.py  — barcoding phylogenies + assembly stats
  3_Coding_changes.py      — genome-wide P. natalensis vs P. cubensis proteome comparison
  4_Psilocybin_cluster_3D.py — psilocybin biosynthesis cluster, 3D structures + variants

Deploy: Streamlit Community Cloud (main file Home.py), or run standalone:
  streamlit run Home.py
Requires: streamlit only (each page embeds a self-contained interactive HTML report).
"""
import os
import streamlit as st

st.set_page_config(page_title="P. natalensis genome portal", layout="wide")

_LOGO = os.path.join(os.path.dirname(__file__), "assets", "mg_logo.png")
st.logo(_LOGO, size="large", link="https://www.medicinalgenomics.com")

st.title("*Psilocybe natalensis* — genome & pathway portal")
st.caption("Medicinal Genomics · in-house Oxford Nanopore sequencing")

st.subheader("Abstract")
st.markdown(
    "We report a draft whole-genome assembly of *Psilocybe natalensis* generated in-house "
    "from Oxford Nanopore long reads (Ligation-based libraries, ~17 Gb of sequence), and a "
    "genome-wide comparison against the *P. cubensis* “Penis Envy” reference "
    "(RefSeq GCF_017499595.1). Across **12,589** orthologous genes the coding sequence is "
    "**~87% identical** at the DNA level; because only about **29%** of coding-sequence "
    "substitutions are nonsynonymous, the encoded proteins are **~90% identical** — the "
    "signature of purifying selection acting on a genome-wide scale. Four barcoding loci "
    "(ITS, EF1α, RPB1, RPB2) place our specimen with the authentic *P. natalensis* type "
    "material and its close relatives (*P. chuxiongensis*, *P. maluti*), distinct from "
    "both *P. cubensis* and the recently described *P. ochraceocentrata* — the species "
    "underlying material sold commercially as “Natal Super Strength.” We further resolve the "
    "**psilocybin biosynthesis cluster** (psiD, psiH, psiM, psiT2, psiR) and map **122** "
    "amino-acid substitutions relative to *P. cubensis* onto AlphaFold/ESMFold structures, "
    "the majority in low-constraint regions rather than catalytic sites."
)
st.markdown(
    "*Explore the four analyses from the sidebar. All figures are the original interactive "
    "reports; hover, filter, rotate, and toggle as in the source.*"
)

st.subheader("Pages")
st.markdown("""
| Page | What it shows |
|---|---|
| **1 · Trees & assembly** | Barcoding-locus phylogenies (ITS / EF1α / RPB1 / RPB2), specimen highlighted, + assembly statistics (yield, contigs, N50, fungal vs contaminant separation) |
| **2 · Coding changes (genome-wide)** | Proteome-wide protein-vs-DNA identity scatter, 12,589 genes vs *P. cubensis*, gene-group highlighting + psilocybin-locus stars |
| **3 · Psilocybin cluster in 3D** | The psiD/psiH/psiM/psiT2/psiR cluster: substitutions painted on AlphaFold/ESMFold structures |
| **4 · Genome re-analysis** | ONT run QC — per-barcode read comparison, yield, coverage & identity, mash species ID. *(A small 550 Mb Rapid-library pilot; the 17 Gb assembly above used Ligation-based libraries.)* |
""")

st.info(
    "**Caveats (apply throughout):** structures are AlphaFold/ESMFold models, not experimental. "
    "Variant calls are against the *P. cubensis* reference from a **draft** ONT assembly. "
    "Low-confidence (low-pLDDT) regions are least reliable in both model and alignment.",
    icon="⚠️",
)

st.caption("Data extracted from the standalone interactive HTML reports (MGC/Latest).")
