"""
Psilocybin cluster — 3D coding-change viewer (Streamlit port of the standalone HTML page).

Reproduces the interactive HTML site:
  - pick a cluster gene
  - pick which structure to show (AlphaFold cubensis ref, ESMFold cubensis, ESMFold natalensis)
  - 3D structure with amino-acid substitutions painted on (colored by pLDDT confidence)
  - toggle: superpose the natalensis model on the reference
  - radio: color scheme (variants / pLDDT / plain)
  - linear per-residue variant map + summary tables

Drop this file (and psilo_cluster_data.json alongside it) into the same Streamlit
project that serves the pathogen/KASP tools. If that project is a multipage app,
put this in the pages/ folder; otherwise run it directly:
    streamlit run psilocybin_cluster_app.py

Requires: streamlit, py3Dmol, stmol  (pip install stmol py3Dmol)
"""
import json, os
import streamlit as st
import py3Dmol
from stmol import showmol

st.set_page_config(page_title="Psilocybin cluster — coding changes in 3D", layout="wide")

DATA_PATH = os.path.join(os.path.dirname(__file__), "psilo_cluster_data.json")

@st.cache_data
def load():
    with open(DATA_PATH) as f:
        return json.load(f)

DATA = load()
GENES = {g["gene"]: g for g in DATA["genes"]}
ORDER = [g["gene"] for g in DATA["genes"]]

# ---- pLDDT color ramp (AlphaFold convention) ----
def plddt_color(p):
    if p is None: return "#888888"
    if p >= 90: return "#0053D6"
    if p >= 70: return "#65CBF3"
    if p >= 50: return "#FFDB13"
    return "#FF7D45"

st.title("Psilocybin cluster — coding changes in 3D")
st.caption("Amino-acid changes between an in-house ONT *P. natalensis* assembly and the "
           "*P. cubensis* reference, painted onto AlphaFold / ESMFold structures.")

# ---------------- sidebar controls (the HTML radio buttons / dropdowns) ----------------
with st.sidebar:
    st.header("Controls")
    gene = st.selectbox("Cluster gene", ORDER,
                        format_func=lambda k: f"{k} — {GENES[k]['name']}")
    g = GENES[gene]
    struct_opts = {s["id"]: s["label"] for s in g["structs"]}
    # default to the natalensis model if present, else AlphaFold ref
    default_sid = "esm_nat" if "esm_nat" in struct_opts else g["structs"][0]["id"]
    sid = st.radio("Structure", list(struct_opts.keys()),
                   index=list(struct_opts.keys()).index(default_sid),
                   format_func=lambda k: struct_opts[k])
    color_by = st.radio("Color scheme", ["Variants (subs highlighted)", "pLDDT confidence", "Plain (spectrum)"])
    superpose = st.checkbox("Superpose natalensis on reference", value=False,
                            help="Overlay the natalensis model (grey) on the chosen structure to see backbone divergence.")
    show_sites = st.checkbox("Show binding / active sites", value=True)
    style_choice = st.selectbox("Representation", ["cartoon", "stick + cartoon"])

# ---------------- gene header stats ----------------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Length", f"{g['plen']} aa")
c2.metric("% identity", f"{g['pid']}%")
c3.metric("Substitutions", len(g["variants"]))
c4.metric("Backbone RMSD", f"{g['compare']['rmsd']} Å")
c5.metric("TM-score", f"{g['compare']['tm']}")

