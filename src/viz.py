from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

def _apply_style(font_size: int = 14):
    plt.rcParams.update({
        "font.size": font_size,
        "axes.titlesize": font_size + 2,
        "axes.labelsize": font_size,
        "legend.fontsize": font_size - 2,
        "figure.autolayout": True,
    })

def plot_global_trend(df_global: pd.DataFrame, outpath: str, *, dpi: int = 200, figsize=(10,5)) -> None:
    _apply_style()
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df_global["year"], df_global["co2_global"])
    ax.set_title("Global CO₂ Emissions Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("CO₂ (million tonnes)")
    ax.grid(True, alpha=0.2)
    Path(outpath).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath, dpi=dpi)
    plt.close(fig)

def plot_top_emitters(df_top: pd.DataFrame, outpath: str, *, dpi: int = 200, figsize=(10,6)) -> None:
    _apply_style()
    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(df_top["country"][::-1], df_top["co2"][::-1])
    ax.set_title("Top Emitters (Production CO₂)")
    ax.set_xlabel("CO₂ (million tonnes)")
    ax.set_ylabel("Country")
    Path(outpath).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath, dpi=dpi)
    plt.close(fig)

def plot_scatter_co2_vs_gdp(df_scatter: pd.DataFrame, outpath: str, *, dpi: int = 200, figsize=(8,6)) -> None:
    _apply_style()
    if "gdp" not in df_scatter.columns:
        raise ValueError("GDP column missing for scatter plot")
    fig, ax = plt.subplots(figsize=figsize)
    ax.scatter(df_scatter["gdp"], df_scatter["co2_per_capita"])
    ax.set_title("CO₂ per Capita vs GDP")
    ax.set_xlabel("GDP (current US$)")
    ax.set_ylabel("CO₂ per capita (t)")
    ax.grid(True, alpha=0.2)
    Path(outpath).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath, dpi=dpi)
    plt.close(fig)
