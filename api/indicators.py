import pandas as pd
import numpy as np

def calculate_garman_klass_volatility(data):
    """
    Calculate Garman-Klass volatility.
    
    This estimator uses high, low, open, and close prices to estimate volatility,
    potentially providing a more accurate measure than close-to-close volatility.
    
    Args:
    data (pd.DataFrame): DataFrame containing 'High', 'Low', 'Open', and 'Close' columns.
    
    Returns:
    np.array: Garman-Klass volatility estimates.
    """
    log_hl = np.log(data['High'] / data['Low'])
    log_co = np.log(data['Close'] / data['Open'])
    return np.sqrt(0.5 * log_hl**2 - (2*np.log(2)-1) * log_co**2)

def calculate_rsi(data, window=20):
    """
    Calculate the Relative Strength Index (RSI).
    
    RSI is a momentum indicator that measures the magnitude of recent price changes
    to evaluate overbought or oversold conditions.
    
    Args:
    data (pd.DataFrame): DataFrame containing 'Close' column.
    window (int): The number of periods to use for RSI calculation. Default is 20.
    
    Returns:
    pd.Series: RSI values.
    """
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_bollinger_bands(data, window=20, num_std=2):
    """
    Calculate Bollinger Bands.
    
    Bollinger Bands consist of a middle band (typically a simple moving average)
    and an upper and lower band that are 'num_std' standard deviations away from the middle band.
    
    Args:
    data (pd.DataFrame): DataFrame containing 'Close' column.
    window (int): The rolling window for calculating the moving average and standard deviation. Default is 20.
    num_std (int): The number of standard deviations for the upper and lower bands. Default is 2.
    
    Returns:
    tuple: Upper band, middle band, and lower band as pd.Series.
    """
    rolling_mean = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return upper_band, rolling_mean, lower_band

def calculate_atr(data, window=20):
    """
    Calculate Average True Range (ATR).
    
    ATR is a technical analysis indicator that measures market volatility.
    
    Args:
    data (pd.DataFrame): DataFrame containing 'High', 'Low', and 'Close' columns.
    window (int): The number of periods to use for ATR calculation. Default is 20.
    
    Returns:
    pd.Series: ATR values.
    """
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    return true_range.rolling(window=window).mean()

def calculate_dollar_volume(data):
    """
    Calculate Dollar Volume.
    
    Dollar Volume is the product of closing price and trading volume.
    
    Args:
    data (pd.DataFrame): DataFrame containing 'Close' and 'Volume' columns.
    
    Returns:
    pd.Series: Dollar Volume values.
    """
    return data['Close'] * data['Volume']

def calculate_percent_change(data):
    """
    Calculate Percent Change.
    
    Percent Change measures the day-over-day percentage change in closing price.
    
    Args:
    data (pd.DataFrame): DataFrame containing 'Close' column.
    
    Returns:
    pd.Series: Percent Change values.
    """
    return ((data['Close'] - data['Close'].shift(1)) / data['Close'].shift(1)) * 100

def calculate_sma(data, window=20):
    """
    Calculate Simple Moving Average (SMA).
    
    SMA is the unweighted mean of the previous 'window' data points.
    
    Args:
    data (pd.DataFrame): DataFrame containing 'Close' column.
    window (int): The number of periods to use for SMA calculation. Default is 20.
    
    Returns:
    pd.Series: SMA values.
    """
    return data['Close'].rolling(window=window).mean()

def calculate_pe_ratio(data, earnings_per_share):
    """
    Calculate Price-to-Earnings (P/E) Ratio.
    
    P/E Ratio is the ratio of a company's share price to its earnings per share.
    
    Args:
    data (pd.DataFrame): DataFrame containing 'Close' column.
    earnings_per_share (float): The company's earnings per share.
    
    Returns:
    pd.Series: P/E Ratio values.
    """
    return data['Close'] / earnings_per_share

def calculate_indicators(data, earnings_per_share):
    """
    Calculate all technical indicators.
    
    This function calculates various technical indicators and returns them as a dictionary.
    
    Args:
    data (pd.DataFrame): DataFrame containing price and volume data.
    earnings_per_share (float): The company's earnings per share.
    
    Returns:
    dict: A dictionary containing all calculated indicators.
    """
    indicators = {}
    indicators['garman_klass'] = calculate_garman_klass_volatility(data).fillna(0).tolist()
    indicators['rsi'] = calculate_rsi(data).fillna(0).tolist()
    upper, middle, lower = calculate_bollinger_bands(data)
    indicators['bollinger_upper'] = upper.fillna(0).tolist()
    indicators['bollinger_middle'] = middle.fillna(0).tolist()
    indicators['bollinger_lower'] = lower.fillna(0).tolist()
    indicators['atr'] = calculate_atr(data).fillna(0).tolist()
    indicators['dollar_volume'] = calculate_dollar_volume(data).fillna(0).tolist()
    indicators['percent_change'] = calculate_percent_change(data).fillna(0).tolist()
    indicators['sma_20'] = calculate_sma(data, window=20).fillna(0).tolist()
    indicators['sma_50'] = calculate_sma(data, window=50).fillna(0).tolist()
    indicators['pe_ratio'] = calculate_pe_ratio(data, earnings_per_share).fillna(0).tolist()
    return indicators
