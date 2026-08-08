# *Psilocybe natalensis* genome portal — Streamlit app

Multipage Streamlit port of the four standalone interactive HTML reports (MGC/Latest).
Reproduces the radio-button / dropdown interactivity that Substack/Twitter strip out.

**Implementation note:** this is a *native rebuild* (Route 2), not an iframe embed of the
original HTML. The data payloads were extracted from each report's inline JS (`const DATA`,
`const G`, `const FIGS`, and a JSON `<script>` tag) into `data/*.json`, and the interactivity
is reimplemented from scratch with Streamlit widgets driving pandas / matplotlib / Bio.Phylo /
py3Dmol. (The alternative — dropping the raw report HTML into `st.components.v1.html` so the
original JS runs in an iframe — was not used, because those reports depend on a Claude
frame-runtime that only resolves on claudeusercontent.com.) The 3D structure viewer (page 4)
is genuine JS: py3Dmol/stmol renders 3Dmol.js inside a Streamlit component iframe.

## Layout
```
Home.py                          landing page
pages/
  1_Genome_reanalysis.py         ONT run QC (reads, yield, coverage, mash ID)
  2_Trees_and_assembly.py        barcoding phylogenies (Bio.Phylo), specimen highlighted, + assembly stats
  3_Coding_changes.py            genome-wide proteome comparison, 12,589 genes
  4_Psilocybin_cluster_3D.py     psilocybin cluster 3D (py3Dmol/stmol) + variant map
data/
  genome_reanalysis.json         33 KB
  trees_assembly.json            156 KB  (figs + 8 newick trees)
  coding_changes_genomewide.json 4.4 MB  (compact 12,589-gene table)
  psilo_cluster_data.json        5.4 MB  (5 genes, structures + variants)
requirements.txt
```

## Run locally
```
pip install -r requirements.txt
streamlit run Home.py
```

## Deploy alongside the pathogen/KASP tools
- If that server is a single multipage app: copy `pages/*` and `data/*` into it (rename
  pages to avoid number collisions with existing pages).
- If separate apps: deploy this folder as its own app, same server/host.
- Streamlit Community Cloud: push to a GitHub repo, point Cloud at `Home.py`. **Public repo
  = public data** — the 4.4 MB genome-wide table is fully downloadable; deploy from a private
  repo (or gate behind the KASP auth) if any of this is pre-publication.

## Notes / known deployment gotchas
- `stmol` pulls a stale transitive dep — pin **`ipython_genutils`** explicitly (already in
  requirements.txt) or the import fails with `ModuleNotFoundError: ipython_genutils`.
- Page 1 (QC) renders the per-barcode table + pass-read bars natively; some run-level charts
  (cumulative yield, length histogram, coverage dist) are shown as raw JSON where the original
  chart geometry wasn't reconstructed — ask to have any of these rendered as native plots.
- All variant/structure data was extracted from the reports' inline JS payloads
  (`const DATA`, `const G`, `const FIGS`, and a JSON `<script>` tag).

## Caveats (surfaced on every page)
AlphaFold/ESMFold models, not experimental structures; variant calls against the
*P. cubensis* reference from a **draft** ONT assembly; low-pLDDT regions least reliable.
