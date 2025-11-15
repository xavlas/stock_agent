import pandas as pd
from unittest.mock import patch, MagicMock
from agent.fetcher import get_evolution


def test_get_evolution_basic():
    # Build a small fake DataFrame with three days of prices
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=3)
    df = pd.DataFrame({
        "Open": [100, 102, 105],
        "High": [101, 103, 106],
        "Low": [99, 101, 104],
        "Close": [100, 104, 110],
        "Volume": [1000, 1100, 1200],
    }, index=dates)

    mock_ticker = MagicMock()
    mock_ticker.history.return_value = df

    with patch("agent.fetcher.yf.Ticker", return_value=mock_ticker):
        res = get_evolution("FAKE", period="3d", interval="1d")
        assert res["ticker"] == "FAKE"
        assert res["start_price"] == 100.0
        assert res["end_price"] == 110.0
        assert "data" in res
        assert len(res["data"]) == 3
