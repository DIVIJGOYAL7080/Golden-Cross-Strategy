# Golden Cross Strategy
 
Backtests the golden cross strategy on SPY using Interactive Brokers as the data source.
 
## What it does
 
Computes a 50-day and 200-day moving average on daily close prices. When the 50 crosses above the 200 it buys, when it crosses below it sells. Runs two versions — long-short and long-only — and prints Sharpe, Sortino, max drawdown and final capital.
 
SPY was chosen over individual stocks as it trends more cleanly and has less noise, making it better suited for a crossover strategy.
 
## Requirements
 
```bash
pip install ib_async pandas numpy
```
 
IBKR Gateway must be running on port 4002 with the Historical Data Farm active.
 
## Usage
 
```bash
python golden_cross.py
```
 
Change the symbol at the bottom of the file:
 
```python
symbol = "SPY"  # any SMART/USD listed symbol
```
 
## Sample Output
 
```
Long-Short Results:
  Initial Capital  : $100,000.00
  Final Capital    : $112,840.23
  Sharpe Ratio     : 0.67
  Sortino Ratio    : 0.72
  Maximum Drawdown : -14.30%
 
Long-Only Results:
  Initial Capital  : $100,000.00
  Final Capital    : $134,210.45
  Sharpe Ratio     : 0.84
  Sortino Ratio    : 0.91
  Maximum Drawdown : -18.50%
```
 
## Notes
 
- Error handling and diagnostic messages written with AI assistance
- Does not account for brokerage fees or slippage
- Does not place live orders
