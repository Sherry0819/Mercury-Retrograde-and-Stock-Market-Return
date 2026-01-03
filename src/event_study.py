"""Event study utilities (ARIMA-based abnormal returns + CAR)."""

from __future__ import annotations

import pandas as pd
from scipy import stats
from pmdarima import auto_arima


def compute_abnormal_returns_arima_by_year(
    df: pd.DataFrame,
    retrograde_periods: pd.DataFrame,
    significance_level: float = 0.05,
):
    """Compute abnormal returns and CAR within each retrograde window.

    This follows the approach used in the original notebook:
    - For each year, fit an ARIMA model to that year's daily returns
    - Predict in-sample 'normal' returns
    - Abnormal return = actual - normal
    - CAR = cumulative sum of abnormal returns over the window
    - Test whether CAR differs from 0 (one-sample t-test)

    Parameters
    ----------
    df : DataFrame with columns [Date, Return] for ONE country
    retrograde_periods : DataFrame with columns [start, end, year]
    significance_level : alpha for significance

    Returns
    -------
    dict mapping (year, start, end) -> DataFrame with Return, Normal_Return, Abnormal_Return, CAR
    float percentage of years with at least one significant retrograde window
    """
    series = df.copy()
    series["Date"] = pd.to_datetime(series["Date"])
    series = series.sort_values("Date").set_index("Date")

    abnormal_returns = {}
    significant_years_count = 0
    years = sorted(series.index.year.unique())
    total_years = len(years)

    for year in years:
        yearly = series.loc[str(year)].copy()
        if yearly.empty or yearly["Return"].dropna().shape[0] < 30:
            continue

        periods = retrograde_periods[retrograde_periods["start"].dt.year == year]
        if periods.empty:
            continue

        # auto-ARIMA on the year's returns
        auto_model = auto_arima(
            yearly["Return"],
            seasonal=False,
            stepwise=True,
            suppress_warnings=True,
            error_action="ignore",
            max_p=3, max_q=3, d=None,
        )
        best_model = auto_model.fit(yearly["Return"])
        yearly["Normal_Return"] = best_model.predict_in_sample()

        event_returns = []
        non_event_returns = yearly["Return"].tolist()
        year_significant = False

        for _, r in periods.iterrows():
            start_date = r["start"]
            end_date = r["end"]
            window = yearly.loc[start_date:end_date].copy()
            if window.empty:
                continue

            window["Abnormal_Return"] = window["Return"] - window["Normal_Return"]
            window["CAR"] = window["Abnormal_Return"].cumsum()

            event_returns.extend(window["Return"].tolist())

            # remove window days from non-event set
            mask = ~yearly.index.isin(window.index)
            non_event_returns = yearly.loc[mask, "Return"].tolist()

            abnormal_returns[(year, start_date.date().isoformat(), end_date.date().isoformat())] = window[
                ["Return","Normal_Return","Abnormal_Return","CAR"]
            ].reset_index()

            # significance on CAR series vs 0
            t_stat, p = stats.ttest_1samp(window["CAR"], 0)
            if p < significance_level:
                year_significant = True
                break

        if year_significant:
            significant_years_count += 1

    percentage_significant_years = (significant_years_count / total_years) * 100 if total_years else 0.0
    return abnormal_returns, percentage_significant_years
