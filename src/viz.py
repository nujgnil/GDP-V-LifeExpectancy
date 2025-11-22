from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D)
from matplotlib.patches import Ellipse

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


def plot_global_trends(df: pd.DataFrame) -> None:
    """
    Global average trends over time for LE_0 and GDP_pc.
    Adds shading for 19th/20th centuries and annotations that match the report text.
    """
    grouped = (
        df.groupby("Year")[["LE_0", "GDP_pc"]]
        .mean()
        .reset_index()
        .sort_values("Year")
    )

    min_year = int(grouped["Year"].min())
    max_year = int(grouped["Year"].max())

    # Helper to clip shading ranges to available data
    def clip_range(start, end):
        return max(start, min_year), min(end, max_year)

    # ----------------------------------------------------------------------
    # LIFE EXPECTANCY TREND
    # ----------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(grouped["Year"], grouped["LE_0"])
    ax.set_xlabel("Year")
    ax.set_ylabel("Life Expectancy at Birth (years)")
    ax.set_title("Global Average Life Expectancy at Birth Over Time")

    # Shade 19th century (1800–1900) and 20th century (1900–2000)
    y0, y1 = ax.get_ylim()
    start_19, end_19 = clip_range(1800, 1900)
    start_20, end_20 = clip_range(1900, 2000)

    if start_19 < end_19:
        ax.axvspan(start_19, end_19, alpha=0.25, label="19th century")
        ax.text(
            (start_19 + end_19) / 2,
            y1 - (y1 - y0) * 0.03,  # very close to top
            "19th century",
            ha="center",
            va="top",
            fontsize=9,
        )

    if start_20 < end_20:
        ax.axvspan(start_20, end_20, alpha=0.20, color="orange", label="20th century")
        ax.text(
            (start_20 + end_20) / 2,
            y1 - (y1 - y0) * 0.03,  # also high, but slightly below 19th
            "20th century",
            ha="center",
            va="top",
            fontsize=9,
        )

    # Extra shading for "mid-20th century" rapid gains (e.g. 1950–2000)
    start_mid, end_mid = clip_range(1950, 2000)
    if start_mid < end_mid:
        ax.axvspan(start_mid, end_mid, alpha=0.25, color="orange")
        ax.text(
            (start_mid + end_mid) / 2,
            y0 + (y1 - y0) * 0.15,
            "Rapid post-WWII gains",
            ha="center",
            va="center",
            fontsize=9,
        )

    # Annotate "early 1800s ~30 years" and "today ~70 years"
    first = grouped.iloc[0]
    last = grouped.iloc[-1]

    # --- manual label placement controls ---
    # Adjust these four values freely to move the bubbles wherever you like
    first_label_x = first["Year"] - 0     # change this
    first_label_y = first["LE_0"] + 20     # change this

    last_label_x = last["Year"] - 20       # change this
    last_label_y = last["LE_0"] -10       # change this

    # --- annotate early-year life expectancy ---
    ax.annotate(
        f"{int(first['Year'])}: {first['LE_0']:.1f} years\n(early 1800s ≈ low 30s)",
        xy=(first["Year"], first["LE_0"]),         # arrow target
        xytext=(first_label_x, first_label_y),     # bubble location YOU control
        textcoords="data",
        arrowprops=dict(arrowstyle="->", linewidth=1),
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.9),
    )

    # --- annotate latest-year life expectancy ---
    ax.annotate(
        f"{int(last['Year'])}: {last['LE_0']:.1f} years\n(≈ 70 years today)",
        xy=(last["Year"], last["LE_0"]),
        xytext=(last_label_x, last_label_y),       # bubble location YOU control
        textcoords="data",
        arrowprops=dict(arrowstyle="->", linewidth=1),
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.9),
    )


    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "trend_global_LE0.png", dpi=300)
    plt.close(fig)

    # ----------------------------------------------------------------------
    # GDP PER CAPITA TREND
    # ----------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(grouped["Year"], grouped["GDP_pc"], color="darkgreen", linewidth=2)
    ax.set_xlabel("Year")
    ax.set_ylabel("GDP per Capita (USD)")
    ax.set_title("Global Average GDP per Capita Over Time")

    y0, y1 = ax.get_ylim()

    # Shade 19th and 20th centuries in the same way
    if start_19 < end_19:
        ax.axvspan(start_19, end_19, alpha=0.3, color="#0080ff")
        ax.text(
            (start_19 + end_19) / 2,
            y1 - (y1 - y0) * 0.07,
            "19th century",
            ha="center",
            va="center",
            fontsize=9,
        )

    if start_20 < end_20:
        ax.axvspan(start_20, end_20, alpha=0.3, color="#ffa200")
        ax.text(
            (start_20 + end_20) / 2,
            y1 - (y1 - y0) * 0.07,
            "20th century",
            ha="center",
            va="center",
            fontsize=9,
        )

    # Pick one point around 1850 and one around 2000 if available
    year_slow = min(max(1850, min_year), max_year)
    year_fast = min(max(2000, min_year), max_year)

    slow_row = grouped.iloc[(grouped["Year"] - year_slow).abs().argmin()]
    fast_row = grouped.iloc[(grouped["Year"] - year_fast).abs().argmin()]

        # ---- annotation bubbles WITHOUT arrows ----
    slow_label_x = slow_row["Year"] -30
    slow_label_y = slow_row["GDP_pc"] + 1800

    fast_label_x = fast_row["Year"] - 70
    fast_label_y = fast_row["GDP_pc"] - 5300

    ax.annotate(
        f"Slow growth in 19th century\n({int(slow_row['Year'])}: "
        f"${slow_row['GDP_pc']:.0f})",
        xy=(slow_row["Year"], slow_row["GDP_pc"]),     # REQUIRED
        xytext=(slow_label_x, slow_label_y),           # bubble position
        textcoords="data",
        arrowprops=None,                               # No arrow
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.9),
    )

    ax.annotate(
        f"Faster growth in 20th century\n({int(fast_row['Year'])}: "
        f"${fast_row['GDP_pc']:.0f})",
        xy=(fast_row["Year"], fast_row["GDP_pc"]),     # REQUIRED
        xytext=(fast_label_x, fast_label_y),
        textcoords="data",
        arrowprops=None,                               # No arrow
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.9),
    )

    # ---- circle major high-gradient segments (no arrows) ----
    # 1) Post-WWII take-off (~1960s–1970s)
    center1_year = 1965
    center1_row = grouped.iloc[(grouped["Year"] - center1_year).abs().argmin()]
    center1_val = center1_row["GDP_pc"]

    ell1 = Ellipse(
        (center1_year, center1_val),
        width=30,                          # years spanned
        height=(y1 - y0) * 0.40,           # vertical span
        edgecolor="red",
        facecolor="none",
        linewidth=1.5,
    )
    ax.add_patch(ell1)

    # 2) Late-20th / early-21st century boom (~1990s–2010)
    center2_year = 1995
    center2_row = grouped.iloc[(grouped["Year"] - center2_year).abs().argmin()]
    center2_val = center2_row["GDP_pc"]

    ell2 = Ellipse(
        (center2_year, center2_val),
        width=25,
        height=(y1 - y0) * 0.35,
        edgecolor="red",
        facecolor="none",
        linewidth=1.5,
    )
    ax.add_patch(ell2)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "trend_global_GDPpc.png", dpi=300)
    plt.close(fig)


