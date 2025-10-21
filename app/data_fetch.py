
import os
import io
import datetime as dt
from typing import List, Optional
import pandas as pd
import yfinance as yf
import requests

FRED_API = "https://api.stlouisfed.org/fred/series/observations"

def fetch_yf(symbol: str, start: str = "2015-01-01", end: Optional[str] = None) -> pd.DataFrame:
    end = end or dt.date.today().isoformat()
    df = yf.download(symbol, start=start, end=end, progress=False)
    if df.empty:
        return pd.DataFrame()
    df = df.reset_index()[["Date", "Close"]]
    df["Symbol"] = symbol
    return df

def fred_series(series_id: str, start_date: str = "2015-01-01", api_key: Optional[str] = None) -> pd.DataFrame:
    api_key = api_key or os.getenv("FRED_API_KEY", "")
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start_date,
    }
    r = requests.get(FRED_API, params=params, timeout=30)
    r.raise_for_status()
    js = r.json()
    obs = js.get("observations", [])
    df = pd.DataFrame(obs)
    if df.empty:
        return pd.DataFrame()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.rename(columns={"date": "Date", "value": "Value"})
    df = df[["Date", "Value"]]
    df["Series"] = series_id
    return df

def weekly_snapshot(prices_df: pd.DataFrame) -> pd.DataFrame:
    # Resample to weekly (Friday close). If not available, take last available
    df = prices_df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    out = []
    for sym, g in df.groupby("Symbol"):
        g = g.set_index("Date").sort_index()
        w = g["Close"].resample("W-FRI").last().dropna().to_frame("Close").reset_index()
        w["Symbol"] = sym
        out.append(w)
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()

def add_wow_stats(weekly_df: pd.DataFrame) -> pd.DataFrame:
    df = weekly_df.copy()
    df = df.sort_values(["Symbol", "Date"])
    df["WoW_%"] = df.groupby("Symbol")["Close"].pct_change() * 100
    df["MoM_%"] = df.groupby("Symbol")["Close"].pct_change(4) * 100
    return df

def ensure_columns(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    for c in cols:
        if c not in df.columns: df[c] = pd.NA
    return df[cols]
