from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D)


# ---------- PATHS ----------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "merged_cleaned.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------- HELPERS ----------
def load_data() -> pd.DataFrame:
    """Load the cleaned merged dataset."""
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=["GDP_pc", "LE_0"])
    return df


def create_income_groups(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """
    Create income groups based on GDP per capita quartiles
    in the latest year available: Low, Lower-middle, Upper-middle, High.
    """
    latest_year = df["Year"].max()
    snapshot = df[df["Year"] == latest_year].dropna(subset=["GDP_pc"]).copy()

    q1, q2, q3 = snapshot["GDP_pc"].quantile([0.25, 0.5, 0.75])

    def assign_group(g):
        if g <= q1:
            return "Low income"
        elif g <= q2:
            return "Lower-middle"
        elif g <= q3:
            return "Upper-middle"
        else:
            return "High income"

    snapshot["Income_group"] = snapshot["GDP_pc"].apply(assign_group)

    df = df.merge(snapshot[["Entity", "Income_group"]], on="Entity", how="left")

    return df, latest_year


# ---------- 2D PLOTS ----------
def plot_global_trends(df: pd.DataFrame) -> None:
    """
    Global average trends over time for LE_0 and GDP_pc.
    Saves two figures, each with annotations.
    """
    grouped = (
        df.groupby("Year")[["LE_0", "GDP_pc"]]
        .mean()
        .reset_index()
        .sort_values("Year")
    )

    # ---------- Life Expectancy trend ----------
    plt.figure(figsize=(10, 5))
    plt.plot(grouped["Year"], grouped["LE_0"])
    plt.xlabel("Year")
    plt.ylabel("Life Expectancy at Birth (years)")
    plt.title("Global Average Life Expectancy at Birth Over Time")

    # annotate early and late points
    start = grouped.iloc[0]
    end = grouped.iloc[-1]

    plt.annotate(
        f"{int(start['Year'])}: {start['LE_0']:.1f} years",
        xy=(start["Year"], start["LE_0"]),
        xytext=(start["Year"] + 15, start["LE_0"] - 5),
        arrowprops=dict(arrowstyle="->", linewidth=1),
    )

    plt.annotate(
        f"{int(end['Year'])}: {end['LE_0']:.1f} years",
        xy=(end["Year"], end["LE_0"]),
        xytext=(end["Year"] - 60, end["LE_0"] - 10),
        arrowprops=dict(arrowstyle="->", linewidth=1),
    )

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "trend_global_LE0.png", dpi=300)
    plt.close()

    # ---------- GDP per capita trend ----------
    plt.figure(figsize=(10, 5))
    plt.plot(grouped["Year"], grouped["GDP_pc"])
    plt.xlabel("Year")
    plt.ylabel("GDP per Capita (USD)")
    plt.title("Global Average GDP per Capita Over Time")

    start_g = grouped.iloc[0]
    end_g = grouped.iloc[-1]

    plt.annotate(
        f"{int(start_g['Year'])}: ${start_g['GDP_pc']:.0f}",
        xy=(start_g["Year"], start_g["GDP_pc"]),
        xytext=(start_g["Year"] + 15, start_g["GDP_pc"] + 1000),
        arrowprops=dict(arrowstyle="->", linewidth=1),
    )

    plt.annotate(
        f"{int(end_g['Year'])}: ${end_g['GDP_pc']:.0f}",
        xy=(end_g["Year"], end_g["GDP_pc"]),
        xytext=(end_g["Year"] - 60, end_g["GDP_pc"] - 2000),
        arrowprops=dict(arrowstyle="->", linewidth=1),
    )

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "trend_global_GDPpc.png", dpi=300)
    plt.close()



