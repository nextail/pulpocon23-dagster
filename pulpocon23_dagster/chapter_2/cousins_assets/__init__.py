import pandas as pd
from dagster import AssetExecutionContext, DailyPartitionsDefinition, asset

from ..resources.postgres_resource import PostgresResource
from ..utils.time_series_dao import TimeSeriesDao

"""
Dear cousin, I got DB persistence to work but couldn't quite figure out how to do it more elegantly with an IO manager.
Hope you find a way to finish my work!


"""


@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
)
def units_sold(
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
def revenue(
    context: AssetExecutionContext,
    operational_data: pd.DataFrame,
    postgres: PostgresResource,
):
    dao = TimeSeriesDao("revenue", postgres)
    value = float(operational_data["Sales"].sum())
    context.add_output_metadata({"value": value})
    dao.upsert_record(context.partition_key, value)


@asset(partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"), deps=[units_sold, revenue])
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
