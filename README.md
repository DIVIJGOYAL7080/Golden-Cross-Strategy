# Golden Cross Strategy
 
Backtests the golden cross strategy on NSE stocks using Interactive Brokers as the data source.
 
## What it does
 
Computes a 50-day and 200-day moving average on daily close prices. When the 50 crosses above the 200 it buys, when it crosses below it sells. Runs two versions — long-short and long-only — and prints Sharpe, Sortino, max drawdown and final capital.
 
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
symbol = "SBIN"  # any NSE symbol
```
 
## Sample Output
 
```
[IB] Connecting to gateway on port 4002 with clientId=1 ...
[IB] Connected. Fetching 5Y daily data for SBIN ...
[IB] Data fetched successfully. Rows: 1234
 
=============================================
Long-Short Results
=============================================
📈 Long-Short Strategy Backtest Results:
  Initial Capital  : 100,000.00
  Final Capital    : 100,607.54
  Sharpe Ratio     : 0.10
  Sortino Ratio    : 0.01
  Maximum Drawdown : -1.98%
 
=============================================
Long-Only Results
=============================================
📈 Long-Only Strategy Backtest Results:
  Initial Capital  : 100,000.00
  Final Capital    : 149,684.35
  Sharpe Ratio     : 0.49
  Sortino Ratio    : 0.56
  Maximum Drawdown : -22.60%
```
 
## Notes
 
- Does not account for brokerage fees or slippage
- Does not place live orders
 
