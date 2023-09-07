import pandas as pd
from dagster import In, Out, op

url = "https://raw.githubusercontent.com/dfernandezcalle/stock-data/main/data/csv/"


@op(ins={"date": In(str)}, out={"data": Out(pd.DataFrame)}, description="Read stock from csv file")
def get_stock(date):
    stock_url = f"{url}/{date}/stock.csv"
    return pd.read_csv(stock_url)
