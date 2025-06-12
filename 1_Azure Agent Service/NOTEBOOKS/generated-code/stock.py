import yfinance as yf
from typing import Optional

def get_stock_price(ticker: str) -> Optional[float]:
    """
    Retrieve the latest closing price of the given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        Optional[float]: The latest closing price if available, None otherwise.
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if data.empty:
            return None
        return data['Close'].iloc[-1]
    except Exception as e:
        print(f"Error retrieving stock data for {ticker}: {e}")
        return None

if __name__ == "__main__":
    ticker = "MSFT"
    price = get_stock_price(ticker)
    if price is not None:
        print(f"The current price of {ticker} stock is ${price:.2f}")
    else:
        print(f"Could not retrieve the price for {ticker} stock.")