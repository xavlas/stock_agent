import yfinance as yf
from typing import Dict, Any


def get_evolution(ticker: str, period: str = "1mo", interval: str = "1d") -> Dict[str, Any]:
    """Fetch historical prices for `ticker` and return a simple evolution summary.

    Returns a dict with keys: ticker, period, interval, start_date, end_date,
    start_price, end_price, pct_change, data (list of {date, close}).
    """
    t = yf.Ticker(ticker)
    hist = t.history(period=period, interval=interval)
    if hist is None or hist.empty:
        raise ValueError(f"No data for {ticker} with period={period} interval={interval}")

    hist = hist.sort_index()
    start_row = hist.iloc[0]
    end_row = hist.iloc[-1]

    start_price = float(start_row["Close"])
    end_price = float(end_row["Close"])
    pct_change = (end_price - start_price) / start_price * 100

    data = []
    for idx, row in hist.iterrows():
        # use ISO date string for portability
        data.append({"date": str(idx.date()), "close": float(row["Close"])})

    return {
        "ticker": ticker,
        "period": period,
        "interval": interval,
        "start_date": str(hist.index[0].date()),
        "end_date": str(hist.index[-1].date()),
        "start_price": start_price,
        "end_price": end_price,
        "pct_change": round(pct_change, 4),
        "data": data,
    }