def plot_scatter_latest_year(df: pd.DataFrame) -> None:
    """
    Scatter: GDP per capita vs Life Expectancy (latest year),
    with a best-fit curve based on LE_0 ~ log(GDP_pc),
    and a log(GDP) version with a straight best-fit line.
    Includes annotations that match the report text.
    """
    latest_year = df["Year"].max()
    snap = df[df["Year"] == latest_year].dropna(subset=["GDP_pc", "LE_0"]).copy()
    snap = snap[snap["GDP_pc"] > 0]  # log requires positive values

    x_gdp = snap["GDP_pc"].values
    y_le = snap["LE_0"].values
    log_x = np.log(x_gdp)

    # Fit in log space: LE_0 = intercept + slope * log(GDP)
    slope, intercept = np.polyfit(log_x, y_le, 1)

    # ----------------------------------------------------
    # RAW GDP axis with curved log-based best-fit line
    # ----------------------------------------------------
    plt.figure(figsize=(8, 6))
    plt.scatter(x_gdp, y_le, alpha=0.5, label="Country (latest year)")

    # Best-fit curve implied by LE_0 ~ log(GDP_pc)
    x_line = np.linspace(x_gdp.min(), x_gdp.max(), 200)
    y_line = intercept + slope * np.log(x_line)
    plt.plot(x_line, y_line, linewidth=2,
             label="Best fit: LE₀ ~ log(GDP per capita)", color="red")

    # --- Annotations reflecting your paragraph ---

    # Low-income, low-LE cluster (bottom-left)
    low_x = np.percentile(x_gdp, 10)
    low_y = np.percentile(y_le, 10)
    plt.annotate(
        "Low income,\nlow life expectancy",
        xy=(low_x, low_y),
        xytext=(low_x * 2, low_y - 5),
        arrowprops=dict(arrowstyle="->", linewidth=1),
        fontsize=9,
    )

    # High-income, high-LE cluster (top-right)
    high_x = np.percentile(x_gdp, 90)
    high_y = np.percentile(y_le, 90)
    plt.annotate(
        "High income,\nhigh life expectancy",
        xy=(high_x, high_y),
        xytext=(high_x * 0.6, high_y + 3),
        arrowprops=dict(arrowstyle="->", linewidth=1),
        fontsize=9,
    )

    # Curvature / diminishing returns at high income
    # Pick a point near the top of the curve
    idx_high_curve = np.argmax(x_line)
    plt.annotate(
        "Large GDP increases\n→ smaller gains in LE₀",
        xy=(x_line[idx_high_curve], y_line[idx_high_curve]),
        xytext=(x_line[idx_high_curve] * 0.6, y_line[idx_high_curve] - 8),
        arrowprops=dict(arrowstyle="->", linewidth=1),
        fontsize=9,
    )

    plt.xlabel("GDP per Capita (USD)")
    plt.ylabel("Life Expectancy at Birth (years)")
    plt.title(f"GDP per Capita vs Life Expectancy at Birth ({latest_year})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f"scatter_GDPpc_LE0_{latest_year}.png", dpi=300)
    plt.close()

    # ----------------------------------------------------
    #LOG(GDP) axis with straight best-fit line
    # ----------------------------------------------------
    plt.figure(figsize=(8, 6))
    plt.scatter(log_x, y_le, alpha=0.5, label="Country (latest year)")

    log_x_line = np.linspace(log_x.min(), log_x.max(), 200)
    y_line_log = intercept + slope * log_x_line
    plt.plot(log_x_line, y_line_log, linewidth=2,
             label="Best-fit line", color = "red")

    # annnotations for relationship is closer to linear
    mid_log = np.median(log_x)
    mid_y = intercept + slope * mid_log
    plt.annotate(
        "Almost linear pattern in log space:\n"
        "proportional differences in GDP\n"
        "are more informative than absolute levels",
        xy=(mid_log, mid_y),
        xytext=(mid_log, mid_y + 6),
        arrowprops=dict(arrowstyle="->", linewidth=1),
        fontsize=9,
        ha="center",
    )

# highlight low- vs high-log GDP ends
    plt.annotate(
        "Low log(GDP):\nsmall increases in income\n"
        "associated with large gains in LE₀",
        xy=(log_x.min(), intercept + slope * log_x.min()),
        xytext=(log_x.min() + 0.3, intercept + slope * log_x.min() - 8),
        arrowprops=dict(arrowstyle="->", linewidth=1),
        fontsize=9,
    )
    plt.annotate(
        "High log(GDP):\nextra income yields\n"
        "smaller extra years of life",
        xy=(log_x.max(), intercept + slope * log_x.max()),
        xytext=(log_x.max() - 1.0, intercept + slope * log_x.max() + 4),
        arrowprops=dict(arrowstyle="->", linewidth=1),
        fontsize=9,
    )

    plt.xlabel("log(GDP per Capita)")
    plt.ylabel("Life Expectancy at Birth (years)")
    plt.title(f"log(GDP per Capita) vs Life Expectancy at Birth ({latest_year})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f"scatter_logGDPpc_LE0_{latest_year}.png", dpi=300)
    plt.close()
    
    
def plot_income_group_boxplot(df: pd.DataFrame) -> None:
    """
    Boxplot of life expectancy by income group (latest year), with:
      - median labels,
      - whisker ranges + deltas (matching boxplot whiskers),
      - income-range text under each income-group label,
      - red boxes highlighting Δ for upper-middle & high income,
      - red arrow from 'widest spread' bubble to Δ of low income,
      - top-right bubble describing higher medians & narrower IQRs
        (no arrows).
    """
    # Attach income groups and filter to latest year
    df, latest_year = create_income_groups(df)
    snap = df[df["Year"] == latest_year].dropna(subset=["LE_0", "Income_group"])

    order = ["Low income", "Lower-middle", "Upper-middle", "High income"]
    le_data = [snap[snap["Income_group"] == g]["LE_0"] for g in order]
    gdp_data = [snap[snap["Income_group"] == g]["GDP_pc"] for g in order]

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.boxplot(le_data, labels=order, showfliers=False)
    ax.set_xlabel("Income Group")
    ax.set_ylabel("Life Expectancy at Birth (years)")
    ax.set_title(f"Life Expectancy by Income Group ({latest_year})")

    # y-limits: bottom fixed at 50, top at 95 for headroom
    ax.set_ylim(50.0, 95.0)

    # --------------------------
    # Median labels
    # --------------------------
    medians = [np.median(d) for d in le_data]
    for i, median_val in enumerate(medians, start=1):
        ax.annotate(
            f"Median ≈ {median_val:.1f}",
            xy=(i, median_val),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            arrowprops=dict(arrowstyle="->", linewidth=0.8),
            bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.85),
        )

    # --------------------------
    # Whisker ranges + deltas
    # --------------------------
    all_vals = np.concatenate([np.asarray(d) for d in le_data])
    ymin, ymax = all_vals.min(), all_vals.max()
    y_span = ymax - ymin
    spread_height = 0.08 * y_span  # base vertical offset

    delta_label_positions: list[tuple[float, float]] = []

    for idx, (group, vals) in enumerate(zip(order, le_data), start=1):
        arr = np.asarray(vals)
        q1, q3 = np.percentile(arr, [25, 75])
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        whisk_low = arr[arr >= lower_bound].min()
        whisk_high = arr[arr <= upper_bound].max()

        # "Range: low–high" label
        range_y = whisk_high + spread_height
        ax.annotate(
            f"Range: {whisk_low:.1f}–{whisk_high:.1f}",
            xy=(idx, whisk_high),
            xytext=(idx, range_y),
            textcoords="data",
            ha="center",
            va="bottom",
            fontsize=8.5,
            arrowprops=dict(arrowstyle="->", linewidth=0.8),
            bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.9),
        )

        # "Δ = ..." label (red box for upper-middle & high)
        delta_y = range_y + 0.6 * spread_height
        delta = whisk_high - whisk_low
        edge_col = "red" if group in ["Upper-middle", "High income"] else "black"

        ax.annotate(
            f"Δ = {delta:.1f}",
            xy=(idx, delta_y),
            xycoords="data",
            ha="center",
            va="bottom",
            fontsize=8.5,
            bbox=dict(
                boxstyle="round,pad=0.25",
                fc="white",
                ec=edge_col,
                lw=1.2,
                alpha=0.95,
            ),
        )

        delta_label_positions.append((idx, delta_y))

    # --------------------------
    # Income ranges under x-labels
    # --------------------------
    income_labels = []
    for g, gdp_vals in zip(order, gdp_data):
        if gdp_vals.empty:
            income_labels.append(g)
        else:
            lo_gdp = gdp_vals.min()
            hi_gdp = gdp_vals.max()
            income_labels.append(f"{g}\n{lo_gdp:,.0f}–{hi_gdp:,.0f} USD")
    ax.set_xticklabels(income_labels)

    # --------------------------
    # "Widest spread" callout (low income)
    # --------------------------
    low_delta_x, low_delta_y = delta_label_positions[0]
    low_arrow_target_y = low_delta_y + 0.8  # a bit above the Δ box

    ax.annotate(
        "Widest spread:\nlarge inequality\nwithin low-income group",
        xy=(low_delta_x, low_arrow_target_y),   # arrow tip in data coords
        xycoords="data",
        xytext=(0.05, 0.88),                    # text box in axes fraction
        textcoords="axes fraction",
        ha="left",
        va="top",
        fontsize=9,
        arrowprops=dict(arrowstyle="->", linewidth=0.9, color="red"),
        bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.9),
    )

    # --------------------------
    # "Higher medians & narrower IQRs" bubble (no arrows)
    # --------------------------
    ax.annotate(
        "Higher medians and narrower IQRs:\n"
        "life expectancy more homogeneous\n"
        "in upper-middle & high-income groups",
        xy=(0.82, 0.985),          # dummy, not used since we use xytext
        xycoords="axes fraction",
        xytext=(0.82, 0.985),
        textcoords="axes fraction",
        ha="center",
        va="top",
        fontsize=9,
        arrowprops=None,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.9),
    )

    fig.tight_layout()
    out_path = OUTPUT_DIR / f"boxplot_LE0_income_groups_{latest_year}.png"
    fig.savefig(out_path, dpi=300)
    plt.close(fig)



