import pandas as pd

def clean_temperature_anomaly(
    df: pd.DataFrame,
    *,
    year_min: int = 1900,
    expected_year_col: str | None = None,
    expected_value_col: str | None = None,
    expected_region_col: str | None = None
) -> pd.DataFrame:
    """
    Normalizes a temperature anomaly dataset to columns:
      ['region', 'year', 'anomaly']

    Tries to auto-detect common header names if not provided.
    """

    df = df.copy()

    # --- auto-detect columns if not specified ---
    def pick(col_candidates):
        for c in col_candidates:
            if c in df.columns:
                return c
        return None

    year_col = expected_year_col or pick(["year", "Year", "date", "Date"])
    value_col = expected_value_col or pick(["anomaly","temp_anomaly","value","Anomaly","TempAnomaly","Temperature_Anomaly"])
    region_col = expected_region_col or pick(["region","Region","area","Area","country","Country","entity","Entity"])

    # minimal validation
    missing = [n for n, c in {"year": year_col, "anomaly": value_col}.items() if c is None]
    if missing:
        raise ValueError(f"Missing required columns in CSV (could not detect): {', '.join(missing)}")

    # --- normalize types ---
    df[year_col] = pd.to_numeric(df[year_col], errors="coerce").astype("Int64")
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")

    if region_col:
        df[region_col] = df[region_col].astype("string").str.strip()
    else:
        # fallback single region if not present
        region_col = "_region"
        df[region_col] = "Global"

    # --- select & rename to canonical schema ---
    out = df[[region_col, year_col, value_col]].rename(
        columns={region_col: "region", year_col: "year", value_col: "anomaly"}
    )

    # --- filter & clean ---
    out = out[out["year"].notna()]
    out = out[out["year"] >= year_min]
    out = out.dropna(subset=["anomaly"])
    out = out.drop_duplicates().sort_values(["region","year"]).reset_index(drop=True)

    return out

clean_temperature_anomaly()

