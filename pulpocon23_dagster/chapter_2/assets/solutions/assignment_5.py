
import pandas as pd
from dagster import AssetExecutionContext, DailyPartitionsDefinition, MetadataValue, asset

from ...resources import OperationalDataRepository
from ...utils.data_transformation import csv_str_to_df, date_str_to_date


@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
    io_manager_key="s3_json_io_manager",
)
def operational_data(
    context: AssetExecutionContext,
    operational_data_repository: OperationalDataRepository,
) -> pd.DataFrame:
    partition_date = date_str_to_date(context.partition_key)
    csv_data = operational_data_repository.get_csv_for_date(partition_date)
    operational_data = csv_str_to_df(csv_data)
    context.add_output_metadata(
        {"num_records": len(operational_data), "preview": MetadataValue.md(operational_data.head().to_markdown())}
    )
    return operational_data


# TODO: Think about whether we should an example with direct persistence and explicit dependencies


@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
    io_manager_key="s3_json_io_manager",
)
def units_sold(
    context: AssetExecutionContext,
    operational_data: pd.DataFrame,
) -> int:
    result = int(operational_data["Quantity"].sum())
    context.add_output_metadata({"value": result})
    return result


@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
    io_manager_key="s3_json_io_manager",
)
def revenue(
    context: AssetExecutionContext,
    operational_data: pd.DataFrame,
) -> float:
    result = float(operational_data["Sales"].sum())
    context.add_output_metadata({"value": result})
    return result


@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
    io_manager_key="s3_json_io_manager",
)
def average_sales_price(
    context: AssetExecutionContext,
    units_sold: int,
    revenue: float,
) -> float:
    result = revenue / units_sold
    context.add_output_metadata({"value": result})
    return result
