from dagster import Definitions, FilesystemIOManager

from .assets import (
    daily_stock_as_asset_from_op,
    daily_stock_asset,
    daily_stock_job,
    forecast_next_month_asset,
    weekly_stock_asset,
)
from .configuration import recover_name_asset, recover_name_job
from .input_output_types import number_validation_job
from .io_managers import give_me_five_asset
from .op_graph_job import math_job
from .partitions import partition_asset
from .resources import CredentialsResource, recover_credentials_asset

defs = Definitions(
    assets=[
        daily_stock_as_asset_from_op,
        daily_stock_asset,
        weekly_stock_asset,
        forecast_next_month_asset,
        recover_credentials_asset,
        recover_name_asset,
        partition_asset,
        give_me_five_asset,
    ],
    jobs=[math_job, daily_stock_job, number_validation_job, recover_name_job],
    resources={
        "credentials": CredentialsResource(
            username="foo",
            password="bar",
        ),
        "fs_io_manager": FilesystemIOManager(),
    },
)
