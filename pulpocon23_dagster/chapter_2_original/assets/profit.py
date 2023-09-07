from dagster import AssetIn, DailyPartitionsDefinition, Output, asset
from pandas import DataFrame

from pulpocon23_dagster.chapter_2_original.ops.get_profit import get_profit_by_filter, get_profit_total


@asset(
    io_manager_key="s3_io_manager",
    ins={"stock": AssetIn(key="daily_stock")},
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
    key_prefix=["profit"],
    group_name="business_process",
)
def total_profit(context, stock) -> Output[float]:
    partition_date = context.asset_partition_key_for_output()
    data = get_profit_total(stock)
    context.log.debug(data)
    return Output(
        data,
        metadata={
            "date": partition_date,
            "profit": data,
        },
    )


@asset(
    io_manager_key="s3_io_manager",
    ins={"stock": AssetIn(key="daily_stock")},
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
    key_prefix=["profit"],
    group_name="business_process",
)
def by_category_profit(context, stock) -> Output[DataFrame]:
    partition_date = context.asset_partition_key_for_output()
    data = get_profit_by_filter(stock, filtro="Category")
    context.log.debug(data.to_json(orient="records", lines=True))
    categories = data.loc[:, "Category"].values.tolist()
    return Output(
        data,
        metadata={
            "date": partition_date,
            "categories": f"{categories}",
            "result": data.to_json(orient="records", lines=True),
        },
    )
