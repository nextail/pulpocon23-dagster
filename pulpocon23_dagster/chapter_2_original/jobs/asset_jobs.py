from dagster import DailyPartitionsDefinition
from dagster._core.definitions.unresolved_asset_job_definition import define_asset_job

business_process_job = define_asset_job(
    name="business_process_job", partitions_def=DailyPartitionsDefinition(start_date="2023-08-02")
)
daily_stock_job = define_asset_job(
    name="daily_stock_job",
    selection="stock/daily_stock",
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
)
total_profit_job = define_asset_job(
    name="total_profit_job",
    selection="profit/total_profit",
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
)
by_category_profit_job = define_asset_job(
    name="by_category_profit_job",
    selection="profit/by_category_profit",
    partitions_def=DailyPartitionsDefinition(start_date="2023-08-02"),
)
