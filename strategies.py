"""
Investment Strategies Module
Backtest different investment strategies and compare results.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class InvestmentStrategy:
    """Base class for investment strategies"""
    
    def __init__(self, ticker):
        self.ticker = ticker
        self.results = None
        
    def backtest(self, start_date, end_date):
        """Run backtest - to be implemented by subclasses"""
        raise NotImplementedError


class DollarCostAveraging(InvestmentStrategy):
    """
    Dollar-Cost Averaging (DCA) Strategy
    Invest a fixed amount at regular intervals
    """
    
    def __init__(self, ticker, investment_amount, frequency='monthly'):
        """
        Parameters:
        -----------
        ticker : str
            Stock symbol
        investment_amount : float
            Amount to invest each period
        frequency : str
            'monthly', 'weekly', or 'daily'
        """
        super().__init__(ticker)
        self.investment_amount = investment_amount
        self.frequency = frequency
    
    def backtest(self, start_date, end_date, verbose=True):
        """
        Backtest DCA strategy
        
        Parameters:
        -----------
        start_date : str
            Start date for backtest
        end_date : str
            End date for backtest
        verbose : bool
            Print progress
            
        Returns:
        --------
        results : StrategyResults
            Backtest results
        """
        if verbose:
            print(f"Backtesting DCA for {self.ticker}...")
            print(f"  Investment: ${self.investment_amount} {self.frequency}")
            print(f"  Period: {start_date} to {end_date}")
        
        # Fetch data
        data = yf.download(self.ticker, start=start_date, end=end_date, progress=False)
        prices = data['Adj Close']
        
        # Determine investment dates based on frequency
        if self.frequency == 'monthly':
            investment_dates = pd.date_range(start=prices.index[0], end=prices.index[-1], freq='MS')
        elif self.frequency == 'weekly':
            investment_dates = pd.date_range(start=prices.index[0], end=prices.index[-1], freq='W')
        else:  # daily
            investment_dates = prices.index
        
        # Align investment dates with trading dates
        investment_dates = [d for d in investment_dates if d in prices.index]
        
        # Simulate investments
        shares_owned = 0
        investments = []
        share_history = []
        portfolio_values = []
        
        for date in prices.index:
            if date in investment_dates:
                price = prices[date]
                shares_bought = self.investment_amount / price
                shares_owned += shares_bought
                investments.append({
                    'date': date,
                    'price': price,
                    'amount': self.investment_amount,
                    'shares': shares_bought
                })
            
            # Record portfolio value at each trading day
            portfolio_value = shares_owned * prices[date]
            share_history.append(shares_owned)
            portfolio_values.append(portfolio_value)
        
        # Calculate results
        total_invested = len(investments) * self.investment_amount
        final_value = portfolio_values[-1]
        total_return = final_value - total_invested
        total_return_pct = (total_return / total_invested) if total_invested > 0 else 0
        
        results_data = pd.DataFrame({
            'date': prices.index,
            'price': prices.values,
            'shares_owned': share_history,
            'portfolio_value': portfolio_values
        })
        
        self.results = StrategyResults(
            strategy_name=f"DCA - ${self.investment_amount} {self.frequency}",
            ticker=self.ticker,
            data=results_data,
            total_invested=total_invested,
            final_value=final_value,
            total_return=total_return,
            total_return_pct=total_return_pct
        )
        
        if verbose:
            print(f"  ✓ Total Invested: ${total_invested:,.2f}")
            print(f"  ✓ Final Value: ${final_value:,.2f}")
            print(f"  ✓ Total Return: ${total_return:,.2f} ({total_return_pct:.1%})")
        
        return self.results


class LumpSumInvestment(InvestmentStrategy):
    """
    Lump Sum Investment Strategy
    Invest all money at once
    """
    
    def __init__(self, ticker, investment_amount):
        """
        Parameters:
        -----------
        ticker : str
            Stock symbol
        investment_amount : float
            Total amount to invest upfront
        """
        super().__init__(ticker)
        self.investment_amount = investment_amount
    
    def backtest(self, start_date, end_date, verbose=True):
        """Backtest lump sum investment"""
        if verbose:
            print(f"Backtesting Lump Sum Investment for {self.ticker}...")
            print(f"  Investment: ${self.investment_amount} at start")
            print(f"  Period: {start_date} to {end_date}")
        
        # Fetch data
        data = yf.download(self.ticker, start=start_date, end=end_date, progress=False)
        prices = data['Adj Close']
        
        # Invest at start
        start_price = prices.iloc[0]
        shares_owned = self.investment_amount / start_price
        
        # Calculate portfolio values over time
        portfolio_values = shares_owned * prices.values
        
        # Calculate results
        final_value = portfolio_values[-1]
        total_return = final_value - self.investment_amount
        total_return_pct = total_return / self.investment_amount
        
        results_data = pd.DataFrame({
            'date': prices.index,
            'price': prices.values,
            'shares_owned': [shares_owned] * len(prices),
            'portfolio_value': portfolio_values
        })
        
        self.results = StrategyResults(
            strategy_name=f"Lump Sum - ${self.investment_amount}",
            ticker=self.ticker,
            data=results_data,
            total_invested=self.investment_amount,
            final_value=final_value,
            total_return=total_return,
            total_return_pct=total_return_pct
        )
        
        if verbose:
            print(f"  ✓ Total Invested: ${self.investment_amount:,.2f}")
            print(f"  ✓ Final Value: ${final_value:,.2f}")
            print(f"  ✓ Total Return: ${total_return:,.2f} ({total_return_pct:.1%})")
        
        return self.results


class BuyAndHoldWithDividends(InvestmentStrategy):
    """
    Buy and Hold Strategy with Dividend Reinvestment
    """
    
    def __init__(self, ticker, investment_amount):
        super().__init__(ticker)
        self.investment_amount = investment_amount
    
    def backtest(self, start_date, end_date, verbose=True):
        """Backtest buy and hold with dividend reinvestment"""
        if verbose:
            print(f"Backtesting Buy & Hold (with dividends) for {self.ticker}...")
            print(f"  Investment: ${self.investment_amount}")
            print(f"  Period: {start_date} to {end_date}")
        
        # Fetch price and dividend data
        ticker_obj = yf.Ticker(self.ticker)
        data = yf.download(self.ticker, start=start_date, end=end_date, progress=False)
        try:
            dividends = ticker_obj.dividends[start_date:end_date]
        except:
            dividends = pd.Series(dtype='float64')
        
        prices = data['Adj Close']
        
        # Simulate with dividend reinvestment
        start_price = prices.iloc[0]
        shares_owned = self.investment_amount / start_price
        
        portfolio_values = []
        shares_history = []
        
        for date in prices.index:
            # Reinvest dividends
            if date in dividends.index:
                dividend_per_share = dividends[date]
                dividend_amount = shares_owned * dividend_per_share
                new_shares = dividend_amount / prices[date]
                shares_owned += new_shares
            
            portfolio_value = shares_owned * prices[date]
            portfolio_values.append(portfolio_value)
            shares_history.append(shares_owned)
        
        final_value = portfolio_values[-1]
        total_return = final_value - self.investment_amount
        total_return_pct = total_return / self.investment_amount
        
        results_data = pd.DataFrame({
            'date': prices.index,
            'price': prices.values,
            'shares_owned': shares_history,
            'portfolio_value': portfolio_values
        })
        
        self.results = StrategyResults(
            strategy_name=f"Buy & Hold (Div Reinvest) - ${self.investment_amount}",
            ticker=self.ticker,
            data=results_data,
            total_invested=self.investment_amount,
            final_value=final_value,
            total_return=total_return,
            total_return_pct=total_return_pct
        )
        
        if verbose:
            print(f"  ✓ Total Invested: ${self.investment_amount:,.2f}")
            print(f"  ✓ Final Value: ${final_value:,.2f}")
            print(f"  ✓ Total Return: ${total_return:,.2f} ({total_return_pct:.1%})")
        
        return self.results


class StrategyResults:
    """Container for backtest results"""
    
    def __init__(self, strategy_name, ticker, data, total_invested, 
                 final_value, total_return, total_return_pct):
        self.strategy_name = strategy_name
        self.ticker = ticker
        self.data = data
        self.total_invested = total_invested
        self.final_value = final_value
        self.total_return = total_return
        self.total_return_pct = total_return_pct
    
    def summary(self):
        """Print summary of results"""
        print(f"\n{self.strategy_name}")
        print("=" * 50)
        print(f"Ticker:          {self.ticker}")
        print(f"Total Invested:  ${self.total_invested:,.2f}")
        print(f"Final Value:     ${self.final_value:,.2f}")
        print(f"Total Return:    ${self.total_return:,.2f}")
        print(f"Return %:        {self.total_return_pct:>6.2%}")
        print("=" * 50)


if __name__ == "__main__":
    print("Investment Strategies Module")
    print("Import and use in your scripts: from strategies import DollarCostAveraging")
