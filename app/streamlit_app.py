
import os
import pandas as pd
import streamlit as st
from pathlib import Path
from app.data_fetch import add_wow_stats

st.set_page_config(page_title="Metals Dashboard", layout="wide")

st.title("Metals Dashboard · Copper · Silver · Platinum")

DATA_DIR = Path("data")
files = {
    "Copper (HG=F)": DATA_DIR / "prices_copper.csv",
    "Silver (SI=F)": DATA_DIR / "prices_silver.csv",
    "Platinum (PL=F)": DATA_DIR / "prices_platinum.csv",
}

dfs = []
for label, f in files.items():
    if f.exists():
        df = pd.read_csv(f, parse_dates=["Date"])
        df["Symbol"] = label.split()[0]  # Copper/Silver/Platinum
        dfs.append(df)

if not dfs:
    st.warning("No data yet. Wait for the first weekly run or run fetch_and_commit.py locally.")
    st.stop()

full = pd.concat(dfs, ignore_index=True)
full = full.sort_values(["Symbol", "Date"])
full = add_wow_stats(full)

st.subheader("Latest snapshot")
last_date = full["Date"].max().date().isoformat()
latest = full[full["Date"] == full["Date"].max()][["Symbol", "Close", "WoW_%", "MoM_%"]]
st.write(f"Week ending: **{last_date}**")
st.dataframe(latest.style.format({"Close": "{:,.2f}", "WoW_%": "{:+.2f}", "MoM_%": "{:+.2f}"}), use_container_width=True)

tab1, tab2 = st.tabs(["Charts", "History Table"])

with tab1:
    for sym in full["Symbol"].unique():
        sub = full[full["Symbol"] == sym]
        st.line_chart(sub.set_index("Date")["Close"], height=220, use_container_width=True)
        st.caption(f"{sym} – Close price history")
with tab2:
    st.dataframe(full.sort_values(["Symbol","Date"], ascending=[True, False]), use_container_width=True)
