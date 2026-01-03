"""Feature engineering utilities."""

from __future__ import annotations

import pandas as pd


def add_time_features(df: pd.DataFrame, date_col: str = "Date") -> pd.DataFrame:
    out = df.copy()
    out[date_col] = pd.to_datetime(out[date_col])
    out["Year"] = out[date_col].dt.year
    out["Quarter"] = out[date_col].dt.quarter
    out["Year_Quarter"] = out["Year"].astype(str) + "Q" + out["Quarter"].astype(str)
    return out


def add_return_volatility(
    df: pd.DataFrame,
    window: int = 30,
    group_col: str = "Country",
    return_col: str = "Return",
    out_col: str = "Return_Volatility",
) -> pd.DataFrame:
    """Rolling std dev of returns (per country)."""
    out = df.copy()
    out[out_col] = (
        out.groupby(group_col)[return_col]
        .rolling(window=window, min_periods=1)
        .std()
        .reset_index(level=0, drop=True)
    )
    return out


def add_lagged_columns(
    df: pd.DataFrame,
    col: str,
    n_lags: int = 3,
    group_col: str = "Country",
    prefix: str | None = None,
) -> pd.DataFrame:
    out = df.copy()
    prefix = prefix or f"Lagged_{col}"
    for k in range(1, n_lags + 1):
        out[f"{prefix}_{k}"] = out.groupby(group_col)[col].shift(k)
    return out
