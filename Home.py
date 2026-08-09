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

_HERO = os.path.join(os.path.dirname(__file__), "assets", "hero_landing.png")
_hl, _hc, _hr = st.columns([1, 2, 1])
with _hc:
    st.image(_HERO, use_container_width=True,
             caption="P. natalensis and the out-of-Africa diaspora of the P. cubensis lineage, "
                     "read by long-read (Oxford Nanopore) sequencing. (Illustrative artwork.)")

st.subheader("Abstract")
st.markdown(
    "*Psilocybe natalensis* is an African relative of the domesticated “magic mushroom” "
    "*P. cubensis*, and a candidate for the out-of-Africa diaspora of this lineage. Like "
    "*P. cubensis*, it is reported as associated with **dung and fertilized grassland** rather "
    "than wood — it was first described from South Africa by Gartz *et al.* (1995), and "
    "Bradshaw *et al.* characterise the African *cubensis*-relatives as dung-associated / "
    "woodland leaf-litter species (growing in woodland leaf litter and near decomposing "
    "herbivore dung, not on wood). The broader interest is comparative: the *Psilocybe* linked "
    "to **Wood Lovers Paralysis (WLP)** — chiefly the Australian *P. subaeruginosa* group — are "
    "**wood- *and* dung-inhabiting** species (not exclusively lignicolous; they fruit on woody "
    "debris, wood chips and also dung/enriched soil), yet WLP tracks specifically with their "
    "wood-associated fruiting. WLP is attributed to an as-yet-unidentified tryptamine, so a "
    "reference-grade genome of an African *cubensis* "
    "relative provides a baseline for how conserved the psilocybin biosynthesis cluster is "
    "across the diaspora — the backdrop against which any pathway variation elsewhere in the "
    "genus would be read. Our source material was a **single commercial spore syringe** sold "
    "as *P. natalensis* (Mass Mycology, batch A072403, “for research purposes only”). Because "
    "Bradshaw *et al.* found that most deposited commercial “natalensis” sequences are in fact "
    "*P. ochraceocentrata*, we barcoded this genome before drawing conclusions. We generated a "
    "draft whole-genome assembly in-house from Oxford Nanopore long reads (Ligation-based "
    "libraries, one **~17 Gb** run; ~60% of reads were bacterial microbiome, separated during "
    "assembly), and compared it against the *P. cubensis* “Penis Envy” reference "
    "(RefSeq GCF_017499595.1)."
)
st.markdown(
    "Across **12,589** orthologous genes the coding sequence is **~87% identical** at the DNA "
    "level; because only about **29%** of coding-sequence substitutions are nonsynonymous, the "
    "encoded proteins are **~90% identical** — the signature of purifying selection acting "
    "genome-wide. Barcoding this one genome at four loci (ITS, EF1α, RPB1, RPB2) places it "
    "concordantly with authentic *P. natalensis* type material and its close relatives "
    "(*P. chuxiongensis*, *P. maluti*) — **~99.5% identity** — and ~5.5% away from both "
    "*P. cubensis* and the recently described *P. ochraceocentrata* (Bradshaw *et al.* 2026), "
    "the species now understood to underlie much commercial “Natal Super Strength.” In other "
    "words this particular vial is a genuine *natalensis*-complex organism, **not** the "
    "mislabeled *ochraceocentrata* common in the trade. As a single specimen, this establishes "
    "the identity of this batch — not population- or species-wide variation, which would need "
    "more collections. Focusing on the **psilocybin biosynthesis cluster** "
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
| **1 · Psilocybin cluster in 3D** | The psiD/psiH/psiM/psiT2/psiR cluster: substitutions painted on AlphaFold/ESMFold structures — rotate, toggle, and inspect each residue change |
| **2 · Trees & assembly** | Barcoding-locus phylogenies (ITS / EF1α / RPB1 / RPB2), specimen highlighted, + assembly statistics (yield, contigs, N50, fungal vs contaminant separation) |
| **3 · Synteny / karyotype** | Whole-genome synteny — our draft ONT contigs placed onto the *P. cubensis* chromosome-level reference (1,122 of 1,125 placed), showing large-scale genome conservation between the two species |
| **4 · Coding changes (genome-wide)** | Proteome-wide protein-vs-DNA identity scatter, 12,589 genes vs *P. cubensis*, gene-group highlighting + psilocybin-locus stars |
| **5 · Genome re-analysis** | ONT run QC — per-barcode read comparison, yield, coverage & identity, mash species ID. *(A small 550 Mb Rapid-library pilot; the 17 Gb assembly above used Ligation-based libraries.)* |
""")

st.info(
    "**Caveats (apply throughout):** structures are AlphaFold/ESMFold models, not experimental. "
    "Variant calls are against the *P. cubensis* reference from a **draft** ONT assembly. "
    "Low-confidence (low-pLDDT) regions are least reliable in both model and alignment.",
    icon="⚠️",
)

st.info(
    "**Data availability & roadmap.** Raw ONT sequence reads (concatenated FASTQ) are available here: "
    "[fastq_runid_5c74a372…concat.fastq.gz]"
    "(https://mgcdata.s3.amazonaws.com/shared/fastq_runid_5c74a372-b8e7-4ae3-9a32-a46cf34d2eef-concat.fastq.gz) "
    "(~15.9 GB gzipped ONT reads). "
    "We are currently integrating the *P. subaeruginosa* data from McTaggart *et al.* — the "
    "Australian wood- and dung-inhabiting clade linked to Wood Lovers Paralysis — for direct "
    "psilocybin-cluster comparison, and **this page will continue to update** as the full "
    "17 Gb assembly and additional taxa are analyzed.",
    icon="🔄",
)

st.divider()
st.subheader("The Wood Lovers Paralysis question — where the evidence stands")
st.markdown(
    "Wood Lovers Paralysis (WLP) is a rare, reversible weakness/paralysis reported after eating "
    "certain *Psilocybe* when they fruit on **wood**. It clusters in two regions with endemic "
    "wood-capable species: **Australia / New Zealand** (*P. subaeruginosa* — the source of a "
    "DNA-confirmed clinical case series from Victoria; Silvester *et al.* 2026) and the "
    "**Pacific Northwest USA** (*P. azurescens*, *P. cyanescens*), where the phenomenon has "
    "long been discussed among foragers and is reported to have informed Oregon's regulatory "
    "caution toward lignicolous species (attributions we have not independently verified). "
    "Importantly, these species are **wood- *and* dung-inhabiting**, not exclusively "
    "lignicolous — but WLP tracks specifically with their **wood-grown** fruitings, and the "
    "purely dung- and grass-associated species (*P. cubensis*, *P. natalensis*) are not "
    "implicated. Paralysis after magic mushrooms was first described in 1973 for "
    "the wood-inhabiting *P. subcaerulipes*; the colloquial term is more recent "
    "(Dörner *et al.* 2022). Notably, **there are no reports of WLP from South Africa or "
    "involving *P. natalensis*** — though this reflects reporting patterns (WLP surveillance is "
    "concentrated in Australia/NZ and the US), not proven absence. **No causative compound has "
    "been identified.** The leading idea, on structural grounds, is that the quaternary "
    "trimethylammonium tryptamine **aeruginascin** — or its dephosphorylated congener "
    "**4-OH-TMT** — might behave like the paralytic quaternary alkaloid **bufotenidine**, to "
    "which it is structurally analogous (the aeruginascin/bufotenidine analogy is the basis of "
    "the hypothesis, e.g. Beck & Barlow)."
)
st.markdown(
    "Two findings keep this **hypothetical, not established** — and both come from analytical "
    "chemistry:\n"
    "- **The chemistry is not wood-lover-specific.** In the Hoffmeister lab's LC-MS survey, "
    "aeruginascin was detected in *P. mexicana* and *P. cyanescens*, and — consistent with "
    "earlier work — **also in the dung-inhabiting, non-paralytic *P. cubensis***. The paper "
    "notes explicitly that *no WLP report pertains to P. cubensis* (Dörner *et al.* 2022). So "
    "the presence of aeruginascin alone does not track with the paralysis.\n"
    "- **The putative active metabolite is not found in the mushroom.** In the same survey the "
    "dephosphorylated congener **4-OH-TMT was not detected in any of the species examined** "
    "(Dörner *et al.* 2022) — it is a hypothesized in-body conversion product, not a measured "
    "fungal metabolite. And where 4-OH-TMT has been synthesized and receptor-profiled, its "
    "pharmacology does not cleanly reproduce bufotenidine's (Chadeayne *et al.* 2020)."
)
st.markdown(
    "As of this writing, the WLP causative agent remains **unidentified**, and aeruginascin is "
    "a leading candidate on structural grounds that analytical chemistry has not confirmed. "
    "This is where comparative genomics can *contribute*, not *resolve*: a reference-grade "
    "psilocybin cluster from a **non-wood-loving** African relative (this study) is a baseline "
    "against which the biosynthetic gene complement of the **wood-loving** *P. subaeruginosa* "
    "clade (McTaggart *et al.* 2024) can be compared, asking whether any enzyme difference "
    "could plausibly redirect tryptamine chemistry. It does not, by itself, identify a toxin — "
    "and **we make no claim that *P. natalensis* causes or relates to WLP.**"
)
with st.expander("References"):
    st.markdown(
        "- **Dörner S, Rogge K, Fricke J, … Hoffmeister D (2022).** Genetic Survey of "
        "*Psilocybe* Natural Products. *ChemBioChem* 23(14):e202200249. "
        "doi:10.1002/cbic.202200249. "
        "*(LC-MS: aeruginascin in P. mexicana / P. cyanescens and in P. cubensis; 4-OH-TMT not "
        "detected in any species; notes no WLP report pertains to P. cubensis. Full text "
        "verified.)*\n"
        "- **Chadeayne AR, Pham DNK, Reid BG, … Eguchi R (2020).** Active Metabolite of "
        "Aeruginascin (4-Hydroxy-*N,N,N*-trimethyltryptamine): Synthesis, Structure, and "
        "Serotonergic Binding Affinity. *ACS Omega* 5(27):16940–16943. "
        "doi:10.1021/acsomega.0c02208. *(high affinity at 5-HT1A/2A/2B, does **not** bind 5-HT3 "
        "where activity had been predicted. Full text verified.)*\n"
        "- **Silvester A, Hampton S, May TW, Holmes GD, Leang YH (2026).** Three cases of "
        "wood-lover paralysis: clinical insights from Victoria, Australia. *Clinical Toxicology*. "
        "doi:10.1080/15563650.2026.2640196. *(three patients; Cases 2 & 3 DNA-confirmed as "
        "P. subaeruginosa; states no specific alkaloid has yet been proven to cause WLP. Full "
        "text verified.)*\n"
        "- **McTaggart AR *et al.* (2024).** Wood-loving magic mushrooms (*P. subaeruginosa* "
        "group) from Australia are saprotrophic invaders in the Northern Hemisphere. "
        "*(source of the wood-lover clade we are integrating.)*\n"
        "- The aeruginascin–bufotenidine structural analogy underpinning the WLP hypothesis is "
        "commonly attributed to S. Beck & J. Barlow; the early PNW muscle-weakness observation "
        "to P. Stamets, *Psilocybin Mushrooms of the World* (1996); and the primary bufotenidine "
        "neuromuscular pharmacology to earlier *Arundo donax* studies. **These references are "
        "cited here from summary sources and have not been individually verified against the "
        "originals** — treat the specific attributions as provisional.\n\n"
        "*Bottom line: aeruginascin is detectable by LC-MS but is not wood-lover-specific; the "
        "hypothesized active metabolite (4-OH-TMT) has not been detected in the mushrooms; no "
        "analytical study has yet identified the compound responsible for WLP.*"
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
    "Caleb McKernan, Brendan Kane, Kevin McKernan, Yvonne Helbert and Juliana Carvalho — "
    "DNA preps, library preps and ONT sequencing."
)

st.caption("Data extracted from the standalone interactive HTML reports (MGC/Latest).")

st.divider()
st.subheader("Appendix — source material")
st.markdown(
    "The sequenced material was a single commercial *P. natalensis* spore syringe "
    "(**Mass Mycology, batch A072403**, “For Research Purposes Only”). We barcoded this genome "
    "at four loci before drawing conclusions because Bradshaw *et al.* had shown that most "
    "deposited commercial “natalensis” sequences are in fact *P. ochraceocentrata*; this vial "
    "resolved within the genuine *P. natalensis* complex. Photographs of the source vial are "
    "provided below as a provenance record."
)
_A_FRONT = os.path.join(os.path.dirname(__file__), "assets", "vial_front.jpeg")
_A_BATCH = os.path.join(os.path.dirname(__file__), "assets", "vial_batch.jpeg")
_c1, _c2 = st.columns(2)
with _c1:
    st.image(_A_FRONT, caption="Source vial — label face: “P. Natalensis”, Mass Mycology.",
             use_container_width=True)
with _c2:
    st.image(_A_BATCH, caption="Source vial — batch A072403, “For Research Purposes Only”.",
             use_container_width=True)
st.caption("Provenance: commercial spore syringe, single specimen (n = 1). Identity established "
           "by four-locus barcoding of this genome, not by the vendor label.")
