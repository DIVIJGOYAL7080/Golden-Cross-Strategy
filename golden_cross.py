import pandas as pd
import numpy as np
import datetime
from ib_async import *


class goldenCross:

    def __init__(self, df: pd.DataFrame, long_period: int, short_period: int):
        self.df = df
        self.short_period = short_period
        self.long_period = long_period
        self.validate_dataframe()
        self.compute_indicators()

    def validate_dataframe(self):
        required_columns = {"open", "high", "low", "close"}
        if not isinstance(self.df, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame.")
        if not required_columns.issubset(self.df.columns):
            missing = required_columns - set(self.df.columns)
            raise ValueError(f"DataFrame is missing required columns: {missing}")
        if self.df.isnull().any().any():
            self.df.ffill(inplace=True)
            self.df.bfill(inplace=True)

    def compute_indicators(self):
        self.df["long_average"] = self.df["close"].rolling(window=self.long_period).mean()
        self.df["short_average"] = self.df["close"].rolling(window=self.short_period).mean()
        self.df["long_average"] = self.df["long_average"].ffill().bfill()
        self.df["short_average"] = self.df["short_average"].ffill().bfill()

    def generate_signals(self):
        self.df["signals"] = 0
        cross_up = (
            (self.df["short_average"] > self.df["long_average"]) &
            (self.df["short_average"].shift(1) <= self.df["long_average"].shift(1))
        )
        cross_down = (
            (self.df["short_average"] < self.df["long_average"]) &
            (self.df["short_average"].shift(1) >= self.df["long_average"].shift(1))
        )
        self.df.loc[cross_up, "signals"] = 1
        self.df.loc[cross_down, "signals"] = -1

    def get_strategy_frame(self):
        return self.df


def fetch_data_from_ib(symbol: str) -> pd.DataFrame:
    end_date = datetime.datetime.now().replace(
        hour=23, minute=59, second=59
    ).strftime('%Y%m%d %H:%M:%S UTC')

    contract = Stock(symbol, 'SMART', 'USD')
    ib = IB()
    stock_df = pd.DataFrame()

    ib.connect("127.0.0.1", 4002, clientId=1, timeout=10, readonly=False)

    if not ib.client.isReady():
        print("connection failed, check gateway is running on port 4002")
        ib.disconnect()
        return stock_df

    try:
        ib.qualifyContracts(contract)
        bars = ib.reqHistoricalData(
            contract,
            endDateTime=end_date,
            durationStr="5 Y",
            barSizeSetting="1 day",
            whatToShow='TRADES',
            useRTH=False,
            formatDate=1
        )

        if not bars:
            print(f"no data returned for {symbol}, check your IB data subscription")
            ib.disconnect()
            return stock_df

        stock_df = util.df(bars)
        stock_df.columns = [c.lower() for c in stock_df.columns]
        stock_df = stock_df.ffill()

    except Exception as e:
        print(f"error fetching data: {e}")
    finally:
        ib.disconnect()

    return stock_df


def test_strategy(df: pd.DataFrame, initial_capital: float):
    starting_capital = initial_capital

    df["returns"] = df["close"].pct_change()
    df["strategy_returns"] = df["returns"] * df["signals"].shift(1)
    df["cumulative_strategy_returns"] = (1 + df["strategy_returns"]).cumprod()
    df["cumulative_returns"] = (1 + df["returns"]).cumprod()
    df["capital"] = starting_capital * df["cumulative_strategy_returns"]

    final_capital = df["capital"].iloc[-1]
    daily_return_mean = df["strategy_returns"].mean()
    daily_return_std = df["strategy_returns"].std(ddof=1)

    sharpe_ratio = (
        (daily_return_mean / daily_return_std) * np.sqrt(252)
        if daily_return_std > 0 else np.nan
    )

    downside_returns = df["strategy_returns"][df["strategy_returns"] < 0]
    downside_std = downside_returns.std(ddof=1)
    sortino_ratio = (
        (daily_return_mean / downside_std) * np.sqrt(252)
        if downside_std > 0 else np.nan
    )

    peak = df["capital"].cummax()
    max_drawdown = ((df["capital"] - peak) / peak).min()

    print("Long-Short Results:")
    print(f"  Initial Capital  : ${starting_capital:,.2f}")
    print(f"  Final Capital    : ${final_capital:,.2f}")
    print(f"  Sharpe Ratio     : {sharpe_ratio:.2f}")
    print(f"  Sortino Ratio    : {sortino_ratio:.2f}")
    print(f"  Maximum Drawdown : {max_drawdown * 100:.2f}%")

    return df


def test_strategy_long_only(df: pd.DataFrame, initial_capital: float):
    starting_capital = initial_capital

    df["returns"] = df["close"].pct_change()

    position = 0
    positions = [0]
    for i in range(1, len(df)):
        signal = df.loc[i, "signals"]
        if signal == 1 and position == 0:
            position = 1
        elif signal == -1 and position == 1:
            position = 0
        positions.append(position)

    df["position"] = positions
    df["strategy_returns"] = df["returns"] * df["position"].shift(1).fillna(0)
    df["cumulative_strategy_returns"] = (1 + df["strategy_returns"]).cumprod()
    df["cumulative_returns"] = (1 + df["returns"]).cumprod()
    df["capital"] = starting_capital * df["cumulative_strategy_returns"]

    final_capital = df["capital"].iloc[-1]
    daily_return_mean = df["strategy_returns"].mean()
    daily_return_std = df["strategy_returns"].std(ddof=1)

    sharpe_ratio = (
        (daily_return_mean / daily_return_std) * np.sqrt(252)
        if daily_return_std > 0 else np.nan
    )

    downside_returns = df["strategy_returns"][df["strategy_returns"] < 0]
    downside_std = downside_returns.std(ddof=1)
    sortino_ratio = (
        (daily_return_mean / downside_std) * np.sqrt(252)
        if downside_std > 0 else np.nan
    )

    peak = df["capital"].cummax()
    max_drawdown = ((df["capital"] - peak) / peak).min()

    print("Long-Only Results:")
    print(f"  Initial Capital  : ${starting_capital:,.2f}")
    print(f"  Final Capital    : ${final_capital:,.2f}")
    print(f"  Sharpe Ratio     : {sharpe_ratio:.2f}")
    print(f"  Sortino Ratio    : {sortino_ratio:.2f}")
    print(f"  Maximum Drawdown : {max_drawdown * 100:.2f}%")

    return df


if __name__ == "__main__":
    symbol = "SPY"
    stock_df = fetch_data_from_ib(symbol)

    if stock_df.empty:
        exit(1)

    gs = goldenCross(stock_df, long_period=200, short_period=50)
    gs.generate_signals()

    strategy_df = gs.get_strategy_frame().reset_index(drop=True)

    print("\n" + "=" * 40)
    test_strategy(strategy_df.copy(), initial_capital=100000)

    print("\n" + "=" * 40)
    test_strategy_long_only(strategy_df.copy(), initial_capital=100000)