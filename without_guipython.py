import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def get_stock_data(ticker, start_date, end_date):
    """
    Fetches historical stock data for a given ticker and date range.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            print(f"No data found for {ticker} between {start_date} and {end_date}. Please check the ticker or date range.")
            return None
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def calculate_moving_averages(data, short_window, long_window):
    """
    Calculates Simple Moving Averages (SMAs) for given windows.
    """
    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()
    return data

def plot_stock_data(data, ticker, short_window, long_window):
    """
    Plots the closing price and moving averages.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price', color='blue')
    plt.plot(data['SMA_Short'], label=f'SMA {short_window} (Close)', color='orange')
    plt.plot(data['SMA_Long'], label=f'SMA {long_window} (Close)', color='green')
    plt.title(f'{ticker} Stock Price with {short_window}-day and {long_window}-day SMAs')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    """
    Main function to run the stock market analyzer.
    """
    print("Welcome to the Python Stock Market Analyzer!")

    ticker = input("Enter the stock ticker symbol (e.g., AAPL, GOOGL, MSFT): ").upper()

    # Define date range (e.g., last 1 year)
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365 * 2) # Last 2 years of data

    print(f"\nFetching data for {ticker} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
    stock_data = get_stock_data(ticker, start_date, end_date)

    if stock_data is None:
        print("Exiting.")
        return

    # Calculate moving averages
    short_window = 20  # 20-day SMA
    long_window = 50   # 50-day SMA
    stock_data = calculate_moving_averages(stock_data, short_window, long_window)

    print("\n--- Stock Data Sample ---")
    print(stock_data.tail()) # Display last few rows of data

    # Plot the data
    plot_stock_data(stock_data, ticker, short_window, long_window)

    # --- Basic Analysis ---
    print("\n--- Basic Analysis ---")
    latest_close = floatstock_data['Close'].iloc[-1]
    latest_sma_short = float(stock_data['SMA_Short'].iloc[-1])
    latest_sma_long = float(stock_data['SMA_Long'].iloc[-1])

    print(f"Latest Close Price: ${latest_close:.2f}")
    print(f"Latest {short_window}-day SMA: ${latest_sma_short:.2f}")
    print(f"Latest {long_window}-day SMA: ${latest_sma_long:.2f}")

    if latest_sma_short > latest_sma_long and stock_data['SMA_Short'].iloc[-2] <= stock_data['SMA_Long'].iloc[-2]:
        print(f"Golden Cross! The {short_window}-day SMA has crossed above the {long_window}-day SMA. This can be a bullish signal.")
    elif latest_sma_short < latest_sma_long and stock_data['SMA_Short'].iloc[-2] >= stock_data['SMA_Long'].iloc[-2]:
        print(f"Death Cross! The {short_window}-day SMA has crossed below the {long_window}-day SMA. This can be a bearish signal.")
    elif latest_close > latest_sma_short and latest_close > latest_sma_long:
        print("Current price is above both short and long-term moving averages. Generally considered bullish.")
    elif latest_close < latest_sma_short and latest_close < latest_sma_long:
        print("Current price is below both short and long-term moving averages. Generally considered bearish.")
    else:
        print("Price action is mixed relative to moving averages.")


if __name__ == "__main__":
    main()
