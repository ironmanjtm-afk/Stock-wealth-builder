# Stock Wealth Builder - Educational Data Analysis

Learn how to grow your wealth through stock investing with interactive data analysis and visualizations.

## Overview

This project provides educational tools to analyze stock data, backtest investment strategies, and visualize portfolio growth. It demonstrates key principles like compound interest, dollar-cost averaging, and diversification.

## Features

- **Stock Data Analysis**: Fetch and analyze historical stock prices
- **Strategy Backtesting**: Test different investment approaches
- **Portfolio Visualization**: See your wealth grow over time
- **Risk Analysis**: Understand volatility and drawdowns
- **Comparison Tools**: Compare different stocks and strategies
- **Interactive Reports**: Generate detailed analysis reports

## Installation

```bash
# Clone the repository
git clone https://github.com/ironmanjtm-afk/stock-wealth-builder.git
cd stock-wealth-builder

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
from stock_analyzer import compare_stocks
from visualizations import StockVisualizer

# Analyze stocks
analyzer = compare_stocks(['AAPL', 'MSFT', 'GOOGL'])
analyzer.print_summary()

# Visualize
visualizer = StockVisualizer()
cum_returns = {ticker: data['cumulative'] for ticker, data in analyzer.returns.items()}
visualizer.plot_cumulative_returns(cum_returns)
```

## Running Examples

```bash
# Basic stock analysis
python examples/basic_analysis.py

# Compare investment strategies
python examples/strategy_comparison.py

# Risk analysis
python examples/risk_analysis.py

# Wealth projection
python examples/wealth_projection.py
```

## Project Structure

```
stock-wealth-builder/
├── stock_analyzer.py          # Main stock data analysis
├── strategies.py              # Investment strategies
├── visualizations.py          # Plotting utilities
├── examples/                  # Example scripts
│   ├── basic_analysis.py
│   ├── strategy_comparison.py
│   ├── risk_analysis.py
│   └── wealth_projection.py
├── requirements.txt
└── README.md
```

## Key Concepts Demonstrated

### 1. Compound Interest
Watch how your money grows exponentially over time through reinvested dividends and capital appreciation.

### 2. Dollar-Cost Averaging
Invest a fixed amount regularly to reduce the impact of market volatility.

### 3. Diversification
Reduce risk by spreading investments across multiple stocks and sectors.

### 4. Risk vs. Return
Understand the trade-off between potential gains and volatility.

### 5. Buy and Hold
See the power of long-term investing vs. short-term trading.

## Example Use Cases

- Analyze 5-year performance of major tech stocks
- Compare AAPL vs. MSFT total returns
- Backtest $500/month investing in a stock
- Calculate compound annual growth rate (CAGR)
- Visualize the impact of market crashes
- Track portfolio diversification

## Data Sources

- **yfinance**: Yahoo Finance historical stock data
- **Free tier**: No API key required
- **Data Range**: Up to 20+ years of historical data

## Educational Value

This project teaches:
- How financial markets work
- Python data analysis with pandas and numpy
- Data visualization with matplotlib and plotly
- Quantitative analysis and backtesting
- Risk assessment and portfolio theory

## Disclaimer

This is for **educational purposes only**. Past performance does not guarantee future results. Always consult with a financial advisor before making investment decisions. This code does not provide financial advice.

## License

MIT License - Feel free to use this for learning and education.

## Contributing

Have ideas for improvements? Feel free to submit issues or pull requests!
