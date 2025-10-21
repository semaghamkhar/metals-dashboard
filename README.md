# Metals Dashboard (Copper · Silver · Platinum)

A production-ready **Streamlit** dashboard that updates **weekly** via **GitHub Actions**, pulls market data,
and shows **week-over-week** comparisons with auto-generated reports.

## What you get
- 📈 Streamlit app (`app/streamlit_app.py`) showing prices for **Copper (HG=F)**, **Silver (SI=F)**, **Platinum (PL=F)**
- 🔄 Weekly updater (`.github/workflows/weekly_update.yml`) running `fetch_and_commit.py` every **Sunday 06:00 UTC**
- 🗂️ Local history CSVs in `data/` committed weekly; Streamlit reads from these for **WoW** and historical charts
- 📝 Report generator (`app/report_writer.py`) — produces a weekly Markdown report in `reports/`
- 🧪 Uses **yfinance** for futures prices and **FRED** for macro indices (optional)

## Quick start (local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Deploy (Streamlit Cloud)
1. Push this folder to a public GitHub repo.
2. In Streamlit Cloud, set **Main file path** to `app/streamlit_app.py`.
3. (Optional) Set environment variable `FRED_API_KEY` for macro series.

## Scheduled weekly updates (GitHub Actions)
- Edit `.github/workflows/weekly_update.yml` if you want a different day/time.
- The workflow runs `python fetch_and_commit.py` to fetch *last week* close for each symbol and append to `data/*.csv`.
- Add a `FRED_API_KEY` GitHub secret if you use FRED series.

## Data sources
- Prices (front futures): **Yahoo Finance** symbols `HG=F`, `SI=F`, `PL=F`
- Macro (optional): FRED series like **DFF** (Fed Funds), **DTWEXBGS** (Broad USD Index)

## Notes
- Yahoo Finance data is provided “as is” (unofficial). If you need paid/official sources (LME, TradingEconomics, Nasdaq Data Link), extend `app/data_fetch.py`.
- The app computes **WoW** and **MoM** deltas and can export a **weekly Markdown report**.

## Folder structure
```
metals-dashboard/
  app/
    streamlit_app.py
    data_fetch.py
    report_writer.py
  data/
    prices_copper.csv
    prices_silver.csv
    prices_platinum.csv
    macro_fred.csv
  reports/
  fetch_and_commit.py
  requirements.txt
  .env.example
  .github/workflows/weekly_update.yml
  README.md
```
