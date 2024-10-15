import yfinance as yf
import pandas as pd

# Get S&P 500 tickers
def get_tickers():
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    sp500.sort_values(by='Symbol', ascending=True, inplace=True)
    return sp500['Symbol'].tolist()

# Get stock data from Yahoo Finance
def get_stock_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date)
    return data[['Open', 'High', 'Low', 'Close', 'Volume']]

# Get ticker info from Yahoo Finance
def get_ticker_info(symbol):
    stock = yf.Ticker(symbol)
    return stock.info



