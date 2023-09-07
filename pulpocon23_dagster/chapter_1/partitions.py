import pandas as pd
from dagster import DailyPartitionsDefinition, Output, asset
from pandas import DataFrame


@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2023-09-04"),
    key_prefix=["example"],
    group_name="partitions",
)
def partition_asset(context) -> Output[DataFrame]:
    partition_date = context.asset_partition_key_for_output()
    data = pd.read_csv(
        f"https://raw.githubusercontent.com/dfernandezcalle/stock-data/main/data/csv/{partition_date}/stock.csv"
    )
    return Output(data, metadata={"lines": len(data.index)})
