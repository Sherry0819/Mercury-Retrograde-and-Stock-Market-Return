"""Prepare analysis dataset.

Demo (uses included sample):
    python scripts/00_prepare_data.py --use-sample

Full run (requires your local WRDS/Excel files):
    python scripts/00_prepare_data.py --raw-dir data/raw

Outputs:
    data/processed/analysis_dataset.csv
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

from src.config import PATHS, VOL_WINDOW_DAYS, N_VOL_LAGS
from src.calendar import load_retrograde_periods, add_mercury_retrograde_dummy
from src.data_loader import load_sample_returns, load_full_returns
from src.features import add_time_features, add_return_volatility, add_lagged_columns


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--use-sample", action="store_true", help="Use demo sample dataset bundled with repo.")
    p.add_argument("--raw-dir", type=str, default=str(PATHS.raw_dir), help="Local raw data directory (not committed).")
    p.add_argument("--out", type=str, default=str(PATHS.processed_dir / "analysis_dataset.csv"))
    args = p.parse_args()

    if args.use_sample:
        df = load_sample_returns(str(PATHS.sample_returns_csv))
    else:
        df = load_full_returns(args.raw_dir)

    periods = load_retrograde_periods(str(PATHS.retrograde_periods_csv))
    df = add_mercury_retrograde_dummy(df, periods, date_col="Date")
    df = add_time_features(df)
    df = add_return_volatility(df, window=VOL_WINDOW_DAYS, group_col="Country")
    df = add_lagged_columns(df, col="Return_Volatility", n_lags=N_VOL_LAGS, group_col="Country")

    # drop lag NA rows for clean regression
    df = df.dropna(subset=[f"Lagged_Return_Volatility_{k}" for k in range(1, N_VOL_LAGS + 1)])

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Wrote: {out_path}  (rows={len(df):,})")


if __name__ == "__main__":
    main()
