import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# ─────────────────────────────────────────────
# Fetching Historical Stock Data
# ─────────────────────────────────────────────
def get_stock_data(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            print(f"No data found for {ticker} between {start_date} and {end_date}.")
            return None
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# ─────────────────────────────────────────────
# Calculating Technical Indicators
# ─────────────────────────────────────────────
def calculate_indicators(data):
    # SMA & EMA
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()

    # RSI
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = data['Close'].ewm(span=12, adjust=False).mean()
    ema26 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = ema12 - ema26
    data['MACD_Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

    # Bollinger Bands
    data['BB_Mid'] = data['Close'].rolling(window=20).mean()
    data['BB_Std'] = data['Close'].rolling(window=20).std()
    data['BB_Upper'] = data['BB_Mid'] + 2 * data['BB_Std']
    data['BB_Lower'] = data['BB_Mid'] - 2 * data['BB_Std']

    return data

# ─────────────────────────────────────────────
# Plotting Multiple Indicators
# ─────────────────────────────────────────────
def plot_all(data, ticker):
    plt.figure(figsize=(14, 10))

    # Price & Moving Averages
    plt.subplot(3, 1, 1)
    plt.plot(data['Close'], label='Close Price', color='blue')
    plt.plot(data['SMA_20'], label='SMA 20', color='orange')
    plt.plot(data['SMA_50'], label='SMA 50', color='green')
    plt.plot(data['EMA_20'], label='EMA 20', color='purple')
    plt.title(f'{ticker} - Price & Moving Averages')
    plt.legend()
    plt.grid(True)

    # RSI
    plt.subplot(3, 1, 2)
    plt.plot(data['RSI'], label='RSI', color='darkred')
    plt.axhline(70, linestyle='--', color='red')
    plt.axhline(30, linestyle='--', color='green')
    plt.title('Relative Strength Index (RSI)')
    plt.legend()
    plt.grid(True)

    # MACD
    plt.subplot(3, 1, 3)
    plt.plot(data['MACD'], label='MACD', color='black')
    plt.plot(data['MACD_Signal'], label='Signal Line', color='magenta')
    plt.title('MACD & Signal Line')
    plt.plot(data['BB_Upper'], label='Bollinger Upper', color='gray', linestyle='--')
    plt.plot(data['BB_Lower'], label='Bollinger Lower', color='gray', linestyle='--')



    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ─────────────────────────────────────────────
# Signal Interpretation
# ─────────────────────────────────────────────
def interpret_signals(data):
    print("\n📊 Signal Summary:")
    close = data['Close'].iloc[-1]
    sma_20 = data['SMA_20'].iloc[-1]
    sma_50 = data['SMA_50'].iloc[-1]
    rsi = data['RSI'].iloc[-1]
    macd = data['MACD'].iloc[-1]
    signal = data['MACD_Signal'].iloc[-1]

    print(f"Latest Close Price: {close:.2f}")
    print(f"SMA 20: {sma_20:.2f}, SMA 50: {sma_50:.2f}")
    print(f"RSI: {rsi:.2f} → {'Overbought' if rsi > 70 else 'Oversold' if rsi < 30 else 'Neutral'}")
    print(f"MACD vs Signal: {macd:.2f} vs {signal:.2f} → {'Bullish' if macd > signal else 'Bearish'}")

    if sma_20 > sma_50:
        print("🟢 Trend: Golden Cross (Bullish)")
    elif sma_20 < sma_50:
        print("🔴 Trend: Death Cross (Bearish)")
    else:
        print("⚪ Trend: Neutral/Sideways")

# ─────────────────────────────────────────────
# Main Program
# ─────────────────────────────────────────────
def main():
    print("Welcome to the Advanced Stock Market Analyzer!")

    ticker = input("Enter stock ticker (e.g. AAPL, TATAMOTORS.NS): ").upper()
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365 * 2)

    data = get_stock_data(ticker, start_date, end_date)
    if data is None:
        print("Exiting... No data retrieved.")
        return

    data = calculate_indicators(data)
    print("\n📂 Sample Data Snapshot:")
    print(data.tail())

    plot_all(data, ticker)
    interpret_signals(data)

if __name__ == "__main__":
    main()
