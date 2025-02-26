import time

import pandas as pd
import polars as pl


def pandas_calculate_moving_average(df, period=200):
    df[f"{period}dma"] = df.groupby("name")["close"].transform(lambda x: x.rolling(window=period, min_periods=1).mean())
    df.loc[df.groupby('name').head(period - 1).index, f"{period}dma"] = None
    return df


def pandas_calculate_rsi(df, period=200):
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period, min_periods=1).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period, min_periods=1).mean()

    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    return df


def pandas_calculate_stochastic_oscillator(df, period=14):
    df["low_min"] = df.groupby("name")["low"].transform(lambda x: x.rolling(window=period, min_periods=1).min())
    df["high_max"] = df.groupby("name")["high"].transform(lambda x: x.rolling(window=period, min_periods=1).max())
    df.loc[df.groupby('name').head(period - 1).index, ["low_min", "high_max"]] = None

    df["stochastic_oscillator"] = 100 * ((df["close"] - df["low_min"]) / (df["high_max"] - df["low_min"]))

    df.drop(columns=["low_min", "high_max"], inplace=True)

    return df


def pandas_calculate_roc(df, period=14):
    df["ROC"] = df.groupby("name")["close"].transform(lambda x: (x - x.shift(period)) / x.shift(period) * 100)

    return df


def pandas_add_indicators(df):
    df = df.sort_values(by=["name", "date"])
    df = pandas_calculate_moving_average(df)
    df = pandas_calculate_rsi(df)
    df = pandas_calculate_stochastic_oscillator(df)
    df = pandas_calculate_roc(df)
    return df


def polars_calculate_moving_average(df, period):
    df = df.with_columns(
        pl.col("close").rolling_mean(200).over("name").alias(f"{period}dma")
    )
    return df


def polars_calculate_rsi(df, period=14):
    delta = df["close"].diff()

    gain = pl.when(delta > 0).then(delta).otherwise(0).rolling_mean(window_size=period, min_periods=1)
    loss = pl.when(delta < 0).then(-delta).otherwise(0).rolling_mean(window_size=period, min_periods=1)

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    df = df.with_columns(rsi.alias("RSI"))

    return df


def polars_calculate_stochastic_oscillator(df, period=14):
    low_min = df.select(["name", "date", pl.col("low").rolling_min(period).alias("low_min")])
    high_max = df.select(["name", "date", pl.col("high").rolling_max(period).alias("high_max")])
    df = df.join(low_min, on=["name", "date"]).join(high_max, on=["name", "date"])
    df = df.with_columns(
        ((df["close"] - df["low_min"]) / (df["high_max"] - df["low_min"]) * 100).alias("stochastic_oscillator")
    )
    return df.drop(["low_min", "high_max"])


def polars_calculate_roc(df, period=14):
    df = df.with_columns(((df["close"] - df["close"].shift(period)) / df["close"].shift(period) * 100).alias("ROC"))
    return df


def polars_add_indicators(df):
    df = df.sort(["name", "date"])
    df = polars_calculate_moving_average(df, 14)
    df = polars_calculate_rsi(df)
    df = polars_calculate_stochastic_oscillator(df)
    df = polars_calculate_roc(df)
    return df


def benchmark_pandas_vs_polars(file_path):
    start = time.time()
    pd_df = pd.read_csv(file_path)
    result = pandas_add_indicators(pd_df)
    end = time.time() - start
    print(f"Pandas processing time: {end:.2f}s")

    start = time.time()
    pl_df = pl.read_csv(file_path)
    polars_add_indicators(pl_df)
    end = time.time() - start
    print(f"Polars processing time: {end:.2f}s")

    return result


