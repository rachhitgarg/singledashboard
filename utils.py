import pandas as pd
from functools import lru_cache

@lru_cache(maxsize=32)
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def phase_order(df: pd.DataFrame, col: str = "Phase") -> pd.DataFrame:
    """Order Phase column as Pre-AI -> Yoodli -> JPT (if present)."""
    if col in df.columns:
        cat = pd.CategoricalDtype(categories=["Pre-AI", "Yoodli", "JPT"], ordered=True)
        df[col] = df[col].astype(cat)
    return df
