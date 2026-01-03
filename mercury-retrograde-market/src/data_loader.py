"""Data loading utilities.

This repo ships with a small demo dataset:
  data/sample/world_indices_returns_sample.csv

For the full project, place your country Excel files under:
  data/raw/DM/*.xlsx
  data/raw/EM/*.xlsx
with columns: Date, Return
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_sample_returns(sample_csv: str) -> pd.DataFrame:
    df = pd.read_csv(sample_csv)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def load_returns_from_excel_folder(folder: Path, market_type: str) -> pd.DataFrame:
    """Load country return series from a folder of .xlsx files."""
    records = []
    for fp in sorted(folder.glob("*.xlsx")):
        tmp = pd.read_excel(fp)
        if "Date" not in tmp.columns or "Return" not in tmp.columns:
            raise ValueError(f"{fp} must contain columns ['Date','Return']")
        tmp = tmp[["Date","Return"]].dropna()
        tmp["Date"] = pd.to_datetime(tmp["Date"])
        tmp["Country"] = fp.stem
        tmp["Market_Type"] = market_type
        records.append(tmp)
    if not records:
        raise FileNotFoundError(f"No .xlsx files found in {folder}")
    return pd.concat(records, ignore_index=True)


def load_full_returns(raw_dir: str) -> pd.DataFrame:
    """Load full dataset from local raw directory (not committed)."""
    raw = Path(raw_dir)
    dm = load_returns_from_excel_folder(raw / "DM", "DM")
    em = load_returns_from_excel_folder(raw / "EM", "EM")
    return pd.concat([dm, em], ignore_index=True)
