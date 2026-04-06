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
 
## Notes
 
- Does not account for brokerage fees or slippage
- Does not place live orders
