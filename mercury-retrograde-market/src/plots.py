"""Plotting helpers."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def save_volatility_plot(df: pd.DataFrame, out_path: str, title: str = "Volatility over time"):
    fig = plt.figure()
    plt.plot(df["Date"], df["Return_Volatility"])
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Rolling Volatility (std)")
    plt.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
