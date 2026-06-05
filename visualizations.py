"""
Visualization Module
Create interactive and static plots for stock analysis.
"""

import matplotlib.pyplot as plt
import numpy as np


class StockVisualizer:
    """Create visualizations for stock analysis"""
    
    @staticmethod
    def plot_price_history(stock_data, title="Stock Price History", figsize=(14, 6)):
        """
        Plot price history for one or more stocks
        
        Parameters:
        -----------
        stock_data : dict or pd.Series
            Either a dict with stock data or a single Series
        title : str
            Plot title
        figsize : tuple
            Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        if isinstance(stock_data, dict):
            for ticker, prices in stock_data.items():
                ax.plot(prices.index, prices.values, label=ticker, linewidth=2)
        else:
            ax.plot(stock_data.index, stock_data.values, linewidth=2)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_cumulative_returns(returns_data, title="Cumulative Returns", figsize=(14, 6)):
        """
        Plot cumulative returns over time
        
        Parameters:
        -----------
        returns_data : dict
            Dict with cumulative returns for each stock
        title : str
            Plot title
        figsize : tuple
            Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        for ticker, cum_returns in returns_data.items():
            ax.plot(cum_returns.index, cum_returns.values * 100, label=ticker, linewidth=2)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Return (%)', fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_drawdown(returns_data, title="Drawdown Over Time", figsize=(14, 6)):
        """
        Plot drawdown (peak-to-trough decline) over time
        
        Parameters:
        -----------
        returns_data : dict
            Dict with cumulative returns
        title : str
            Plot title
        figsize : tuple
            Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        for ticker, cum_returns in returns_data.items():
            running_max = cum_returns.expanding().max()
            drawdown = (cum_returns - running_max) / (1 + running_max)
            ax.plot(drawdown.index, drawdown.values * 100, label=ticker, linewidth=2)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Drawdown (%)', fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.fill_between(ax.get_xlim(), 0, -100, alpha=0.1, color='red')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_strategy_comparison(strategy_results_list, figsize=(14, 7)):
        """
        Compare multiple strategy results
        
        Parameters:
        -----------
        strategy_results_list : list
            List of StrategyResults objects
        figsize : tuple
            Figure size
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Portfolio value comparison
        for results in strategy_results_list:
            ax1.plot(results.data['date'], results.data['portfolio_value'], 
                    label=results.strategy_name, linewidth=2, marker='o', markersize=2)
        
        ax1.set_title('Portfolio Value Over Time', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Date', fontsize=11)
        ax1.set_ylabel('Value ($)', fontsize=11)
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Return comparison
        names = [r.strategy_name for r in strategy_results_list]
        returns = [r.total_return_pct * 100 for r in strategy_results_list]
        colors = ['green' if r > 0 else 'red' for r in returns]
        
        bars = ax2.bar(range(len(names)), returns, color=colors, alpha=0.7)
        ax2.set_title('Total Return Comparison', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Return (%)', fontsize=11)
        ax2.set_xticks(range(len(names)))
        ax2.set_xticklabels(names, rotation=45, ha='right', fontsize=9)
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
        
        # Add value labels on bars
        for bar, ret in zip(bars, returns):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{ret:.1f}%', ha='center', va='bottom' if height > 0 else 'top',
                    fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_volatility_comparison(stats_df, figsize=(10, 6)):
        """
        Plot volatility comparison for multiple stocks
        
        Parameters:
        -----------
        stats_df : pd.DataFrame
            DataFrame with stock statistics
        figsize : tuple
            Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        volatilities = stats_df['volatility'] * 100
        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(volatilities)))
        
        bars = ax.bar(range(len(volatilities)), volatilities, color=colors, alpha=0.8)
        ax.set_title('Annualized Volatility by Stock', fontsize=12, fontweight='bold')
        ax.set_ylabel('Volatility (%)', fontsize=11)
        ax.set_xlabel('Stock', fontsize=11)
        ax.set_xticks(range(len(volatilities)))
        ax.set_xticklabels(volatilities.index, fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, vol in zip(bars, volatilities):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{vol:.1f}%', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_risk_return_scatter(stats_df, figsize=(10, 8)):
        """
        Scatter plot of risk vs return for stocks
        
        Parameters:
        -----------
        stats_df : pd.DataFrame
            DataFrame with stock statistics
        figsize : tuple
            Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        returns = stats_df['annualized_return'] * 100
        risks = stats_df['volatility'] * 100
        
        scatter = ax.scatter(risks, returns, s=200, alpha=0.6, 
                            c=stats_df['sharpe_ratio'], cmap='viridis')
        
        for idx, ticker in enumerate(stats_df.index):
            ax.annotate(ticker, (risks.iloc[idx], returns.iloc[idx]),
                       fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Risk (Volatility %)', fontsize=12)
        ax.set_ylabel('Return (Annualized %)', fontsize=12)
        ax.set_title('Risk vs Return Profile', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Sharpe Ratio', fontsize=11)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_distribution_of_returns(returns_dict, title="Distribution of Daily Returns", figsize=(14, 6)):
        """
        Plot histogram of daily returns
        
        Parameters:
        -----------
        returns_dict : dict
            Dict with daily returns for each stock
        title : str
            Plot title
        figsize : tuple
            Figure size
        """
        fig, axes = plt.subplots(1, len(returns_dict), figsize=figsize)
        
        if len(returns_dict) == 1:
            axes = [axes]
        
        for ax, (ticker, daily_returns) in zip(axes, returns_dict.items()):
            daily_returns = daily_returns.dropna() * 100
            
            ax.hist(daily_returns, bins=50, alpha=0.7, color='steelblue', edgecolor='black')
            ax.set_title(f'{ticker} Daily Returns', fontsize=11, fontweight='bold')
            ax.set_xlabel('Return (%)', fontsize=10)
            ax.set_ylabel('Frequency', fontsize=10)
            ax.grid(True, alpha=0.3, axis='y')
            
            mean_ret = daily_returns.mean()
            ax.axvline(mean_ret, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_ret:.2f}%')
            ax.legend(fontsize=9)
        
        fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        return fig


def show_all_plots():
    """Display all plots"""
    plt.show()


if __name__ == "__main__":
    print("Visualization Module")
    print("Import and use in your scripts: from visualizations import StockVisualizer")
