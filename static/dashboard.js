// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function() {
    // Constants for date handling
    const TODAY = new Date();
    const DEFAULT_START_DATE = '2024-01-01';
    const DEFAULT_END_DATE = TODAY.toISOString().split('T')[0];

    // DOM elements
    const symbolElement = document.getElementById('symbol');
    const startDateElement = document.getElementById('start_date');
    const endDateElement = document.getElementById('end_date');
    const companyNameElement = document.getElementById('company_name');
    const filterButton = document.getElementById('filter');
    const exportButton = document.getElementById('export');

    // Set default date values
    startDateElement.value = DEFAULT_START_DATE;
    endDateElement.value = DEFAULT_END_DATE;

    // Chart configuration
    const BASE_LAYOUT = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#ffffff' },
        xaxis: { 
            gridcolor: '#4a4e69', 
            linecolor: '#4a4e69',
            rangeslider: { visible: false }
        },
        yaxis: { gridcolor: '#4a4e69', linecolor: '#4a4e69' },
        margin: { l: 50, r: 50, t: 50, b: 50 },
        responsive: true,
        autosize: true,
        height: 400 // Fixed height for all charts
    };

    /**
     * Updates the company name displayed on the page
     */
    function updateCompanyName() {
        companyNameElement.textContent = symbolElement.value;
    }

    /**
     * Creates or updates a chart with the given data and layout
     * @param {string} divId - The ID of the div element to render the chart in
     * @param {Array} traces - The data traces for the chart
     * @param {string} layoutTitle - The title for the chart
     * @param {Object} additionalLayout - Additional layout options to merge
     */
    function createOrUpdateChart(divId, traces, layoutTitle, additionalLayout = {}) {
        Plotly.react(divId, traces, { 
            ...BASE_LAYOUT, 
            title: layoutTitle,
            ...additionalLayout
        });
    }

    /**
     * Fetches stock data and updates all charts
     */
    function updateCharts() {
        const symbol = symbolElement.value;
        const startDate = startDateElement.value || DEFAULT_START_DATE;
        const endDate = endDateElement.value || DEFAULT_END_DATE;

        console.log('Fetching data for:', symbol, startDate, endDate);

        fetch(`/api/get_stock_data?symbol=${symbol}&start=${startDate}&end=${endDate}`)
            .then(response => response.json())
            .then(data => {
                console.log('Received data:', data);

                const { stock_data: stockData, indicators } = data;

                if (!stockData || stockData.length === 0) {
                    console.error('No stock data received');
                    return;
                }

                // Update all charts
                updateStockPriceChart(stockData);
                updateGarmanKlassChart(stockData, indicators);
                updateRSIChart(stockData, indicators);
                updateBollingerBandsChart(stockData, indicators);
                updateATRChart(stockData, indicators);
                updateDollarVolumeChart(stockData, indicators);
                updatePercentChangeChart(stockData, indicators);
                updateMovingAveragesChart(stockData, indicators);
                updatePERatioChart(stockData, indicators);

                // Update company name after loading data
                updateCompanyName();
            })
            .catch(error => {
                console.error("Error fetching data:", error);
            });
    }

    /**
     * Updates the Stock Price and Volume chart
     * @param {Array} stockData - The stock data array
     */
    function updateStockPriceChart(stockData) {
        createOrUpdateChart('stock_price', [
            {
                x: stockData.map(d => d.Date),
                open: stockData.map(d => d.Open),
                high: stockData.map(d => d.High),
                low: stockData.map(d => d.Low),
                close: stockData.map(d => d.Close),
                type: 'candlestick',
                xaxis: 'x',
                yaxis: 'y'
            },
            {
                x: stockData.map(d => d.Date),
                y: stockData.map(d => d.Volume),
                type: 'bar',
                yaxis: 'y2',
                name: 'Volume',
                marker: {
                    color: stockData.map(d => d.Close >= d.Open ? 'rgba(0, 255, 0, 0.3)' : 'rgba(255, 0, 0, 0.3)')
                }
            }
        ], 'Stock Price and Volume', {
            dragmode: 'zoom',
            showlegend: false,
            xaxis: {
                rangeslider: { visible: false },
                title: 'Date'
            },
            yaxis: { title: 'Price' },
            yaxis2: {
                title: 'Volume',
                overlaying: 'y',
                side: 'right'
            }
        });
    }

    /**
     * Updates the Garman-Klass Volatility chart
     * @param {Array} stockData - The stock data array
     * @param {Object} indicators - The calculated indicators
     */
    function updateGarmanKlassChart(stockData, indicators) {
        createOrUpdateChart('garman_klass', [{
            x: stockData.map(d => d.Date),
            y: indicators.garman_klass,
            type: 'scatter',
            mode: 'lines',
            line: { color: '#4cc9f0' }
        }], 'Garman-Klass Volatility');
    }

    /**
     * Updates the RSI chart
     * @param {Array} stockData - The stock data array
     * @param {Object} indicators - The calculated indicators
     */
    function updateRSIChart(stockData, indicators) {
        createOrUpdateChart('rsi', [{
            x: stockData.map(d => d.Date),
            y: indicators.rsi,
            type: 'scatter',
            mode: 'lines',
            line: { color: '#f72585' }
        }], 'RSI');
    }

    /**
     * Updates the Bollinger Bands chart
     * @param {Array} stockData - The stock data array
     * @param {Object} indicators - The calculated indicators
     */
    function updateBollingerBandsChart(stockData, indicators) {
        createOrUpdateChart('bollinger_bands', [
            {
                x: stockData.map(d => d.Date),
                y: stockData.map(d => d.Close),
                type: 'scatter',
                mode: 'lines',
                name: 'Price',
                line: { color: '#4361ee' }
            },
            {
                x: stockData.map(d => d.Date),
                y: indicators.bollinger_upper,
                type: 'scatter',
                mode: 'lines',
                name: 'Upper Band',
                line: { color: '#4cc9f0' }
            },
            {
                x: stockData.map(d => d.Date),
                y: indicators.bollinger_lower,
                type: 'scatter',
                mode: 'lines',
                name: 'Lower Band',
                line: { color: '#f72585' }
            }
        ], 'Bollinger Bands');
    }

    /**
     * Updates the ATR (Average True Range) chart
     * @param {Array} stockData - The stock data array
     * @param {Object} indicators - The calculated indicators
     */
    function updateATRChart(stockData, indicators) {
        createOrUpdateChart('atr', [{
            x: stockData.map(d => d.Date),
            y: indicators.atr,
            type: 'scatter',
            mode: 'lines',
            line: { color: '#7209b7' }
        }], 'ATR (Average True Range)');
    }

    /**
     * Updates the Dollar Volume chart
     * @param {Array} stockData - The stock data array
     * @param {Object} indicators - The calculated indicators
     */
    function updateDollarVolumeChart(stockData, indicators) {
        createOrUpdateChart('dollar_volume', [{
            x: stockData.map(d => d.Date),
            y: indicators.dollar_volume,
            type: 'bar',
            marker: { color: '#3a0ca3' }
        }], 'Dollar Volume');
    }

    /**
     * Updates the Percent Change chart
     * @param {Array} stockData - The stock data array
     * @param {Object} indicators - The calculated indicators
     */
    function updatePercentChangeChart(stockData, indicators) {
        createOrUpdateChart('percent_change', [{
            x: stockData.map(d => d.Date),
            y: indicators.percent_change,
            type: 'bar',
            name: 'Percent Change',
            marker: {
                color: indicators.percent_change.map(v => v >= 0 ? 'green' : 'red')
            }
        }], 'Daily Percent Change');
    }

    /**
     * Updates the Moving Averages chart
     * @param {Array} stockData - The stock data array
     * @param {Object} indicators - The calculated indicators
     */
    function updateMovingAveragesChart(stockData, indicators) {
        createOrUpdateChart('moving_averages', [
            {
                x: stockData.map(d => d.Date),
                y: stockData.map(d => d.Close),
                type: 'scatter',
                mode: 'lines',
                name: 'Close Price',
                line: { color: '#4361ee' }
            },
            {
                x: stockData.map(d => d.Date),
                y: indicators.sma_20,
                type: 'scatter',
                mode: 'lines',
                name: '20-day SMA',
                line: { color: '#f72585' }
            },
            {
                x: stockData.map(d => d.Date),
                y: indicators.sma_50,
                type: 'scatter',
                mode: 'lines',
                name: '50-day SMA',
                line: { color: '#4cc9f0' }
            }
        ], 'Moving Averages');
    }

    /**
     * Updates the Price-to-Earnings Ratio chart
     * @param {Array} stockData - The stock data array
     * @param {Object} indicators - The calculated indicators
     */
    function updatePERatioChart(stockData, indicators) {
        createOrUpdateChart('pe_ratio', [{
            x: stockData.map(d => d.Date),
            y: indicators.pe_ratio,
            type: 'scatter',
            mode: 'lines',
            name: 'P/E Ratio',
            line: { color: '#7209b7' }
        }], 'Price-to-Earnings Ratio');
    }

    /**
     * Exports the stock data as a CSV file
     */
    function exportCSV() {
        const symbol = symbolElement.value;
        const startDate = startDateElement.value || DEFAULT_START_DATE;
        const endDate = endDateElement.value || DEFAULT_END_DATE;

        const url = `/api/export_csv?symbol=${symbol}&start=${startDate}&end=${endDate}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Error exporting CSV:', data.error);
                    alert('Error exporting CSV. Please try again.');
                    return;
                }

                // Create and trigger download of CSV file
                const blob = new Blob([data.csv_data], { type: 'text/csv;charset=utf-8;' });
                const link = document.createElement('a');
                if (link.download !== undefined) {
                    const url = URL.createObjectURL(blob);
                    link.setAttribute('href', url);
                    link.setAttribute('download', data.filename);
                    link.style.visibility = 'hidden';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }
            })
            .catch(error => {
                console.error('Error exporting CSV:', error);
                alert('Error exporting CSV. Please try again.');
            });
    }

    // Event listeners
    filterButton.addEventListener('click', updateCharts);
    exportButton.addEventListener('click', exportCSV);

    // Load initial data
    updateCharts();

    // Resize charts when window size changes
    window.addEventListener('resize', function() {
        const graphs = document.querySelectorAll('.graph');
        graphs.forEach(graph => {
            Plotly.relayout(graph.id, {
                width: graph.offsetWidth,
                height: 400
            });
        });
    });
});