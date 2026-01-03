"""Run ARIMA-based event study for one country.

Demo:
    python scripts/02_event_study.py --use-sample --country US

Outputs:
    results/tables/event_study_US.csv
    results/tables/event_study_summary_US.txt
"""
import sys
from pathlib import Path

# Ensure repo root is on PYTHONPATH so `import src...` works when running as a script
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


import argparse
from pathlib import Path
import pandas as pd

from src.config import PATHS, SIGNIFICANCE_LEVEL
from src.calendar import load_retrograde_periods
from src.data_loader import load_sample_returns, load_full_returns
from src.event_study import compute_abnormal_returns_arima_by_year


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--use-sample", action="store_true")
    p.add_argument("--raw-dir", type=str, default=str(PATHS.raw_dir))
    p.add_argument("--country", type=str, required=True)
    args = p.parse_args()

    if args.use_sample:
        df = load_sample_returns(str(PATHS.sample_returns_csv))
    else:
        df = load_full_returns(args.raw_dir)

    df = df[df["Country"] == args.country].copy()
    if df.empty:
        raise SystemExit(f"No rows found for country={args.country}")

    periods = load_retrograde_periods(str(PATHS.retrograde_periods_csv))
    out_map, pct = compute_abnormal_returns_arima_by_year(df[["Date","Return"]], periods, significance_level=SIGNIFICANCE_LEVEL)

    # Flatten outputs
    rows = []
    for (year, start, end), wdf in out_map.items():
        wdf = wdf.copy()
        wdf["year"] = year
        wdf["event_start"] = start
        wdf["event_end"] = end
        rows.append(wdf)
    if rows:
        out_df = pd.concat(rows, ignore_index=True)
    else:
        out_df = pd.DataFrame()

    PATHS.tables_dir.mkdir(parents=True, exist_ok=True)
    out_file = PATHS.tables_dir / f"event_study_{args.country}.csv"
    out_df.to_csv(out_file, index=False)

    summ_file = PATHS.tables_dir / f"event_study_summary_{args.country}.txt"
    with open(summ_file, "w", encoding="utf-8") as f:
        f.write(f"Country: {args.country}\n")
        f.write(f"Percentage of years with at least one significant CAR window (alpha={SIGNIFICANCE_LEVEL}): {pct:.2f}%\n")
        f.write(f"Number of event windows exported: {len(out_map)}\n")

    print(f"Wrote: {out_file}")
    print(f"Wrote: {summ_file}")


if __name__ == "__main__":
    main()