# ---------------- 3D viewer ----------------
def build_view(g, sid, color_by, superpose, show_sites, style_choice):
    struct = next(s for s in g["structs"] if s["id"] == sid)
    pdb = struct["pdb"]
    view = py3Dmol.view(width=820, height=560)
    view.addModel(pdb, "pdb")

    # base representation
    if color_by.startswith("pLDDT"):
        # color by b-factor (pLDDT stored in B-factor column of AF/ESM PDBs)
        view.setStyle({"cartoon": {"colorscheme": {"prop": "b",
            "gradient": "roygb", "min": 50, "max": 90}}})
    elif color_by.startswith("Plain"):
        view.setStyle({"cartoon": {"color": "spectrum"}})
    else:
        view.setStyle({"cartoon": {"color": "#cfd4dc"}})  # neutral grey; variants painted below

    # paint substitutions
    if color_by.startswith("Variants"):
        for v in g["variants"]:
            col = plddt_color(v.get("plddt"))
            sel = {"resi": v["resi"]}
            view.addStyle(sel, {"cartoon": {"color": col}})
            if style_choice.startswith("stick"):
                view.addStyle(sel, {"stick": {"color": col, "radius": 0.25}})

    # binding / active sites as red sticks
    if show_sites:
        for f in g["features"]:
            if f["t"] and ("Binding" in f["t"] or "Active" in f["t"]):
                for r in range(int(f["s"]), int(f["e"]) + 1):
                    view.addStyle({"resi": r}, {"stick": {"color": "#d62728", "radius": 0.3}})

    # superpose native (grey, transparent cartoon)
    if superpose and g.get("pdb_nat_super"):
        view.addModel(g["pdb_nat_super"], "pdb")
        view.setStyle({"model": 1}, {"cartoon": {"color": "#999999", "opacity": 0.55}})

    view.zoomTo()
    view.setBackgroundColor("0xffffff")
    return view

left, right = st.columns([3, 2])
with left:
    st.subheader(f"{gene} · {next(s['label'] for s in g['structs'] if s['id']==sid)}")
    view = build_view(g, sid, color_by, superpose, show_sites, style_choice)
    showmol(view, height=560, width=820)
    st.caption("Substitution colors = model confidence at that residue "
               "(dark blue ≥90, light blue 70–90, yellow 50–70, orange <50 pLDDT). "
               "Red sticks = binding/active sites. Grey overlay = superposed natalensis model.")

with right:
    st.subheader("Substitutions")
    import pandas as pd
    vdf = pd.DataFrame(g["variants"])
    if len(vdf):
        vdf["change"] = vdf["ref"] + vdf["pos"].astype(str) + vdf["alt"]
        st.dataframe(vdf[["change", "pos", "plddt"]].rename(columns={"plddt": "pLDDT"}),
                     height=300, use_container_width=True, hide_index=True)
    st.subheader("Sequence features")
    fdf = pd.DataFrame(g["features"])
    if len(fdf):
        st.dataframe(fdf.rename(columns={"t": "type", "s": "start", "e": "end"}),
                     height=180, use_container_width=True, hide_index=True)

# ---------------- linear variant map (matplotlib, always renders) ----------------
st.subheader("Per-residue map")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(11, 1.6))
L = g["plen"]
ax.add_patch(plt.Rectangle((0, -0.12), L, 0.24, color="#e6e6e6"))
for f in g["features"]:
    if f["t"] and ("Binding" in f["t"] or "Active" in f["t"]):
        ax.plot([f["s"], f["s"]], [-0.12, 0.12], color="#d62728", lw=1.5)
for v in g["variants"]:
    col = plddt_color(v.get("plddt"))
    ax.plot([v["pos"], v["pos"]], [0.12, 0.7], color=col, lw=0.7)
    ax.plot(v["pos"], 0.7, "o", ms=3, color=col)
for d in g["indels"]:
    ax.plot(d.get("after", 0), -0.3, "v", ms=7, color="#111")
ax.set_xlim(-5, L + 5); ax.set_ylim(-0.45, 0.9); ax.set_yticks([])
ax.set_xlabel("residue position"); 
for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
st.pyplot(fig)

st.divider()
st.caption("Caveats: AlphaFold/ESMFold models, not crystal structures; substitutions called "
           "against the P. cubensis reference from a draft ONT assembly; low-pLDDT changes sit "
           "where both model and alignment are least reliable.")
