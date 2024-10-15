# Library imports
import os
import json
from datetime import datetime
from io import StringIO
import numpy as np
import pandas as pd
import yfinance as yf
from flask import Flask, render_template, request, jsonify

# Local imports
from yfinance_data import get_stock_data, get_tickers
from indicators import (
    calculate_indicators, calculate_garman_klass_volatility, 
    calculate_rsi, calculate_bollinger_bands, calculate_atr, 
    calculate_dollar_volume, calculate_percent_change, 
    calculate_sma, calculate_pe_ratio
)

# Flask app initialization
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Custom JSON encoder to handle NumPy and Pandas data types
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if pd.isna(obj):
            return None
        return super(NpEncoder, self).default(obj)

@app.route('/')
def index():
    """Render the main dashboard page with available stock tickers."""
    tickers = get_tickers()
    return render_template('dashboard.html', tickers=tickers)

@app.route('/api/get_stock_data')
def api_get_stock_data():
    """
    API endpoint to fetch stock data and calculate indicators.
    
    Query parameters:
    - symbol: Stock symbol (default: AAPL)
    - start: Start date (default: 2024-01-01)
    - end: End date (default: current date)
    """
    try:
        # Extract query parameters
        symbol = request.args.get('symbol', 'AAPL')
        start_date = request.args.get('start', '2024-01-01')
        end_date = request.args.get('end', datetime.now().strftime('%Y-%m-%d'))
        
        print(f"Fetching data for {symbol} from {start_date} to {end_date}")
        
        # Fetch stock data
        stock_data = get_stock_data(symbol, start_date, end_date)
        
        if stock_data.empty:
            return jsonify({'error': 'No data available for the specified date range'}), 404
        
        # Fetch additional stock info
        stock = yf.Ticker(symbol)
        earnings_per_share = stock.info.get('trailingEps', 0)
        
        # Calculate indicators
        indicators = calculate_indicators(stock_data, earnings_per_share)
        
        # Prepare response data
        stock_data.index = stock_data.index.strftime('%Y-%m-%d')
        stock_data_dict = stock_data.reset_index().to_dict(orient='records')
        
        # Ensure all indicator values are serializable
        indicators_dict = {
            key: value.tolist() if isinstance(value, (pd.Series, np.ndarray)) else value
            for key, value in indicators.items()
        }
        
        response_data = {
            'stock_data': stock_data_dict,
            'indicators': indicators_dict
        }
        
        print("Data prepared successfully")
        return json.dumps(response_data, cls=NpEncoder), 200, {'Content-Type': 'application/json'}
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/export_csv')
def export_csv():
    """
    API endpoint to export stock data and indicators as CSV.
    
    Query parameters:
    - symbol: Stock symbol (default: AAPL)
    - start: Start date (default: 2020-01-01)
    - end: End date (default: current date)
    """
    try:
        # Extract query parameters
        symbol = request.args.get('symbol', 'AAPL')
        start_date = request.args.get('start', '2020-01-01')
        end_date = request.args.get('end', datetime.now().strftime('%Y-%m-%d'))
        
        # Fetch stock data
        stock_data = get_stock_data(symbol, start_date, end_date)
        
        if stock_data.empty:
            return jsonify({'error': 'No data available for the specified date range'}), 404
        
        # Fetch additional stock info
        stock = yf.Ticker(symbol)
        earnings_per_share = stock.info.get('trailingEps', 0)
        
        # Calculate indicators
        combined_data = stock_data.copy()
        combined_data['garman_klass'] = calculate_garman_klass_volatility(combined_data)
        combined_data['rsi'] = calculate_rsi(combined_data)
        upper, middle, lower = calculate_bollinger_bands(combined_data)
        combined_data['bollinger_upper'] = upper
        combined_data['bollinger_middle'] = middle
        combined_data['bollinger_lower'] = lower
        combined_data['atr'] = calculate_atr(combined_data)
        combined_data['dollar_volume'] = calculate_dollar_volume(combined_data)
        combined_data['percent_change'] = calculate_percent_change(combined_data)
        combined_data['sma_20'] = calculate_sma(combined_data, window=20)
        combined_data['sma_50'] = calculate_sma(combined_data, window=50)
        combined_data['pe_ratio'] = calculate_pe_ratio(combined_data, earnings_per_share)
        
        # Convert the DataFrame to CSV string
        csv_buffer = StringIO()
        combined_data.to_csv(csv_buffer, index=True)
        csv_string = csv_buffer.getvalue()
        
        return jsonify({'csv_data': csv_string, 'filename': f'{symbol}_data.csv'})
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
