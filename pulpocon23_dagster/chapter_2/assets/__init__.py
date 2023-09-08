import pandas as pd
from dagster import (
    AssetExecutionContext,
    AssetIn,
    DailyPartitionsDefinition,
    MarkdownMetadataValue,
    asset,
)

from ..resources.postgres_resource import PostgresResource
from ..utils.time_series_dao import TimeSeriesDao

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


# Taking persistence into our own hands, using basic dependency https://docs.dagster.io/concepts/assets/software-defined-assets#defining-basic-dependencies
@asset(partitions_def=daily_partitioning)
def revenue(
    context: AssetExecutionContext,
    operational_data: pd.DataFrame,
    postgres: PostgresResource,
):
    value = float(
        operational_data["Sales"].sum()
    )  # Need to convert to float because numpy numeric types are not supported
    context.add_output_metadata({"value": value})
    dao = TimeSeriesDao("revenue", postgres)
    date = context.partition_key
    dao.upsert_record(date, value)


@asset(
    ins={"upstream_operational_data": AssetIn(key=["operational_data"])},
    key="units_sold",  # default key (function name) can be overridden
    partitions_def=daily_partitioning,
)
def function_computing_units_sold(
    context: AssetExecutionContext,
    upstream_operational_data: pd.DataFrame,
    postgres: PostgresResource,
):
    value = int(upstream_operational_data["Quantity"].sum())
    context.add_output_metadata({"value": value})
    dao = TimeSeriesDao("units_sold", postgres)
    date = context.partition_key
    dao.upsert_record(date, value)


# We go back to explicitly define dependencies between assets, as well as extracting / loading
@asset(partitions_def=daily_partitioning, deps=[revenue, function_computing_units_sold])
def average_sales_price(context: AssetExecutionContext, postgres: PostgresResource):
    date = context.partition_key
    revenue = TimeSeriesDao("revenue", postgres).get_value(date)
    units_sold = TimeSeriesDao("units_sold", postgres).get_value(date)
    value = float(revenue / units_sold)
    context.add_output_metadata({"value": value})
    dao = TimeSeriesDao("average_sales_price", postgres)
    dao.upsert_record(date, value)
