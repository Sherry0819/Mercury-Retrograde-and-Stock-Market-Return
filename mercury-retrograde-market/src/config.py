"""Project configuration.

Edit these values to point to your local data if you have the full WRDS dataset.
The repository ships with a small sample dataset under data/sample/ for demo runs.
"""

from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Paths:
    repo_root: Path = Path(__file__).resolve().parents[1]
    data_dir: Path = repo_root / "data"
    sample_returns_csv: Path = data_dir / "sample" / "world_indices_returns_sample.csv"
    retrograde_periods_csv: Path = data_dir / "sample" / "mercury_retrograde_periods.csv"

    # Optional: place full datasets locally (not committed)
    raw_dir: Path = data_dir / "raw"
    processed_dir: Path = data_dir / "processed"

    results_dir: Path = repo_root / "results"
    tables_dir: Path = results_dir / "tables"
    figures_dir: Path = results_dir / "figures"

PATHS = Paths()

# Feature engineering
VOL_WINDOW_DAYS = 30
N_VOL_LAGS = 3

# Event study
SIGNIFICANCE_LEVEL = 0.05
