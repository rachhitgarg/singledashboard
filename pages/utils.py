
import pandas as pd
from functools import lru_cache

@lru_cache(maxsize=32)
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def phase_order(df, col="Phase"):
    cat = pd.CategoricalDtype(categories=["Pre-AI","Yoodli","JPT"], ordered=True)
    if col in df.columns:
        df[col] = df[col].astype(cat)
    return df
