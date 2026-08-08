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
    "*Psilocybe natalensis* is an African relative of the domesticated “magic mushroom” "
    "*P. cubensis*, and a candidate for the out-of-Africa diaspora that predates cattle "
    "domestication. Because it can grow on **wood** — the ecological setting associated with "
    "**Wood Lovers Paralysis (WLP)**, a reversible paralysis linked to an as-yet-unidentified "
    "tryptamine — its psilocybin-cluster genes are of direct interest: any structural change "
    "in the biosynthetic enzymes could redirect the pathway toward a paralytic analog. "
    "To examine this, we generated a draft whole-genome assembly of *P. natalensis* in-house "
    "from Oxford Nanopore long reads (Ligation-based libraries, one **~17 Gb** run; ~60% of "
    "reads were bacterial microbiome, separated during assembly), and compared it against the "
    "*P. cubensis* “Penis Envy” reference (RefSeq GCF_017499595.1)."
)
st.markdown(
    "Across **12,589** orthologous genes the coding sequence is **~87% identical** at the DNA "
    "level; because only about **29%** of coding-sequence substitutions are nonsynonymous, the "
    "encoded proteins are **~90% identical** — the signature of purifying selection acting "
    "genome-wide. Four barcoding loci (ITS, EF1α, RPB1, RPB2) place our specimen with authentic "
    "*P. natalensis* type material and its close relatives (*P. chuxiongensis*, *P. maluti*), "
    "distinct from both *P. cubensis* and the recently described *P. ochraceocentrata* "
    "(Bradshaw *et al.*) — the species underlying material sold commercially as "
    "“Natal Super Strength.” Focusing on the **psilocybin biosynthesis cluster** "
    "(psiD, psiH, psiM, psiT2, psiR), we map **122** amino-acid substitutions relative to "
    "*P. cubensis* onto AlphaFold/ESMFold structures — the majority in low-constraint regions "
    "rather than catalytic sites, the starting point for asking whether any change plausibly "
    "alters product chemistry."
)
st.markdown(
    "*These data are ~1 week old — an early draft from a partial-run snapshot that will improve "
    "as the full 17 Gb is analyzed. Explore the four analyses from the sidebar; all figures are "
    "the original interactive reports (hover, filter, rotate, toggle as in the source).*"
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

st.divider()
st.subheader("Resources & credits")
st.markdown(
    "- **[psilocydia.net](https://psilocydia.net/)** — 117 public *Psilocybe* genomes; a "
    "community resource for the genetic diversity and origin of the magic mushroom.\n"
    "- **Companion write-up:** *Psilocybe Structural Genomics — can the Psilocybe diaspora "
    "inform on Wood Lovers Paralysis?* (Substack — link to be added)."
)
st.markdown(
    "**Credits.** Stephen McLaughlin — ONT data analysis. "
    "Caleb McKernan, Brendan Kane, Kevin McKernan, Yvonne Helbert and Juliana Carvallo — "
    "DNA preps, library preps and ONT sequencing."
)

st.caption("Data extracted from the standalone interactive HTML reports (MGC/Latest).")
