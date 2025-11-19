import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "merged_cleaned.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "eda"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    return pd.read_csv(DATA_PATH)


def basic_info(df):
    print("\n=== BASIC DATA INFO ===")
    print(df.info())
    print("\nShape:", df.shape)
    print("\nColumns:", df.columns.tolist())


def missing_values(df):
    print("\n=== MISSING VALUES (%) ===")
    print((df.isna().mean() * 100).round(2))


def summary_stats(df):
    print("\n=== SUMMARY STATISTICS ===")
    print(df.describe().T)


def correlation_matrix(df):
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.corr(numeric_only=True), annot=False, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.savefig(OUTPUT_DIR / "correlation_matrix.png")
    plt.close()


def distplots(df):
    plt.figure(figsize=(10, 5))
    sns.histplot(df["GDP_pc"], bins=50)
    plt.title("GDP per Capita Distribution")
    plt.savefig(OUTPUT_DIR / "dist_gdp.png")
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.histplot(df["LE_0"], bins=50)
    plt.title("Life Expectancy at Birth Distribution")
    plt.savefig(OUTPUT_DIR / "dist_le0.png")
    plt.close()

def scatterplots(df):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="GDP_pc", y="LE_0", alpha=0.4)
    plt.title("GDP per Capita vs Life Expectancy at Birth")
    plt.xlabel("GDP per Capita (USD)")
    plt.ylabel("Life Expectancy at Birth")
    plt.tight_layout()
    plt.show()

def timeseries_examples(df):
    sample_countries = ["United States", "China", "India", "Germany"]

    for country in sample_countries:
        subset = df[df["Entity"] == country]

        plt.figure(figsize=(10, 5))
        plt.plot(subset["Year"], subset["GDP_pc"], label="GDP_pc")
        plt.title(f"GDP per Capita Over Time — {country}")
        plt.savefig(OUTPUT_DIR / f"gdp_ts_{country}.png")
        plt.close()

        plt.figure(figsize=(10, 5))
        plt.plot(subset["Year"], subset["LE_0"], label="LE_0")
        plt.title(f"Life Expectancy at Birth Over Time — {country}")
        plt.savefig(OUTPUT_DIR / f"le_ts_{country}.png")
        plt.close()


if __name__ == "__main__":
    df = load_data()

    basic_info(df)
    missing_values(df)
    summary_stats(df)

    correlation_matrix(df)
    distplots(df)
    scatterplots(df)
    timeseries_examples(df)

    print("\nEDA complete! Figures saved in:", OUTPUT_DIR)
