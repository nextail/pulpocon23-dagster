import pandas as pd
from dagster import In, Out, op


@op(
    ins={"df_stock": In(pd.DataFrame), "filtro": In(str)},
    out={"data": Out(pd.DataFrame)},
    description="Read stock and aggregate profit by filter",
)
def get_profit_by_filter(df_stock, filtro):
    df_stock["Profit"] = df_stock["Profit"].astype(float)
    df_profit = df_stock.groupby(filtro, as_index=False).Profit.sum()
    return df_profit


@op(
    ins={"df_stock": In(pd.DataFrame)},
    out={"data": Out(float)},
    description="Read stock and get profit",
)
def get_profit_total(df_stock):
    df_stock["Profit"] = df_stock["Profit"].astype(float)
    df_profit = df_stock.Profit.sum()
    return df_profit
