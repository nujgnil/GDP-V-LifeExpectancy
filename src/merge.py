# src/merge.py

import os
from pathlib import Path
import pandas as pd

# --- PATHS (edit if you ever move things) ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
GDP_CSV = PROJECT_ROOT / "data" / "raw" / "gdp-per-capita-maddison-project-database.csv"
LE_CSV  = PROJECT_ROOT / "data" / "raw" / "RLEADA.csv"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim"
INTERIM_PATH = INTERIM_DIR / "lifeexp_gdp_merged.csv"


def load_data():
    """Load raw GDP and Life Expectancy CSV files."""
    df_gdp = pd.read_csv(GDP_CSV)
    df_le  = pd.read_csv(LE_CSV)
    return df_le, df_gdp


def merge_datasets(df_le: pd.DataFrame, df_gdp: pd.DataFrame) -> pd.DataFrame:
    """
    Merge Life Expectancy and GDP datasets on Entity, Code and Year.
    Returns merged DataFrame.
    """
    merged = pd.merge(
        df_le,
        df_gdp,
        on=["Entity", "Code", "Year"],
        how="inner"
    )
    return merged


def save_interim(df_merged: pd.DataFrame, path: Path = INTERIM_PATH) -> None:
    """
    Save merged dataset to the interim directory.
    """
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    df_merged.to_csv(path, index=False)
    print(f"Merged dataset saved to: {path}")


if __name__ == "__main__":
    # 1) load
    df_le, df_gdp = load_data()

    # 2) merge
    df_merged = merge_datasets(df_le, df_gdp)

    # 3) basic info so you can see it worked
    print("Merged shape:", df_merged.shape)
    print(df_merged.head(10).to_string(index=False))

    # 4) save to data/interim
    save_interim(df_merged)
