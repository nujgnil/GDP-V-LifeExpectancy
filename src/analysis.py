import pandas as pd

def latest_year(df: pd.DataFrame, strategy: str = "max_available", fixed_year: int | None = None) -> int:
    if strategy == "max_available":
        return int(df["year"].max())
    if fixed_year is not None:
        return int(fixed_year)
    return int(df["year"].max())

def global_trend(df: pd.DataFrame) -> pd.DataFrame:
    # Production-based CO2 summed by year
    if "co2" not in df.columns:
        raise ValueError("Column 'co2' not found.")
    return df.groupby("year", as_index=False)["co2"].sum().rename(columns={"co2":"co2_global"})

def top_emitters(df: pd.DataFrame, year: int, n: int = 20) -> pd.DataFrame:
    d = df[df["year"] == year]
    return (
        d.groupby("country", as_index=False)["co2"].sum()
         .sort_values("co2", ascending=False)
         .head(n)
         .reset_index(drop=True)
    )

def correlation_frame(df: pd.DataFrame, year: int) -> pd.DataFrame:
    # Data for scatter: CO2 per capita vs GDP
    cols = [c for c in ["country","year","co2_per_capita","gdp","population"] if c in df.columns]
    d = df[cols]
    d = d[(d["year"] == year) & d["co2_per_capita"].notna()]
    if "gdp" in d.columns:
        d = d[d["gdp"].notna()]
    return d