def plot_country_trajectories_2d(df: pd.DataFrame) -> None:
    """
    Trajectories in log(GDP per capita) – Life Expectancy space
    for selected countries, with non-overlapping annotation bubbles.
    """
    countries = ["China", "India", "United States", "Germany", "Brazil", "South Africa"]

    # ensure log GDP exists
    df = df.copy()
    if "log_GDP_pc" not in df.columns:
        df["log_GDP_pc"] = np.log(df["GDP_pc"])

    df_sel = df[df["Entity"].isin(countries)].dropna(subset=["LE_0", "log_GDP_pc"])

    fig, ax = plt.subplots(figsize=(11, 7))

    # plot trajectories
    series = {}
    for c in countries:
        sub = df_sel[df_sel["Entity"] == c].sort_values("Year")
        if sub.empty:
            continue
        ax.plot(
            sub["log_GDP_pc"],
            sub["LE_0"],
            marker="o",
            markersize=3,
            linewidth=1.2,
            label=c,
        )
        series[c] = sub

    ax.set_xlabel("log(GDP per Capita)")
    ax.set_ylabel("Life Expectancy at Birth (years)")
    ax.set_title(
        "Trajectories in log(GDP)–Life Expectancy Space\nSelected Countries Over Time"
    )
    ax.legend(loc="upper left", fontsize=9)

    # --- annotation helper ---
    def annotate_traj(country, pos="end", text="", xy_index=None, xytext=(0, 0)):
        sub = series[country]
        if pos == "start":
            p = sub.iloc[0]
        elif pos == "end":
            p = sub.iloc[-1]
        elif pos == "mid":
            if xy_index is None:
                xy_index = len(sub) // 2
            p = sub.iloc[xy_index]
        else:
            raise ValueError("pos must be 'start', 'end', or 'mid'")

        ax.annotate(
            text,
            xy=(p["log_GDP_pc"], p["LE_0"]),
            xycoords="data",
            xytext=xytext,
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.95),
            arrowprops=dict(arrowstyle="->", linewidth=0.9),
        )

    # --- individual bubbles (tuned offsets to avoid overlap) ---

    # China
    annotate_traj(
        "China",
        pos="start",
        text="China (start: 1950)",
        xytext=(-40, 100),
    )
    annotate_traj(
        "China",
        pos="end",
        text="China (recent: 2020)\nrapid gains in income & LE",
        xytext=(20, 30),
    )

    # India
    annotate_traj(
        "India",
        pos="start",
        text="India (start: 1950)",
        xytext=(50, -60),
    )
    annotate_traj(
        "India",
        pos="end",
        text="India (recent: 2020)\ncatch-up in LE with slower income growth",
        xytext=(-85, 75),
    )

    # United States – high starting income, gradual LE gains
    annotate_traj(
        "United States",
        pos="mid",
        text="United States:\nhigh income,\nmore gradual LE gains",
        xytext=(50, -40),
    )

    # Germany – high starting income + steady gains
    annotate_traj(
        "Germany",
        pos="end",
        text="Germany:\nrich throughout,\nsteady improvements in LE",
        xytext=(40, -45),
    )

    # Brazil – more irregular path
    annotate_traj(
        "Brazil",
        pos="mid",
        text="Brazil:\nmore irregular path\nin income & LE",
        xytext=(85, -55),
    )

    # South Africa – irregular, stagnation in LE at times
    annotate_traj(
        "South Africa",
        pos="mid",
        text="South Africa:\nstrong income swings\nand LE setbacks",
        xytext=(35, -105),
    )

    fig.tight_layout()
    out_path = OUTPUT_DIR / "trajectories_logGDPpc_LE0_selected_countries.png"
    fig.savefig(out_path, dpi=300)
    plt.close(fig)



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
    
