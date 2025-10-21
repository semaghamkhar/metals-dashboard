
import os
import sys
from pathlib import Path
import datetime as dt
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent / "app"))
from data_fetch import fetch_yf, weekly_snapshot, add_wow_stats

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

SYMS = {
    "copper": "HG=F",
    "silver": "SI=F",
    "platinum": "PL=F",
}

def append_weekly(symbol_key: str, yf_symbol: str, csv_path: Path) -> None:
    # Fetch last 2 months to ensure latest Friday is included
    start = (dt.date.today() - dt.timedelta(days=70)).isoformat()
    df = fetch_yf(yf_symbol, start=start)
    if df.empty:
        print(f"[WARN] No data for {yf_symbol}")
        return
    w = weekly_snapshot(df)
    w = w.rename(columns={"Close":"Close"})
    if csv_path.exists():
        hist = pd.read_csv(csv_path, parse_dates=["Date"])
        # avoid duplicates
        merged = pd.concat([hist, w[["Date","Close"]]], ignore_index=True).drop_duplicates(["Date"], keep="last")
    else:
        merged = w[["Date","Close"]]
    merged = merged.sort_values("Date")
    merged.to_csv(csv_path, index=False)
    print(f"[OK] Updated {csv_path.name} -> rows={len(merged)}")

def main():
    append_weekly("copper", SYMS["copper"], DATA_DIR / "prices_copper.csv")
    append_weekly("silver", SYMS["silver"], DATA_DIR / "prices_silver.csv")
    append_weekly("platinum", SYMS["platinum"], DATA_DIR / "prices_platinum.csv")

if __name__ == "__main__":
    main()
