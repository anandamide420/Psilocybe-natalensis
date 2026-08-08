# Deploying to Streamlit Community Cloud

This app is a self-contained multipage Streamlit app. Community Cloud deploys it
straight from a GitHub repo — no server admin.

## Recommended: a NEW dedicated repo (keep it separate from the KASP app)

A separate repo means this portal has its own privacy setting, its own requirements,
and its own URL — it won't disturb the pathogen/KASP app. You deploy it as a *second*
app under the same Community Cloud account (the free tier allows multiple apps).

### 1. Make the repo (from ~/Desktop/psilo_streamlit)
```bash
cd ~/Desktop/psilo_streamlit
git init
git add .
git commit -m "Psilocybe natalensis genome portal — Streamlit app"
# create an EMPTY repo on github.com first (e.g. psilo-natalensis-portal), then:
git remote add origin https://github.com/<YOUR_USER>/psilo-natalensis-portal.git
git branch -M main
git push -u origin main
```
The 5.1 MB and 4.2 MB data files push fine — both are under GitHub's 50 MB soft /
100 MB hard limit, so no Git LFS is needed.

### 2. Deploy on Community Cloud
1. Go to https://share.streamlit.io → **Create app** → **Deploy a public app from GitHub**.
2. Repository: `<YOUR_USER>/psilo-natalensis-portal`; Branch: `main`; **Main file path: `Home.py`**.
3. Open **Advanced settings** → set **Python version to 3.12** (see gotcha below).
4. Click **Deploy**. First build installs requirements.txt (~2–3 min). You get a URL like
   `https://psilo-natalensis-portal.streamlit.app`.

The four analyses appear in the left sidebar automatically (Community Cloud reads the
`pages/` folder). Page 4's 3D viewer renders live in the browser.

## Privacy — decide before you push
- **Public repo + public app** (what you asked for): everything is open, including the raw
  data files on GitHub and the CSV download on page 3. Simplest.
- **Private repo + public app**: Community Cloud can deploy from a private repo while the app
  itself stays publicly viewable. This hides the raw JSON/CSV from GitHub browsing, though the
  page-3 CSV-download button still hands out the table. Use this if you want the *app* public
  but the *source data files* not directly downloadable from the repo.
- **Private app (viewer allow-list)**: in the app's Settings → Sharing, restrict to specific
  Google/email accounts. Use this if it should stay internal for now.

## Gotchas (all already handled in requirements.txt / files)
- **`ipython_genutils` is pinned** — stmol's stale transitive dependency; without it the
  3D page throws `ModuleNotFoundError` at import.
- **Python 3.12** — set it in Advanced settings. `ipython_genutils` is an old package; 3.12 is
  the safe choice. If the build errors on 3.13, this is why.
- **3Dmol.js loads from a CDN at view time** — Community Cloud has internet, so fine. (Only an
  issue on an air-gapped host.)
- **`.gitignore`** excludes `.venv/`, `__pycache__/`, and `.streamlit/secrets.toml` so you don't
  commit a local venv or any secrets.

## Adding it INTO the existing KASP repo instead (alternative)
If you'd rather have one app with KASP + these pages in the same sidebar:
1. Copy `pages/*.py` into the KASP repo's `pages/` folder — **renumber** if it already has a
   `1_*.py` / `2_*.py` (filename number = sidebar order).
2. Copy `data/*.json` into the KASP repo (adjust the `DATA_PATH` in each page if your data
   folder isn't a sibling of `pages/`).
3. Merge these `requirements.txt` lines into the KASP repo's requirements.
4. `git push` — Community Cloud auto-redeploys the existing app.
Downside: the two tools then share one privacy setting and one URL.