def plot_trajectories_logGDP_LE0(df: pd.DataFrame) -> None:
    """
    2D trajectories in log(GDP per capita)–LE_0 space for selected countries,
    with annotations matching the report text:
    - China & India starting low and moving up-right
    - US & Germany starting high with gradual improvements
    - Brazil & South Africa showing more irregular paths
    """
    countries = ["China", "India", "United States", "Germany", "Brazil", "South Africa"]

    df_sel = df[df["Entity"].isin(countries)].dropna(subset=["GDP_pc", "LE_0"]).copy()
    df_sel = df_sel[df_sel["GDP_pc"] > 0]
    df_sel["log_GDP_pc"] = np.log(df_sel["GDP_pc"])

    plt.figure(figsize=(10, 7))

    for c in countries:
        sub = df_sel[df_sel["Entity"] == c].sort_values("Year")
        if sub.empty:
            continue

        # plot the trajectory as a line with markers
        plt.plot(
            sub["log_GDP_pc"],
            sub["LE_0"],
            marker="o",
            linewidth=1,
            markersize=3,
            label=c,
        )

        start = sub.iloc[0]
        end = sub.iloc[-1]

        # China & India: emphasise "start low, move up-right"
        if c in ["China", "India"]:
            plt.annotate(
                f"{c} (start: {int(start['Year'])})",
                xy=(start["log_GDP_pc"], start["LE_0"]),
                xytext=(start["log_GDP_pc"] - 0.8, start["LE_0"] - 8),
                arrowprops=dict(arrowstyle="->", linewidth=1),
                fontsize=9,
            )
            plt.annotate(
                f"{c} (recent: {int(end['Year'])})",
                xy=(end["log_GDP_pc"], end["LE_0"]),
                xytext=(end["log_GDP_pc"] + 0.3, end["LE_0"] + 3),
                arrowprops=dict(arrowstyle="->", linewidth=1),
                fontsize=9,
            )

        # US & Germany: "start high, gradual improvements"
        if c in ["United States", "Germany"]:
            mid_idx = len(sub) // 2
            mid = sub.iloc[mid_idx]
            plt.annotate(
                f"{c}:\nhigh starting income,\nmore gradual gains",
                xy=(mid["log_GDP_pc"], mid["LE_0"]),
                xytext=(mid["log_GDP_pc"] - 0.7, mid["LE_0"] + 6),
                arrowprops=dict(arrowstyle="->", linewidth=1),
                fontsize=9,
            )

        # Brazil & South Africa: "more irregular paths"
        if c in ["Brazil", "South Africa"]:
            mid_idx = len(sub) // 2
            mid = sub.iloc[mid_idx]
            plt.annotate(
                f"{c}:\nmore irregular path\nin income and LE₀",
                xy=(mid["log_GDP_pc"], mid["LE_0"]),
                xytext=(mid["log_GDP_pc"] + 0.5, mid["LE_0"] - 6),
                arrowprops=dict(arrowstyle="->", linewidth=1),
                fontsize=9,
            )

    plt.xlabel("log(GDP per Capita)")
    plt.ylabel("Life Expectancy at Birth (years)")
    plt.title("Trajectories in log(GDP)–Life Expectancy Space\nSelected Countries Over Time")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "trajectories_logGDPpc_LE0_selected_countries.png", dpi=300)
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
