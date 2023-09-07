from dagster import DailyPartitionsDefinition, Output, asset
from pandas import DataFrame

from pulpocon23_dagster.chapter_2_original.ops.get_stock import get_stock


@asset(
    io_manager_key="s3_io_manager",
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
    key_prefix=["stock"],
    group_name="business_process",
)
def daily_stock(context) -> Output[DataFrame]:
    partition_date = context.asset_partition_key_for_output()
    data = get_stock(partition_date)
    return Output(data, metadata={"date": partition_date, "lines": len(data.index)})
