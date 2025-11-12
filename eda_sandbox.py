# eda_lifeexp_gdp.py
import pandas as pd
from pathlib import Path

# ---- FILE PATHS (edit if needed) ----
GDP_CSV = r"C:/Users/Ling Jun/Desktop/PSB/Masters/DHV/Assignment/CW3/data/raw/gdp-per-capita-maddison-project-database.csv"
LE_CSV  = r"C:/Users/Ling Jun/Desktop/PSB/Masters/DHV/Assignment/CW3/data/raw/RLEADA.csv"

# ------------------------------
# Helpers to detect standard columns
# ------------------------------
def detect_country_col(df):
    for c in df.columns:
        cl = c.strip().lower()
        if cl in {"country", "entity", "location"}:
            return c
    # fallback: anything that looks like a name column (stringy with many uniques)
    obj_cols = df.select_dtypes(include="object").columns
    if len(obj_cols) > 0:
        return obj_cols[0]
    return None

def detect_year_col(df):
    for c in df.columns:
        if c.strip().lower() == "year":
            return c
    # fallback: any integer-like column with reasonable range
    for c in df.columns:
        if pd.api.types.is_integer_dtype(df[c]) and df[c].between(1800, 2100).mean() > 0.5:
            return c
    return None

def guess_value_col(df, keywords):
    # find first column whose name contains ALL keywords (case-insensitive)
    cand = []
    for c in df.columns:
        name = c.lower()
        if all(k in name for k in keywords):
            cand.append(c)
    if cand:
        return cand[0]
    # fallback: first numeric column (not year)
    num_cols = [c for c in df.select_dtypes(include="number").columns]
    ycol = detect_year_col(df)
    num_cols = [c for c in num_cols if c != ycol]
    return num_cols[0] if num_cols else None

def run_basic_eda(df, title):
    print("="*90)
    print(f"{title}: SHAPE/COLUMNS")
    print("="*90)
    print(df.shape)
    print(list(df.columns))
    print()

    # head
    print(f"{title}: HEAD(10)")
    print(df.head(10).to_string(index=False))
    print()

    # missingness
    print(f"{title}: MISSINGNESS (%)")
    miss = (df.isna().mean()*100).round(2).sort_values(ascending=False)
    print(miss.to_string())
    print()

    # numeric describe
    print(f"{title}: NUMERIC DESCRIBE")
    num_cols = df.select_dtypes(include="number").columns
    if len(num_cols):
        print(df[num_cols].describe().T.to_string())
    else:
        print("No numeric columns detected.")
    print()

    # country + year coverage (if present)
    ccol = detect_country_col(df)
    ycol = detect_year_col(df)
    if ccol:
        print(f"{title}: UNIQUE {ccol} COUNT")
        print(df[ccol].nunique(dropna=True))
        print(f"Top 15 {ccol} by row count:")
        print(df[ccol].value_counts().head(15).to_string())
        print()
    if ycol:
        print(f"{title}: YEAR RANGE")
        print(df[ycol].min(), "→", df[ycol].max())
        print("Year sample (first 10):")
        print(sorted(df[ycol].dropna().unique())[:10])
        print("Year sample (last 10):")
        print(sorted(df[ycol].dropna().unique())[-10:])
        print()

def print_merge_diagnostics(df_g, df_l):
    c_g, y_g = detect_country_col(df_g), detect_year_col(df_g)
    c_l, y_l = detect_country_col(df_l), detect_year_col(df_l)

    print("="*90)
    print("MERGE DIAGNOSTICS")
    print("="*90)
    print(f"GDP country col: {c_g} | year col: {y_g}")
    print(f"LE  country col: {c_l} | year col: {y_l}")
    if not all([c_g, y_g, c_l, y_l]):
        print("⚠️ Could not detect merge keys reliably. Check column names.")
        return

    # Basic normalization (strip spaces/case)
    g_countries = set(df_g[c_g].dropna().astype(str).str.strip())
    l_countries = set(df_l[c_l].dropna().astype(str).str.strip())
    common_countries = g_countries & l_countries

    g_years = set(pd.to_numeric(df_g[y_g], errors="coerce").dropna().astype(int))
    l_years = set(pd.to_numeric(df_l[y_l], errors="coerce").dropna().astype(int))
    common_years = sorted(g_years & l_years)

    print(f"Countries — GDP: {len(g_countries)} | LE: {len(l_countries)} | INTERSECTION: {len(common_countries)}")
    print(f"Years     — GDP: {len(g_years)} | LE: {len(l_years)} | INTERSECTION: {len(common_years)}")
    print(f"Common year range (if any): {common_years[:3]} ... {common_years[-3:]}" if common_years else "No common years detected.")
    if len(common_countries) < 10:
        # show a sample of matches/mismatches to debug naming issues
        only_g = sorted(list(g_countries - l_countries))[:10]
        only_l = sorted(list(l_countries - g_countries))[:10]
        print("\nSample countries only in GDP (first 10):", only_g)
        print("Sample countries only in LE  (first 10):", only_l)

def suggest_value_columns(df_g, df_l):
    # Try to guess the main value columns
    gdp_col = guess_value_col(df_g, keywords=["gdp", "per", "cap"])
    le_col  = guess_value_col(df_l, keywords=["life", "expect"])
    print("="*90)
    print("VALUE COLUMN SUGGESTIONS")
    print("="*90)
    print("GDP candidate value column:", gdp_col)
    print("LE  candidate value column:", le_col)
    if gdp_col:
        print("\nGDP sample (non-null):")
        print(df_g[[detect_country_col(df_g), detect_year_col(df_g), gdp_col]].dropna().head(10).to_string(index=False))
    if le_col:
        print("\nLE sample (non-null):")
        print(df_l[[detect_country_col(df_l), detect_year_col(df_l), le_col]].dropna().head(10).to_string(index=False))
    print()

# ------------------------------
# LOAD
# ------------------------------
df_GDP = pd.read_csv(GDP_CSV)
df_LE  = pd.read_csv(LE_CSV)

# ------------------------------
# EDA per dataset
# ------------------------------
run_basic_eda(df_GDP, title="GDP PER CAPITA (RAW)")
run_basic_eda(df_LE,  title="LIFE EXPECTANCY (RAW)")

# ------------------------------
# Merge diagnostics (keys & overlap)
# ------------------------------
print_merge_diagnostics(df_GDP, df_LE)

# ------------------------------
# Suggest likely value columns for each dataset
# ------------------------------
suggest_value_columns(df_GDP, df_LE)
