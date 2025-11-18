import os
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

# ---- PATHS ----
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "merged_cleaned.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "analysis"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data() -> pd.DataFrame:
    """Load the cleaned merged dataset."""
    df = pd.read_csv(DATA_PATH)
    # Basic safety: drop rows with missing key vars
    df = df.dropna(subset=["GDP_pc", "log_GDP_pc", "LE_0"])
    return df


def compute_global_correlations(df: pd.DataFrame) -> None:
    """Compute Pearson and Spearman correlations between GDP and Life Expectancy."""
    cols = ["GDP_pc", "log_GDP_pc", "LE_0", "LE_mean"]
    existing = [c for c in cols if c in df.columns]

    corr_pearson = df[existing].corr(method="pearson")
    corr_spearman = df[existing].corr(method="spearman")

    print("\n=== GLOBAL CORRELATIONS (Pearson) ===")
    print(corr_pearson)
    print("\n=== GLOBAL CORRELATIONS (Spearman) ===")
    print(corr_spearman)

    corr_pearson.to_csv(OUTPUT_DIR / "correlations_pearson.csv")
    corr_spearman.to_csv(OUTPUT_DIR / "correlations_spearman.csv")


def regression_le_on_loggdp(df: pd.DataFrame) -> None:
    """
    Run OLS regression: Life Expectancy at birth (LE_0) ~ log(GDP per capita).
    Saves a text summary to outputs.
    """
    # Use most recent ~20 years to make it more relevant (optional)
    max_year = df["Year"].max()
    df_recent = df[df["Year"] >= max_year - 20].copy()

    y = df_recent["LE_0"]
    X = df_recent[["log_GDP_pc"]]
    X = sm.add_constant(X)  # add intercept

    model = sm.OLS(y, X, missing="drop")
    results = model.fit()

    print("\n=== OLS REGRESSION: LE_0 ~ log_GDP_pc (recent years) ===")
    print(results.summary())

    with open(OUTPUT_DIR / "regression_LE0_logGDP.txt", "w") as f:
        f.write(results.summary().as_text())


def add_decade_column(df: pd.DataFrame) -> pd.DataFrame:
    """Add a decade column (e.g., 1980, 1990, etc.)."""
    df["Decade"] = (df["Year"] // 10) * 10
    return df


def decade_level_trends(df: pd.DataFrame) -> None:
    """
    Compute decade-level average GDP and Life Expectancy,
    and their correlation over time.
    """
    df = add_decade_column(df)

    decade_means = (
        df.groupby("Decade")[["GDP_pc", "LE_0", "LE_mean"]]
        .mean()
        .reset_index()
    )

    print("\n=== DECADE-LEVEL AVERAGES ===")
    print(decade_means.head(15))

    decade_means.to_csv(OUTPUT_DIR / "decade_means.csv", index=False)

    # correlation between decade-mean GDP and LE
    corr_decade = decade_means[["GDP_pc", "LE_0", "LE_mean"]].corr()
    print("\n=== CORRELATION (DECADE-LEVEL MEANS) ===")
    print(corr_decade)

    corr_decade.to_csv(OUTPUT_DIR / "correlations_decade_means.csv")


def create_income_groups(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create income groups based on GDP per capita quartiles.
    Groups: Low, Lower-middle, Upper-middle, High.
    """
    # Use a recent year snapshot to define groups (e.g., last available year)
    snapshot_year = df["Year"].max()
    df_snapshot = df[df["Year"] == snapshot_year].copy()

    # Drop any NaN GDP
    df_snapshot = df_snapshot.dropna(subset=["GDP_pc"])

    # quartiles
    q1, q2, q3 = df_snapshot["GDP_pc"].quantile([0.25, 0.5, 0.75])

    def assign_group(gdp):
        if gdp <= q1:
            return "Low income"
        elif gdp <= q2:
            return "Lower-middle"
        elif gdp <= q3:
            return "Upper-middle"
        else:
            return "High income"

    df_snapshot["Income_group"] = df_snapshot["GDP_pc"].apply(assign_group)

    # Attach group back to full df (merge on Entity)
    df_groups = df.merge(
        df_snapshot[["Entity", "Income_group"]],
        on="Entity",
        how="left",
        suffixes=("", "_group")
    )

    # Save snapshot summary
    group_summary = (
        df_snapshot.groupby("Income_group")[["GDP_pc", "LE_0"]]
        .mean()
        .round(2)
        .reset_index()
        .sort_values("GDP_pc")
    )

    print("\n=== INCOME GROUP SUMMARY (latest year) ===")
    print(group_summary)

    group_summary.to_csv(OUTPUT_DIR / "income_group_summary_latest_year.csv", index=False)

    return df_groups


def find_outliers_residuals(df: pd.DataFrame, year: int = None, top_n: int = 10) -> None:
    """
    For a given year (or latest if None), fit LE_0 ~ log_GDP_pc and report
    top under/over-performers based on residuals.
    """
    if year is None:
        year = df["Year"].max()

    df_year = df[df["Year"] == year].dropna(subset=["LE_0", "log_GDP_pc"]).copy()

    if df_year.empty:
        print(f"\nNo data available for year {year} for outlier analysis.")
        return

    y = df_year["LE_0"]
    X = sm.add_constant(df_year["log_GDP_pc"])

    model = sm.OLS(y, X).fit()
    df_year["residual"] = model.resid  # actual - predicted

    # Over-performers: residual > 0 (live longer than predicted by GDP)
    over = df_year.sort_values("residual", ascending=False).head(top_n)
    under = df_year.sort_values("residual", ascending=True).head(top_n)

    print(f"\n=== OUTLIER ANALYSIS (Year {year}) ===")
    print("\nCountries with HIGHER LE than predicted (top over-performers):")
    print(over[["Entity", "GDP_pc", "LE_0", "residual"]])

    print("\nCountries with LOWER LE than predicted (top under-performers):")
    print(under[["Entity", "GDP_pc", "LE_0", "residual"]])

    over.to_csv(OUTPUT_DIR / f"overperformers_{year}.csv", index=False)
    under.to_csv(OUTPUT_DIR / f"underperformers_{year}.csv", index=False)


def main():
    print("Loading processed data...")
    df = load_data()

    print("Computing global correlations...")
    compute_global_correlations(df)

    print("Running regression LE_0 ~ log_GDP_pc...")
    regression_le_on_loggdp(df)

    print("Computing decade-level trends...")
    decade_level_trends(df)

    print("Creating income groups and summarising...")
    df_with_groups = create_income_groups(df)

    print("Finding outliers based on regression residuals (latest year)...")
    find_outliers_residuals(df_with_groups, year=None, top_n=10)

    print("\nAnalysis complete! Results saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
