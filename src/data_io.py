from pathlib import Path
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def download_owid_csv(url: str, dest: str) -> Path:
    """Download OWID CO2 CSV to dest if not already present."""
    import urllib.request
    dest_path = Path(dest)
    _ensure_parent(dest_path)
    if not dest_path.exists():
        logger.info(f"Downloading OWID CO2 data to {dest_path} ...")
        urllib.request.urlretrieve(url, dest_path)
    else:
        logger.info(f"Using cached file at {dest_path}")
    return dest_path

def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(Path(path))

def save_parquet(df: pd.DataFrame, path: str) -> None:
    p = Path(path)
    _ensure_parent(p)
    df.to_parquet(p, index=False)
