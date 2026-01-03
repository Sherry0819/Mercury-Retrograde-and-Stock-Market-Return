"""Regression models used in the project."""

from __future__ import annotations

import pandas as pd
import statsmodels.formula.api as smf


def run_volatility_fe_regression(df: pd.DataFrame, n_lags: int = 3) -> object:
    """Fixed-effects OLS regression for volatility.

    Model:
        Return_Volatility ~ Mercury_Retrograde + lagged volatilities
                           + Country FE + Year_Quarter FE

    Returns
    -------
    statsmodels RegressionResultsWrapper
    """
    lag_terms = " + ".join([f"Lagged_Return_Volatility_{k}" for k in range(1, n_lags + 1)])
    formula = (
        "Return_Volatility ~ Mercury_Retrograde"
        + (f" + {lag_terms}" if lag_terms else "")
        + " + C(Country) + C(Year_Quarter)"
    )
    model = smf.ols(formula=formula, data=df).fit(cov_type="HC3")
    return model


def run_return_fe_regression(df: pd.DataFrame) -> object:
    """Optional: FE regression for returns (same FE structure)."""
    formula = "Return ~ Mercury_Retrograde + C(Country) + C(Year_Quarter)"
    model = smf.ols(formula=formula, data=df).fit(cov_type="HC3")
    return model


def tidy_params(model) -> pd.DataFrame:
    """Convert a statsmodels results object to a tidy coefficient table."""
    out = pd.DataFrame({
        "term": model.params.index,
        "coef": model.params.values,
        "std_err": model.bse.values,
        "t": model.tvalues.values,
        "p_value": model.pvalues.values,
    })
    return out
