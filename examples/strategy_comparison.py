"""
Investment Strategy Comparison
Compare different investment approaches: DCA vs Lump Sum vs Buy & Hold
"""

from strategies import DollarCostAveraging, LumpSumInvestment, BuyAndHoldWithDividends
from visualizations import StockVisualizer
import matplotlib.pyplot as plt
import pandas as pd


def main():
    print("="*70)
    print("STRATEGY COMPARISON: DCA vs LUMP SUM vs BUY & HOLD")
    print("="*70)
    
    # Parameters
    ticker = 'AAPL'
    start_date = '2020-01-01'
    end_date = '2024-12-31'
    total_capital = 12000  # Total to invest
    
    print(f"\nParameters:")
    print(f"  Stock: {ticker}")
    print(f"  Period: {start_date} to {end_date}")
    print(f"  Total Capital: ${total_capital:,.2f}")
    print("\n" + "-"*70)
    
    # Strategy 1: Dollar-Cost Averaging ($1,000/month)
    print("\nStrategy 1: Dollar-Cost Averaging")
    print("  Invest $1,000 every month for 12 months")
    dca_strategy = DollarCostAveraging(ticker, 1000, frequency='monthly')
    dca_results = dca_strategy.backtest(start_date, end_date)
    
    # Strategy 2: Lump Sum Investment
    print("\nStrategy 2: Lump Sum Investment")
    print(f"  Invest all ${total_capital:,.2f} at the start")
    lump_strategy = LumpSumInvestment(ticker, total_capital)
    lump_results = lump_strategy.backtest(start_date, end_date)
    
    # Strategy 3: Buy & Hold with Dividends
    print("\nStrategy 3: Buy & Hold (Dividend Reinvestment)")
    print(f"  Invest all ${total_capital:,.2f} and reinvest dividends")
    bnh_strategy = BuyAndHoldWithDividends(ticker, total_capital)
    bnh_results = bnh_strategy.backtest(start_date, end_date)
    
    # Summary Table
    print("\n" + "="*70)
    print("RESULTS COMPARISON")
    print("="*70)
    
    results_list = [dca_results, lump_results, bnh_results]
    
    comparison_data = {
        'Strategy': [r.strategy_name for r in results_list],
        'Invested': [f"${r.total_invested:,.2f}" for r in results_list],
        'Final Value': [f"${r.final_value:,.2f}" for r in results_list],
        'Total Return': [f"${r.total_return:,.2f}" for r in results_list],
        'Return %': [f"{r.total_return_pct:>6.2%}" for r in results_list],
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    print("\n" + comparison_df.to_string(index=False))
    
    # Analysis
    print("\n" + "="*70)
    print("ANALYSIS")
    print("="*70)
    
    returns = [r.total_return_pct for r in results_list]
    best_idx = returns.index(max(returns))
    worst_idx = returns.index(min(returns))
    
    print(f"\n✓ Best Strategy: {results_list[best_idx].strategy_name}")
    print(f"  Return: {results_list[best_idx].total_return_pct:.2%}")
    print(f"  Gain: ${results_list[best_idx].total_return:,.2f}")
    
    print(f"\n✓ Worst Strategy: {results_list[worst_idx].strategy_name}")
    print(f"  Return: {results_list[worst_idx].total_return_pct:.2%}")
    print(f"  Gain: ${results_list[worst_idx].total_return:,.2f}")
    
    diff = results_list[best_idx].final_value - results_list[worst_idx].final_value
    print(f"\n✓ Difference: ${diff:,.2f}")
    
    # Visualizations
    print("\n" + "-"*70)
    print("Generating visualizations...")
    
    visualizer = StockVisualizer()
    
    # Strategy Comparison Chart
    fig1 = visualizer.plot_strategy_comparison(results_list)
    plt.savefig('strategy_comparison.png', dpi=100, bbox_inches='tight')
    print("  ✓ Saved: strategy_comparison.png")
    
    print("\n" + "="*70)
    print("KEY INSIGHTS")
    print("="*70)
    print("""
WHAT DID WE LEARN?

1. LUMP SUM vs DCA:
   - Lump sum provides exposure to market gains immediately
   - DCA reduces timing risk by spreading investments over time
   - In bull markets, lump sum typically wins
   - In bear markets, DCA can help avoid large losses

2. DOLLAR-COST AVERAGING (DCA):
   - Invest fixed amount at regular intervals
   - Reduces "timing the market" risk
   - Good for people who receive salary regularly
   - Emotionally easier during market downturns
   - Costs more in fees if trading frequently

3. LUMP SUM:
   - Best if you have a large amount to invest
   - Stays fully invested in the market longer
   - Historically wins in 2 of 3 market conditions
   - Risk: You might buy at the market peak

4. BUY & HOLD with DIVIDENDS:
   - Long-term wealth building strategy
   - Dividend reinvestment compounds returns
   - Less active management required
   - Good for retirement accounts

WHICH STRATEGY IS BEST?
   ✓ Best performer on average: Lump sum investing
   ✓ Most practical for salary earners: Dollar-cost averaging
   ✓ Best for long-term (20+ years): Buy & hold with dividends
   ✓ Most emotionally stable: Dollar-cost averaging
    """)
    
    plt.show()


if __name__ == "__main__":
    main()
