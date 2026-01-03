"""Run regressions and export tables.

Demo:
    python scripts/01_run_models.py --in data/processed/analysis_dataset.csv

Outputs:
    results/tables/volatility_regression_DM.csv
    results/tables/volatility_regression_EM.csv
    results/tables/return_regression_all.csv
    results/tables/*.txt (human-readable summaries)
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

from src.config import PATHS, N_VOL_LAGS
from src.regressions import run_volatility_fe_regression, run_return_fe_regression, tidy_params


def save_summary(model, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(model.summary().as_text())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_path", required=True, help="Prepared dataset CSV")
    args = p.parse_args()

    df = pd.read_csv(args.in_path)
    df["Date"] = pd.to_datetime(df["Date"])

    PATHS.tables_dir.mkdir(parents=True, exist_ok=True)

    # Volatility regressions by market type
    for mt in ["DM", "EM"]:
        sub = df[df["Market_Type"] == mt].copy()
        model = run_volatility_fe_regression(sub, n_lags=N_VOL_LAGS)
        tidy = tidy_params(model)
        tidy.to_csv(PATHS.tables_dir / f"volatility_regression_{mt}.csv", index=False)
        save_summary(model, PATHS.tables_dir / f"volatility_regression_{mt}.txt")

    # Optional: return regression on all markets
    m_ret = run_return_fe_regression(df)
    tidy_params(m_ret).to_csv(PATHS.tables_dir / "return_regression_all.csv", index=False)
    save_summary(m_ret, PATHS.tables_dir / "return_regression_all.txt")

    print(f"Saved tables to: {PATHS.tables_dir}")


if __name__ == "__main__":
    main()
