"""
Basic Stock Analysis Example
Learn the fundamentals of stock analysis
"""

from stock_analyzer import compare_stocks
from visualizations import StockVisualizer
import matplotlib.pyplot as plt


def main():
    print("="*60)
    print("STOCK WEALTH BUILDER - BASIC ANALYSIS")
    print("="*60)
    
    # Analyze major tech stocks
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    
    print(f"\nAnalyzing {len(tickers)} stocks over the last 5 years...")
    analyzer = compare_stocks(tickers)
    
    # Print summary
    analyzer.print_summary()
    
    # Get statistics as dataframe
    stats_df = analyzer.get_summary_dataframe()
    print("\nStatistics Summary:")
    print(stats_df[['total_return', 'annualized_return', 'volatility', 'sharpe_ratio']])
    
    # Create visualizations
    print("\nGenerating visualizations...")
    
    visualizer = StockVisualizer()
    
    # 1. Price History
    fig1 = visualizer.plot_price_history(
        analyzer.returns, 
        "Tech Stocks - Price History (5 Years)"
    )
    plt.savefig('price_history.png', dpi=100, bbox_inches='tight')
    print("  ✓ Saved: price_history.png")
    
    # 2. Cumulative Returns
    cum_returns = {ticker: data['cumulative'] for ticker, data in analyzer.returns.items()}
    fig2 = visualizer.plot_cumulative_returns(
        cum_returns,
        "Tech Stocks - Cumulative Returns"
    )
    plt.savefig('cumulative_returns.png', dpi=100, bbox_inches='tight')
    print("  ✓ Saved: cumulative_returns.png")
    
    # 3. Drawdown Analysis
    fig3 = visualizer.plot_drawdown(
        cum_returns,
        "Tech Stocks - Maximum Drawdown Analysis"
    )
    plt.savefig('drawdown.png', dpi=100, bbox_inches='tight')
    print("  ✓ Saved: drawdown.png")
    
    # 4. Risk vs Return
    fig4 = visualizer.plot_risk_return_scatter(stats_df)
    plt.savefig('risk_vs_return.png', dpi=100, bbox_inches='tight')
    print("  ✓ Saved: risk_vs_return.png")
    
    # 5. Volatility Comparison
    fig5 = visualizer.plot_volatility_comparison(stats_df)
    plt.savefig('volatility.png', dpi=100, bbox_inches='tight')
    print("  ✓ Saved: volatility.png")
    
    # 6. Returns Distribution
    daily_returns = {ticker: data['daily'] for ticker, data in analyzer.returns.items()}
    fig6 = visualizer.plot_distribution_of_returns(
        daily_returns,
        "Tech Stocks - Distribution of Daily Returns"
    )
    plt.savefig('returns_distribution.png', dpi=100, bbox_inches='tight')
    print("  ✓ Saved: returns_distribution.png")
    
    print("\n" + "="*60)
    print("KEY INSIGHTS")
    print("="*60)
    
    # Find best and worst performers
    best_ticker = stats_df['total_return'].idxmax()
    best_return = stats_df['total_return'].max()
    worst_ticker = stats_df['total_return'].idxmin()
    worst_return = stats_df['total_return'].min()
    
    print(f"\n✓ Best Performer: {best_ticker} ({best_return:.1%})")
    print(f"✓ Worst Performer: {worst_ticker} ({worst_return:.1%})")
    
    # Risk analysis
    highest_vol = stats_df['volatility'].idxmax()
    lowest_vol = stats_df['volatility'].idxmin()
    print(f"\n✓ Highest Volatility: {highest_vol} ({stats_df.loc[highest_vol, 'volatility']:.1%})")
    print(f"✓ Lowest Volatility: {lowest_vol} ({stats_df.loc[lowest_vol, 'volatility']:.1%})")
    
    # Risk-adjusted returns
    best_sharpe = stats_df['sharpe_ratio'].idxmax()
    print(f"\n✓ Best Risk-Adjusted Return (Sharpe): {best_sharpe} ({stats_df.loc[best_sharpe, 'sharpe_ratio']:.2f})")
    
    print("\n" + "="*60)
    print("LEARNING POINTS")
    print("="*60)
    print("""
1. TOTAL RETURN: Shows your total profit/loss over the period
   - Higher return = more profit, but may come with higher risk

2. ANNUALIZED RETURN: What your annual return would be if consistent
   - Makes it easier to compare investments across different time periods

3. VOLATILITY: Measures how much the price fluctuates
   - Higher volatility = more risk = wider price swings

4. SHARPE RATIO: Risk-adjusted return metric
   - Higher Sharpe = better return per unit of risk taken
   - Use this to compare "bang for your buck"

5. DRAWDOWN: Peak-to-trough decline during downturns
   - Shows your worst potential loss at any point
   - Important for understanding downside risk
    """)
    
    plt.show()


if __name__ == "__main__":
    main()