def plot_scatter_latest_year(df: pd.DataFrame) -> None:
    """
    Scatter: GDP per capita vs Life Expectancy (latest year),
    with a best-fit curve based on LE_0 ~ log(GDP_pc),
    and a log(GDP) version with a straight best-fit line.
    Includes annotations to highlight key regions.
    """
    latest_year = df["Year"].max()
    snap = df[df["Year"] == latest_year].dropna(subset=["GDP_pc", "LE_0"]).copy()
    snap = snap[snap["GDP_pc"] > 0]  # log requires positive values

    x_gdp = snap["GDP_pc"].values
    y_le = snap["LE_0"].values
    log_x = np.log(x_gdp)

    # fit in log space: LE_0 = intercept + slope * log(GDP)
    slope, intercept = np.polyfit(log_x, y_le, 1)

    # ---------- 1) Raw GDP axis with curved log fit ----------
    plt.figure(figsize=(8, 6))
    plt.scatter(x_gdp, y_le, alpha=0.5, label="Country (latest year)")

    x_line = np.linspace(x_gdp.min(), x_gdp.max(), 200)
    y_line = intercept + slope * np.log(x_line)
    plt.plot(x_line, y_line, color="red", linewidth=2,
             label="Best fit: LE₀ ~ log(GDP per capita)")

    # annotate typical low-income / high-income regions
    low_x = np.percentile(x_gdp, 10)
    low_y = np.percentile(y_le, 10)
    plt.annotate(
        "Low income,\nshorter lives",
        xy=(low_x, low_y),
        xytext=(low_x * 2, low_y - 5),
        arrowprops=dict(arrowstyle="->", linewidth=1),
    )

    high_x = np.percentile(x_gdp, 90)
    high_y = np.percentile(y_le, 90)
    plt.annotate(
        "High income,\nlonger lives",
        xy=(high_x, high_y),
        xytext=(high_x * 0.6, high_y + 3),
        arrowprops=dict(arrowstyle="->", linewidth=1),
    )

    plt.xlabel("GDP per Capita (USD)")
    plt.ylabel("Life Expectancy at Birth (years)")
    plt.title(f"GDP per Capita vs Life Expectancy at Birth ({latest_year})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f"scatter_GDPpc_LE0_{latest_year}.png", dpi=300)
    plt.close()

    # ---------- 2) Log(GDP) axis with straight line ----------
    plt.figure(figsize=(8, 6))
    plt.scatter(log_x, y_le, alpha=0.5, label="Country (latest year)")

    log_x_line = np.linspace(log_x.min(), log_x.max(), 200)
    y_line_log = intercept + slope * log_x_line
    plt.plot(log_x_line, y_line_log, color="red", linewidth=2,
             label="Best-fit line")

    # annotate diminishing returns area
    mid_log = np.median(log_x)
    mid_y = intercept + slope * mid_log
    plt.annotate(
        "Relationship becomes\nflatter at high incomes",
        xy=(log_x.max(), y_line_log[-1]),
        xytext=(mid_log, mid_y + 5),
        arrowprops=dict(arrowstyle="->", linewidth=1),
    )

    plt.xlabel("log(GDP per Capita)")
    plt


def plot_income_group_boxplot(df: pd.DataFrame) -> None:
    """
    Boxplot of Life Expectancy by income group (latest year),
    with median values annotated for each group.
    """
    df, latest_year = create_income_groups(df)
    snap = df[df["Year"] == latest_year].dropna(subset=["LE_0", "Income_group"])

    order = ["Low income", "Lower-middle", "Upper-middle", "High income"]
    data = [snap[snap["Income_group"] == g]["LE_0"] for g in order]

    plt.figure(figsize=(8, 6))
    box = plt.boxplot(data, labels=order, showfliers=False)
    plt.xlabel("Income Group")
    plt.ylabel("Life Expectancy at Birth (years)")
    plt.title(f"Life Expectancy by Income Group ({latest_year})")

    # compute and annotate medians for each group
    medians = [np.median(d) for d in data]

    for i, (group, median_val) in enumerate(zip(order, medians), start=1):
        plt.annotate(
            f"Median ≈ {median_val:.1f}",
            xy=(i, median_val),
            xytext=(i, median_val + 3),  # adjust +3 if labels overlap
            ha="center",
            arrowprops=dict(arrowstyle="->", linewidth=1),
        )

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f"boxplot_LE0_income_groups_{latest_year}.png", dpi=300)
    plt.close()




