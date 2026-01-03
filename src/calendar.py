"""Mercury retrograde calendar utilities."""

from __future__ import annotations

import pandas as pd


def load_retrograde_periods(periods_csv: str) -> pd.DataFrame:
    """Load retrograde periods from CSV.

    CSV columns: year, start, end (YYYY-MM-DD)
    """
    df = pd.read_csv(periods_csv)
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])
    return df


def add_mercury_retrograde_dummy(df: pd.DataFrame, periods: pd.DataFrame, date_col: str = "Date") -> pd.DataFrame:
    """Add Mercury_Retrograde dummy (0/1) based on event windows.

    Parameters
    ----------
    df : DataFrame with a date column
    periods : DataFrame with columns start, end
    date_col : name of the date column in df

    Returns
    -------
    Copy of df with Mercury_Retrograde column.
    """
    out = df.copy()
    out[date_col] = pd.to_datetime(out[date_col])
    out["Mercury_Retrograde"] = 0

    # Vectorized-ish: build a boolean mask by OR-ing each period
    mask = pd.Series(False, index=out.index)
    for _, r in periods.iterrows():
        mask |= (out[date_col] >= r["start"]) & (out[date_col] <= r["end"])
    out.loc[mask, "Mercury_Retrograde"] = 1
    return out
