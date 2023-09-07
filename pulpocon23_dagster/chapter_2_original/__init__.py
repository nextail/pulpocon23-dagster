from dagster import Definitions
from dagster_aws.s3 import ConfigurablePickledObjectS3IOManager, S3Resource

from pulpocon23_dagster.chapter_2_original.assets.profit import by_category_profit, total_profit
from pulpocon23_dagster.chapter_2_original.assets.stock import daily_stock
from pulpocon23_dagster.chapter_2_original.jobs.asset_jobs import (
    business_process_job,
    by_category_profit_job,
    daily_stock_job,
    total_profit_job,
)
from pulpocon23_dagster.chapter_2_original.utils.codespace import endpoint_checker

defs = Definitions(
    assets=[daily_stock, by_category_profit, total_profit],
    resources={
        "s3_io_manager": ConfigurablePickledObjectS3IOManager(
            s3_resource=S3Resource(region_name="eu-west-1", endpoint_url=endpoint_checker()),
            s3_bucket="dagster",
            s3_prefix="business_process",
        )
    },
    jobs=[business_process_job, daily_stock_job, total_profit_job, by_category_profit_job],
)
