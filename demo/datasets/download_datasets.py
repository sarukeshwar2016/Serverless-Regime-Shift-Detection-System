"""
Download sample financial datasets for demo / testing purposes.
Uses yfinance for stock data and generates synthetic crypto data.
"""

import os
import pandas as pd
import numpy as np

DATASETS_DIR = os.path.dirname(os.path.abspath(__file__))


def download_stock_data(ticker: str = "SPY", period: str = "1y") -> str:
    """Download historical stock data via yfinance."""
    import yfinance as yf

    df = yf.download(ticker, period=period)
    path = os.path.join(DATASETS_DIR, f"{ticker}_historical.csv")
    df.to_csv(path)
    print(f"[Dataset] Saved {ticker} data → {path}  ({len(df)} rows)")
    return path


def generate_synthetic_crypto(n: int = 5000) -> str:
    """Generate synthetic crypto price data with injected regime shifts."""
    np.random.seed(42)
    prices = [100.0]
    for i in range(1, n):
        regime = 0.002 if i < 2000 else (-0.001 if i < 3500 else 0.003)
        noise = np.random.normal(regime, 0.02)
        prices.append(prices[-1] * (1 + noise))

    df = pd.DataFrame({"price": prices})
    path = os.path.join(DATASETS_DIR, "synthetic_crypto.csv")
    df.to_csv(path, index=False)
    print(f"[Dataset] Saved synthetic crypto data → {path}  ({n} rows)")
    return path


if __name__ == "__main__":
    download_stock_data()
    generate_synthetic_crypto()
    print("[Dataset] All datasets ready.")
