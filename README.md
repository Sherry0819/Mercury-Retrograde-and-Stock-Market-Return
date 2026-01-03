# Mercury Retrograde and Stock Market Dynamics

This repository packages a **behavioral finance** group project studying whether a widely-held symbolic belief
(Mercury retrograde) is associated with systematic changes in market **volatility** and **returns**.

The repo is organized as a small, reproducible pipeline:
1. **Prepare data** (load returns, build Mercury retrograde indicator, engineer volatility features)
2. **Run models** (fixed-effects regressions for volatility/returns; Developed vs Emerging)
3. **Event study** (ARIMA-based abnormal returns + CAR within retrograde windows)
4. **Export tables/figures** for presentation and GitHub display

> **Data note**: the full WRDS/world-index dataset is not committed to GitHub.  
> This repo includes a small **sample dataset** under `data/sample/` so the pipeline can be demonstrated end-to-end.

## Repository Structure

```
src/            # reusable modules (calendar, features, regressions, event study)
scripts/        # runnable pipeline entrypoints
notebooks/      # original project notebooks (kept for reference)
data/sample/    # small demo dataset + retrograde calendar CSV
results/        # generated tables/figures (not required for version control)
docs/           # paper draft and presentation slides
```

## Quickstart

### 0) Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 1) Prepare dataset (demo sample)
```bash
python scripts/00_prepare_data.py --use-sample
```

This writes:
- `data/processed/analysis_dataset.csv`

### 2) Run regressions
```bash
python scripts/01_run_models.py --in data/processed/analysis_dataset.csv
```

Outputs (CSV + readable TXT summaries):
- `results/tables/volatility_regression_DM.*`
- `results/tables/volatility_regression_EM.*`
- `results/tables/return_regression_all.*`

### 3) Event study (ARIMA abnormal returns + CAR)
```bash
python scripts/02_event_study.py --use-sample --country US
```

Outputs:
- `results/tables/event_study_US.csv`
- `results/tables/event_study_summary_US.txt`

## Methods (high level)

- **Belief indicator**: retrograde windows are encoded from a public calendar (see `data/sample/mercury_retrograde_periods.csv`)
- **Volatility**: rolling standard deviation of returns (default 30 trading days), plus lag terms
- **Regression**: fixed effects for Country and Year-Quarter; heteroskedasticity-robust SE (HC3)
- **Event study**: per-year ARIMA model for “normal” returns; abnormal return = actual − predicted; CAR within event windows

## Data availability

If your original dataset is proprietary (e.g., WRDS exports or internal data), **do not commit it**.
Place it locally under `data/raw/` with:
- `data/raw/DM/*.xlsx`
- `data/raw/EM/*.xlsx`

Each file should have columns: `Date`, `Return`

Then run:
```bash
python scripts/00_prepare_data.py --raw-dir data/raw
```

## My contribution (edit as needed)

- Organized the end-to-end pipeline and refactored notebook logic into reusable modules
- Implemented volatility features, fixed-effects regressions, and ARIMA-based event study
- Added a small demo dataset and clear reproduction steps for portfolio use
