from numbers import Number

import pandas as pd
from dagster import (
    AssetExecutionContext,
    AssetIn,
    DailyPartitionsDefinition,
    MarkdownMetadataValue,
    asset,
)

daily_partitioning = DailyPartitionsDefinition(
    start_date="2023-08-08", end_date="2023-09-08"
)


@asset(partitions_def=daily_partitioning, io_manager_key="s3_json_io_manager")
def operational_data(
    context: AssetExecutionContext,
) -> pd.DataFrame:
    date = context.partition_key
    source_path = f"https://raw.githubusercontent.com/dfernandezcalle/stock-data/main/data/csv/{date}/stock.csv"
    data = pd.read_csv(source_path)
    context.add_output_metadata(
        {
            "num_records": len(data),
            "preview": MarkdownMetadataValue.md(data.head().to_markdown()),
        }
    )  # This metadata is a visual aid to ease our understanding of the assets we are manipulating
    return data


# With basic managed-loading dependency (https://docs.dagster.io/concepts/assets/software-defined-assets#defining-basic-managed-loading-dependencies)
@asset(
    partitions_def=daily_partitioning,
    io_manager_key="partitioned_numeric_time_series_postgres_io_manager",
)
def revenue(context: AssetExecutionContext, operational_data: pd.DataFrame) -> float:
    value = float(
        operational_data["Sales"].sum()
    )  # Need to convert to float because numpy numeric types are not supported
    context.add_output_metadata({"value": value})
    return value


# With explicit managed-loading dependency (https://docs.dagster.io/concepts/assets/software-defined-assets#defining-explicit-managed-loading-dependencies)
@asset(
    ins={"upstream_operational_data": AssetIn(key=["operational_data"])},
    key="units_sold",  # default key (function name) can be overridden
    partitions_def=daily_partitioning,
    io_manager_key="partitioned_numeric_time_series_postgres_io_manager",
)
def function_computing_units_sold(
    context: AssetExecutionContext, upstream_operational_data: pd.DataFrame
) -> int:
    value = int(upstream_operational_data["Quantity"].sum())
    context.add_output_metadata({"value": value})
    return value


@asset(
    partitions_def=daily_partitioning,
    io_manager_key="partitioned_numeric_time_series_postgres_io_manager",
)
def average_sales_price(
    context: AssetExecutionContext, revenue: Number, units_sold: Number
) -> float:
    value = float(revenue / units_sold)
    context.add_output_metadata({"value": value})
    return value
