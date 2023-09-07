from numbers import Number

import pandas as pd
from dagster import AssetExecutionContext, DailyPartitionsDefinition, asset

from ...resources.postgres_resource import PostgresResource
from ...utils.time_series_dao import TimeSeriesDao


@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
)
def units_sold_db_direct_persistence(
    context: AssetExecutionContext,
    operational_data: pd.DataFrame,
    postgres: PostgresResource,
):
    dao = TimeSeriesDao("units_sold", postgres)
    value = int(operational_data["Quantity"].sum())
    context.add_output_metadata({"value": value})
    date = context.partition_key
    dao.upsert_record(date, value)


@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
)
def revenue_db_direct_persistence(
    context: AssetExecutionContext,
    operational_data: pd.DataFrame,
    postgres: PostgresResource,
):
    dao = TimeSeriesDao("revenue", postgres)
    value = float(operational_data["Sales"].sum())
    context.add_output_metadata({"value": value})
    dao.upsert_record(context.partition_key, value)


@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
    deps=[units_sold_db_direct_persistence, revenue_db_direct_persistence],
)
def average_sales_price_db_direct_persistence(
    context: AssetExecutionContext,
    postgres: PostgresResource,
):
    dao = TimeSeriesDao("average_sales_price", postgres)
    date = context.partition_key
    revenue_value = TimeSeriesDao("revenue", postgres).get_value(date)
    units_sold_value = TimeSeriesDao("units_sold", postgres).get_value(date)
    value = float(revenue_value / units_sold_value)
    context.add_output_metadata({"value": value})
    dao.upsert_record(date, value)


@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
    io_manager_key="partitioned_numeric_time_series_postgres_io_manager",
)
def units_sold_db_io_manager_persistence(
    context: AssetExecutionContext,
    operational_data: pd.DataFrame,
) -> int:
    value = int(operational_data["Quantity"].sum())
    context.add_output_metadata({"value": value})
    return value


@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
    io_manager_key="partitioned_numeric_time_series_postgres_io_manager",
)
def revenue_db_io_manager_persistence(
    context: AssetExecutionContext,
    operational_data: pd.DataFrame,
) -> float:
    value = float(operational_data["Sales"].sum())
    context.add_output_metadata({"value": value})
    return value


@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
    io_manager_key="partitioned_numeric_time_series_postgres_io_manager",
)
def average_sales_price_db_io_manager_persistence(
    context: AssetExecutionContext,
    units_sold_db_io_manager_persistence: Number,
    revenue_db_io_manager_persistence: Number,
) -> float:
    value = float(revenue_db_io_manager_persistence / units_sold_db_io_manager_persistence)
    context.add_output_metadata({"value": value})
    return value