def plot_country_trajectories_2d(df: pd.DataFrame) -> None:
    countries = ["United States", "China", "India", "Germany", "Brazil", "South Africa"]
    df_sel = df[df["Entity"].isin(countries)].copy()

    plt.figure(figsize=(10, 6))
    for c in countries:
        sub = df_sel[df_sel["Entity"] == c].sort_values("Year")
        if sub.empty:
            continue
        plt.plot(sub["Year"], sub["LE_0"], label=c)

        # annotate start and end for China and India as examples
        if c in ["China", "India"]:
            start = sub.iloc[0]
            end = sub.iloc[-1]
            plt.annotate(
                f"{c} ({int(start['Year'])})",
                xy=(start["Year"], start["LE_0"]),
                xytext=(start["Year"] - 10, start["LE_0"] - 5),
                arrowprops=dict(arrowstyle="->", linewidth=1),
            )
            plt.annotate(
                f"{c} ({int(end['Year'])})",
                xy=(end["Year"], end["LE_0"]),
                xytext=(end["Year"] - 20, end["LE_0"] + 3),
                arrowprops=dict(arrowstyle="->", linewidth=1),
            )

    plt.xlabel("Year")
    plt.ylabel("Life Expectancy at Birth (years)")
    plt.title("Life Expectancy Over Time — Selected Countries")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "ts_LE0_selected_countries.png", dpi=300)
    plt.close()



# ---------- 3D PLOTS ----------
def plot_3d_gdp_le_year(df: pd.DataFrame) -> None:
    """
    3D scatter: log(GDP_pc) vs LE_0 vs Year.
    Shows how the GDP–LE relationship evolves over time.
    """
    df3 = df.dropna(subset=["GDP_pc", "LE_0"]).copy()
    df3 = df3[df3["GDP_pc"] > 0]
    df3["log_GDP_pc"] = np.log(df3["GDP_pc"])

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(df3["log_GDP_pc"], df3["LE_0"], df3["Year"], alpha=0.3, s=5)
    ax.set_xlabel("log(GDP per Capita)")
    ax.set_ylabel("Life Expectancy at Birth (years)")
    ax.set_zlabel("Year")
    ax.set_title("3D: log(GDP), Life Expectancy, and Time")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "3d_logGDP_LE0_Year.png", dpi=300)
    plt.close()


def plot_3d_gdp_le_growth(df: pd.DataFrame) -> None:
    """
    3D scatter: log(GDP_pc) vs LE_0 vs GDP_growth.
    Shows where rapid growth occurs in GDP–LE space.
    """
    if "GDP_growth" not in df.columns:
        print("GDP_growth not found in dataframe; skipping 3D GDP growth plot.")
        return

    df3 = df.dropna(subset=["GDP_pc", "LE_0", "GDP_growth"]).copy()
    df3 = df3[df3["GDP_pc"] > 0]
    df3["log_GDP_pc"] = np.log(df3["GDP_pc"])

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(df3["log_GDP_pc"], df3["LE_0"], df3["GDP_growth"], alpha=0.3, s=5)
    ax.set_xlabel("log(GDP per Capita)")
    ax.set_ylabel("Life Expectancy at Birth (years)")
    ax.set_zlabel("GDP Growth (year-on-year, fraction)")
    ax.set_title("3D: log(GDP), Life Expectancy, and GDP Growth")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "3d_logGDP_LE0_GDPgrowth.png", dpi=300)
    plt.close()


