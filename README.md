# S&P 500 Dashboard App

This web application provides a dashboard for visualizing and analyzing S&P 500 stock data using various technical indicators.

## Project Structure

```
sp500-dashboard-app/
│
├── app.py
├── indicators.py
├── yfinance_data.py
├── requirements.txt
├── static/
│ ├── dashboard.js
│ └── style.css
└── templates/
└── index.html
```

## Features

- Fetches real-time S&P 500 stock data using yfinance
- Calculates and displays technical indicators:
  - Simple Moving Average (SMA)
  - Relative Strength Index (RSI)
  - Moving Average Convergence Divergence (MACD)
  - Bollinger Bands
  - Average True Range (ATR)
  - Garman Klass Volatility
  - Dollar Volume
  - Percent Change
  - Price to Earnings Ratio (PE Ratio)
- Interactive charts using Plotly
- Responsive design for various screen sizes

## Technical Details

### Backend

- Built with Flask, a lightweight WSGI web application framework in Python
- RESTful API endpoints for fetching stock data and calculating indicators
- Asynchronous data processing to handle multiple requests efficiently
- Utilizes yfinance for fetching stock data
- Calculates indicators using custom algorithms

### Frontend

- Responsive HTML5 layout with CSS3 for styling
- Interactive JavaScript using modern ES6+ features
- Dynamic chart rendering with Plotly.js
- AJAX calls to backend API for real-time data updates

### Data Manipulation and Analysis

- Utilizes pandas for efficient data manipulation and analysis
- NumPy for numerical computations and array operations
- Custom algorithms for calculating various technical indicators

### Data Cleaning

- Handles missing data points through interpolation
- Removes outliers using statistical methods
- Normalizes data for consistent analysis across different stocks

### Data Fetching

- Uses yfinance library to fetch real-time and historical stock data
- Implements caching mechanism to reduce API calls and improve performance
- Error handling for network issues and API limitations

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sp500-dashboard-app.git
   cd sp500-dashboard-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`

3. Use the dashboard to select stocks, timeframes, and indicators for analysis

## Files Description

- `app.py`: Main Flask application file, handles routing and API endpoints
- `indicators.py`: Contains functions for calculating technical indicators
- `yfinance_data.py`: Manages stock data fetching and preprocessing using yfinance
- `requirements.txt`: Lists all Python dependencies
- `static/dashboard.js`: JavaScript file for interactive dashboard functionality, chart updates, and API calls
- `static/style.css`: CSS file for styling the dashboard and ensuring responsiveness
- `templates/index.html`: HTML template for the dashboard layout

## Dependencies

- Flask: Web framework for the backend
- yfinance: Library for fetching stock data
- pandas: Data manipulation and analysis
- numpy: Numerical computing tools
- plotly: Interactive plotting library
- jinja2: Templating engine for Python

## Performance Considerations

- Implements caching to reduce redundant API calls
- Uses asynchronous processing for improved response times
- Optimizes data structures for efficient memory usage

## Security Measures

- Input validation to prevent injection attacks
- Rate limiting to protect against abuse
- HTTPS enforcement for secure data transmission
