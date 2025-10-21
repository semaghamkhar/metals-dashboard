
import datetime as dt
import pandas as pd
from pathlib import Path

TEMPLATE = """# Weekly Metals Report – {week_ending}

**Summary (WoW %):**
{bullets}

## Detail
{table}

"""

def make_report(weekly_df: pd.DataFrame, out_dir: str = "reports") -> str:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    if weekly_df.empty:
        return ""
    last_week = weekly_df["Date"].max()
    week_ending = pd.to_datetime(last_week).date().isoformat()

    latest = weekly_df[weekly_df["Date"] == last_week].copy()
    latest = latest[["Symbol", "Close", "WoW_%", "MoM_%"]].sort_values("Symbol")
    bullets = "\n".join(
        f"- **{row.Symbol}**: close={row.Close:,.2f}, WoW={row['WoW_%']:+.2f}%, MoM={row['MoM_%']:+.2f}%"
        for _, row in latest.iterrows()
    )
    table = latest.to_markdown(index=False)

    md = TEMPLATE.format(week_ending=week_ending, bullets=bullets, table=table)
    out_path = Path(out_dir) / f"report_{week_ending}.md"
    out_path.write_text(md, encoding="utf-8")
    return str(out_path)
