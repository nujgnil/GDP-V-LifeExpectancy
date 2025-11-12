import logging
from pathlib import Path
import typer
import pandas as pd

from src import config as cfg
from src import data_io, preprocessing, analysis, report
from src import viz

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = typer.Typer(help="Data visualization pipeline")


def _print_section(title: str) -> None:
    print("=" * 80)
    print(title)
    print("=" * 80)


def _print_df_preview(name: str, df: pd.DataFrame, n: int = 5) -> None:
    print(f"{name} shape: {df.shape}")
    print(f"{name} columns: {list(df.columns)}")
    print(f"{name} head({n}):")
    print(df.head(n))
    print()


@app.command()
def all(config: str = typer.Option("config/default.yaml", help="Path to config YAML")):
    # -------------------------------------------------------------------------
    # 0) Load configuration
    # -------------------------------------------------------------------------
    _print_section("LOAD CONFIG")
    conf = cfg.load(config)
    print("Config loaded from:", config)
    print(conf)
    print()

    # -------------------------------------------------------------------------
    # 1) Load raw data (from URL if provided, else from raw_path)
    # -------------------------------------------------------------------------
    _print_section("LOAD RAW DATA")
    data_conf = conf.get("data", {})
    owid_url = data_conf.get("owid_url")
    raw_path = data_conf.get("raw_path")
    csv_path: Path

    if owid_url:
        print("Detected 'owid_url' in config; downloading or using cached file.")
        csv_path = data_io.download_owid_csv(owid_url, raw_path or "data/raw/owid_co2.csv")
    else:
        if not raw_path:
            raise ValueError("Config must provide data.raw_path when data.owid_url is not set.")
        csv_path = Path(raw_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"Raw file not found at: {csv_path}")
        print("Using local CSV path from config:", csv_path)

    df_raw = pd.read_csv(csv_path)
    _print_df_preview("RAW", df_raw)

    # -------------------------------------------------------------------------
    # 2) Clean / preprocess
    #    If you are using a different dataset (e.g., temperature anomaly),
    #    replace 'clean_co2' with your specific cleaner.
    # -------------------------------------------------------------------------
    _print_section("CLEAN / PREPROCESS")
    df = preprocessing.clean_co2(
        df_raw,
        year_min=conf["preprocessing"]["year_min"],
        keep_countries_only=conf["preprocessing"]["keep_countries_only"],
    )
    _print_df_preview("CLEAN", df)

    # -------------------------------------------------------------------------
    # 3) Persist processed data
    # -------------------------------------------------------------------------
    _print_section("SAVE PROCESSED")
    processed_path = Path(conf["data"]["processed_path"])
    data_io.save_parquet(df, processed_path)
    print("Processed dataset written to:", processed_path)
    print()

    # -------------------------------------------------------------------------
    # 4) Analysis
    # -------------------------------------------------------------------------
    _print_section("ANALYSIS: GLOBAL TREND / TOP EMITTERS / SCATTER FRAME")
    yr = analysis.latest_year(
        df,
        conf["analysis"].get("latest_year_strategy", "max_available"),
        conf["analysis"].get("fixed_year"),
    )
    print("Selected analysis year:", yr)

    df_global = analysis.global_trend(df)
    _print_df_preview("GLOBAL_TREND", df_global)

    df_top = analysis.top_emitters(df, year=yr, n=conf["analysis"]["top_n_emitters"])
    _print_df_preview("TOP_EMITTERS", df_top)

    df_scatter = analysis.correlation_frame(df, year=yr)
    _print_df_preview("SCATTER_FRAME", df_scatter)

    # -------------------------------------------------------------------------
    # 5) Tables
    # -------------------------------------------------------------------------
    _print_section("EXPORT TABLES")
    tables_dir = Path(conf["outputs"]["tables_dir"])
    tables_dir.mkdir(parents=True, exist_ok=True)
    top_emitters_path = tables_dir / f"top_emitters_{yr}.csv"
    report.export_table(df_top, top_emitters_path)
    print("Table written:", top_emitters_path)
    print()

    # -------------------------------------------------------------------------
    # 6) Figures
    # -------------------------------------------------------------------------
    _print_section("EXPORT FIGURES")
    figures_dir = Path(conf["outputs"]["figures_dir"])
    figures_dir.mkdir(parents=True, exist_ok=True)

    fig1 = figures_dir / "global_trend.png"
    viz.plot_global_trend(df_global, fig1)
    print("Figure written:", fig1)

    fig2 = figures_dir / f"top_emitters_{yr}.png"
    viz.plot_top_emitters(df_top, fig2)
    print("Figure written:", fig2)

    if not df_scatter.empty:
        fig3 = figures_dir / f"scatter_co2_vs_gdp_{yr}.png"
        viz.plot_scatter_co2_vs_gdp(df_scatter, fig3)
        print("Figure written:", fig3)
    else:
        print("Scatter frame empty; skipping scatter figure.")

    print()
    logger.info("Done. Figures and tables written to reports/.")


if __name__ == "__main__":
    app()