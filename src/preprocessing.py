import os
from pathlib import Path
import pandas as pd
import numpy as np

# ---- PATHS ----
PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERIM_FILE = PROJECT_ROOT / "data" / "interim" / "lifeexp_gdp_merged.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_PATH = PROCESSED_DIR / "merged_cleaned.csv"


def load_merged():
    df = pd.read_csv(INTERIM_FILE)
    return df


def clean_column_names(df):
    rename_map = {
        "Life expectancy - Sex: total - Age: 0 - Type: period": "LE_0",
        "Life expectancy - Sex: total - Age: 10 - Type: period": "LE_10",
        "Life expectancy - Sex: total - Age: 15 - Type: period": "LE_15",
        "Life expectancy - Sex: total - Age: 25 - Type: period": "LE_25",
        "Life expectancy - Sex: total - Age: 45 - Type: period": "LE_45",
        "Life expectancy - Sex: total - Age: 65 - Type: period": "LE_65",
        "Life expectancy - Sex: total - Age: 80 - Type: period": "LE_80",
        "GDP per capita": "GDP_pc"
    }
    return df.rename(columns=rename_map)


def fix_dtypes(df):
    df["Year"] = df["Year"].astype(int)
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    return df


def drop_unnecessary_columns(df):
    cols_to_drop = [col for col in df.columns if "annotation" in col.lower()]
    return df.drop(columns=cols_to_drop, errors="ignore")


def filter_years(df):
    """Restrict dataset to reliable shared year range."""
    return df[(df["Year"] >= 1800) & (df["Year"] <= 2020)]


def handle_missing(df):
    le_cols = [c for c in df.columns if c.startswith("LE_")]
    df = df.dropna(subset=le_cols + ["GDP_pc"], how="all")
    df = df.sort_values(["Entity", "Year"])
    df[le_cols + ["GDP_pc"]] = df.groupby("Entity")[le_cols + ["GDP_pc"]].transform(
        lambda x: x.ffill().bfill()
    )
    return df


def remove_outliers(df):
    Q1 = df["GDP_pc"].quantile(0.25)
    Q3 = df["GDP_pc"].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df["GDP_pc"] >= lower) & (df["GDP_pc"] <= upper)]


def add_engineered_features(df):
    """Add log GDP, growth rates, and LE mean index."""
    # log GDP
    df["log_GDP_pc"] = np.log(df["GDP_pc"])

    # growth rates
    df["GDP_growth"] = df.groupby("Entity")["GDP_pc"].pct_change()
    df["LE_0_change"] = df.groupby("Entity")["LE_0"].diff()

    # LE mean
    le_cols = ["LE_0", "LE_10", "LE_15", "LE_25", "LE_45", "LE_65", "LE_80"]
    df["LE_mean"] = df[le_cols].mean(axis=1)

    return df


def add_normalised_features(df):
    df["GDP_pc_z"] = (df["GDP_pc"] - df["GDP_pc"].mean()) / df["GDP_pc"].std()
    df["LE_0_z"] = (df["LE_0"] - df["LE_0"].mean()) / df["LE_0"].std()
    df["GDP_pc_norm"] = (df["GDP_pc"] - df["GDP_pc"].min()) / (df["GDP_pc"].max() - df["GDP_pc"].min())
    df["LE_0_norm"] = (df["LE_0"] - df["LE_0"].min()) / (df["LE_0"].max() - df["LE_0"].min())
    return df


def save_processed(df):
    PROCESSED_DIR.mkdir(exist_ok=True, parents=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"\nProcessed dataset saved to: {PROCESSED_PATH}")


if __name__ == "__main__":
    print("Loading merged dataset...")
    df = load_merged()

    print("Cleaning column names...")
    df = clean_column_names(df)

    print("Fixing data types...")
    df = fix_dtypes(df)

    print("Dropping unnecessary metadata columns...")
    df = drop_unnecessary_columns(df)

    print("Filtering to shared reliable years (1800–2020)...")
    df = filter_years(df)

    print("Handling missing values...")
    df = handle_missing(df)

    print("Removing GDP outliers...")
    df = remove_outliers(df)

    print("Adding engineered features...")
    df = add_engineered_features(df)

    print("Adding normalised features...")
    df = add_normalised_features(df)

    print("Final sorting...")
    df = df.sort_values(["Entity", "Year"]).reset_index(drop=True)

    print("Saving processed dataset...")
    save_processed(df)

    print("\nPreprocessing complete!")
