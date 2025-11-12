from pathlib import Path
import pandas as pd

def export_table(df: pd.DataFrame, outpath: str) -> None:
    p = Path(outpath)
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=False)
