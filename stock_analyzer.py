"""
Stock Analyzer Module
Fetches, analyzes, and visualizes historical stock data.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class StockAnalyzer:
    """Analyze and compare multiple stocks"""
    
    def __init__(self, tickers, start_date=None, end_date=None):
        """
        Initialize the stock analyzer
        
        Parameters:
        -----------
        tickers : list or str
            Stock ticker symbols (e.g., ['AAPL', 'MSFT'])
        start_date : str
            Start date for historical data (format: 'YYYY-MM-DD')
        end_date : str
            End date for historical data (format: 'YYYY-MM-DD')
        """
        if isinstance(tickers, str):
            tickers = [tickers]
        
        self.tickers = tickers
        self.start_date = start_date or (datetime.now() - timedelta(days=365*5)).strftime('%Y-%m-%d')
        self.end_date = end_date or datetime.now().strftime('%Y-%m-%d')
        self.data = {}
        self.returns = {}
        self.stats = {}
        
    def fetch_data(self, verbose=True):
        """
        Fetch historical stock data from Yahoo Finance
        
        Parameters:
        -----------
        verbose : bool
            Print progress messages
        """
        if verbose:
            print(f"Fetching data for {len(self.tickers)} stocks...")
            print(f"Date range: {self.start_date} to {self.end_date}")
        
        for ticker in self.tickers:
            try:
                if verbose:
                    print(f"  Downloading {ticker}...", end=" ")
                
                data = yf.download(
                    ticker,
                    start=self.start_date,
                    end=self.end_date,
                    progress=False
                )
                
                self.data[ticker] = data
                if verbose:
                    print(f"✓ ({len(data)} days)")
                    
            except Exception as e:
                if verbose:
                    print(f"✗ Error: {e}")
    
    def calculate_returns(self, verbose=True):
        """Calculate daily and cumulative returns for each stock"""
        if not self.data:
            raise ValueError("No data fetched. Call fetch_data() first.")
        
        if verbose:
            print("\nCalculating returns...")
        
        for ticker, prices in self.data.items():
            # Daily returns
            daily_returns = prices['Adj Close'].pct_change()
            
            # Cumulative returns (percentage)
            cumulative_returns = (1 + daily_returns).cumprod() - 1
            
            self.returns[ticker] = {
                'daily': daily_returns,
                'cumulative': cumulative_returns,
                'prices': prices['Adj Close']
            }
        
        if verbose:
            print(f"✓ Returns calculated for {len(self.returns)} stocks")
    
    def calculate_statistics(self, verbose=True):
        """Calculate key statistics for each stock"""
        if not self.returns:
            self.calculate_returns(verbose=False)
        
        if verbose:
            print("\nCalculating statistics...")
        
        for ticker in self.tickers:
            daily_ret = self.returns[ticker]['daily'].dropna()
            cum_ret = self.returns[ticker]['cumulative']
            prices = self.returns[ticker]['prices']
            
            # Total return
            total_return = cum_ret.iloc[-1]
            
            # Annualized return
            years = len(daily_ret) / 252  # Trading days per year
            annualized_return = (1 + total_return) ** (1 / years) - 1
            
            # Volatility (annualized)
            volatility = daily_ret.std() * np.sqrt(252)
            
            # Sharpe ratio (assuming 2% risk-free rate)
            risk_free_rate = 0.02
            sharpe_ratio = (annualized_return - risk_free_rate) / volatility if volatility > 0 else 0
            
            # Maximum drawdown
            running_max = cum_ret.expanding().max()
            drawdown = (cum_ret - running_max) / (1 + running_max)
            max_drawdown = drawdown.min()
            
            # Price statistics
            current_price = prices.iloc[-1]
            start_price = prices.iloc[0]
            high = prices.max()
            low = prices.min()
            
            self.stats[ticker] = {
                'total_return': total_return,
                'annualized_return': annualized_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown,
                'current_price': current_price,
                'start_price': start_price,
                'high': high,
                'low': low,
                'days_traded': len(daily_ret)
            }
        
        if verbose:
            print("✓ Statistics calculated")
    
    def print_summary(self):
        """Print a summary of statistics for all stocks"""
        if not self.stats:
            self.calculate_statistics(verbose=False)
        
        print("\n" + "="*80)
        print("STOCK ANALYSIS SUMMARY")
        print("="*80)
        
        for ticker in self.tickers:
            stats = self.stats[ticker]
            print(f"\n{ticker}")
            print("-" * 40)
            print(f"  Total Return:        {stats['total_return']:>8.1%}")
            print(f"  Annualized Return:   {stats['annualized_return']:>8.1%}")
            print(f"  Volatility (Annual): {stats['volatility']:>8.1%}")
            print(f"  Sharpe Ratio:        {stats['sharpe_ratio']:>8.2f}")
            print(f"  Max Drawdown:        {stats['max_drawdown']:>8.1%}")
            print(f"  Current Price:       ${stats['current_price']:>8.2f}")
            print(f"  Start Price:         ${stats['start_price']:>8.2f}")
            print(f"  52-Week High:        ${stats['high']:>8.2f}")
            print(f"  52-Week Low:         ${stats['low']:>8.2f}")
    
    def get_summary_dataframe(self):
        """Return statistics as a pandas DataFrame"""
        if not self.stats:
            self.calculate_statistics(verbose=False)
        
        df = pd.DataFrame(self.stats).T
        return df


def compare_stocks(tickers, start_date=None, end_date=None):
    """
    Convenience function to quickly analyze and compare stocks
    
    Parameters:
    -----------
    tickers : list
        List of stock symbols
    start_date : str
        Start date for analysis
    end_date : str
        End date for analysis
        
    Returns:
    --------
    analyzer : StockAnalyzer
        Initialized and analyzed StockAnalyzer object
    """
    analyzer = StockAnalyzer(tickers, start_date, end_date)
    analyzer.fetch_data()
    analyzer.calculate_returns()
    analyzer.calculate_statistics()
    return analyzer


if __name__ == "__main__":
    # Example usage
    print("Stock Analyzer Module")
    print("Import and use in your scripts: from stock_analyzer import StockAnalyzer")