def plot_3d_age_le_gdp(df: pd.DataFrame) -> None:
    """
    3D plot of Age, LE_at_age, and log(GDP_pc).
    Uses a snapshot of the latest year to illustrate age profiles by income.
    """
    # check required LE columns
    le_cols = ["LE_0", "LE_10", "LE_15", "LE_25", "LE_45", "LE_65", "LE_80"]
    for c in le_cols:
        if c not in df.columns:
            print("Some LE_* columns missing; skipping 3D age profile plot.")
            return

    latest_year = df["Year"].max()
    snap = df[df["Year"] == latest_year].dropna(subset=le_cols + ["GDP_pc"]).copy()
    snap = snap[snap["GDP_pc"] > 0]
    snap["log_GDP_pc"] = np.log(snap["GDP_pc"])

    # reshape to long format
    age_map = {
        "LE_0": 0,
        "LE_10": 10,
        "LE_15": 15,
        "LE_25": 25,
        "LE_45": 45,
        "LE_65": 65,
        "LE_80": 80,
    }
    df_long = snap.melt(
        id_vars=["Entity", "log_GDP_pc"],
        value_vars=le_cols,
        var_name="LE_var",
        value_name="LE_value",
    )
    df_long["Age"] = df_long["LE_var"].map(age_map)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(df_long["Age"], df_long["LE_value"], df_long["log_GDP_pc"], alpha=0.3, s=5)
    ax.set_xlabel("Age (years)")
    ax.set_ylabel("Life Expectancy at that Age (years)")
    ax.set_zlabel("log(GDP per Capita)")
    ax.set_title(f"3D: Age-specific Life Expectancy and log(GDP) ({latest_year})")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f"3d_Age_LE_logGDP_{latest_year}.png", dpi=300)
    plt.close()


def plot_3d_country_trajectories(df: pd.DataFrame) -> None:
    """
    3D trajectories for selected countries: log(GDP_pc) vs LE_0 vs Year.
    """
    countries = ["United States", "China", "India", "Germany", "Brazil", "South Africa"]
    df_sel = df[df["Entity"].isin(countries)].dropna(subset=["GDP_pc", "LE_0"]).copy()
    df_sel = df_sel[df_sel["GDP_pc"] > 0]
    df_sel["log_GDP_pc"] = np.log(df_sel["GDP_pc"])

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    for c in countries:
        sub = df_sel[df_sel["Entity"] == c].sort_values("Year")
        if sub.empty:
            continue
        ax.plot(
            sub["log_GDP_pc"],
            sub["LE_0"],
            sub["Year"],
            marker="o",
            linewidth=1,
            markersize=3,
            label=c,
        )

    ax.set_xlabel("log(GDP per Capita)")
    ax.set_ylabel("Life Expectancy at Birth (years)")
    ax.set_zlabel("Year")
    ax.set_title("3D Trajectories: log(GDP) vs Life Expectancy vs Time")
    ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "3d_trajectories_logGDP_LE0_Year_selected_countries.png", dpi=300)
    plt.close()


# ---------- MAIN ----------
def main():
    print("Loading processed data...")
    df = load_data()

    print("Plotting global 2D trends...")
    plot_global_trends(df)

    print("Plotting 2D scatterplots for latest year...")
    plot_scatter_latest_year(df)

    print("Plotting 2D life expectancy by income group...")
    plot_income_group_boxplot(df)

    print("Plotting 2D time-series trajectories...")
    plot_country_trajectories_2d(df)

    print("Plotting 3D log(GDP)–LE–Year...")
    plot_3d_gdp_le_year(df)

    print("Plotting 3D log(GDP)–LE–GDP growth...")
    plot_3d_gdp_le_growth(df)

    print("Plotting 3D Age–LE_at_age–log(GDP)...")
    plot_3d_age_le_gdp(df)

    print("Plotting 3D country trajectories...")
    plot_3d_country_trajectories(df)

    print("\nAll figures saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
