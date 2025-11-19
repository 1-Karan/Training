import yfinance as yf

def get_stock_data(stock_symbol):
    stock_symbol = stock_symbol.strip().replace(" ", "").upper()
    if not stock_symbol.endswith(".NS"):
        stock_symbol += ".NS"

    try:
        stock = yf.Ticker(stock_symbol)
        hist = stock.history(period="7d")

        if hist.empty:
            print(f"No data found for symbol: {stock_symbol}")
            return []  # ✅ Return empty list instead of None

        required_cols = ['Open', 'Close', 'High', 'Low', 'Volume']
        missing_cols = [col for col in required_cols if col not in hist.columns]
        if missing_cols:
            print(f"Missing columns {missing_cols} in data for {stock_symbol}")
            return []

        selected = hist[required_cols]
        return selected.to_dict(orient="records")

    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return []
