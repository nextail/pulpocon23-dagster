from dagster import Definitions, FilesystemIOManager, load_assets_from_package_module
from dagster_aws.s3 import S3Resource

from . import assets as my_assets
from .jobs.test_postgres import introspect_table_job
from .resources import operational_data_repository
from .resources.partitioned_numeric_time_series_postgres_io_manager import PartitionedNumericTimeSeriesPostgresIOManager
from .resources.postgres_resource import PostgresResource
from .resources.s3_json_io_manager import S3JsonIOManager

asset_definitions = load_assets_from_package_module(
    package_module=my_assets,
    group_name="chapter_2",
    key_prefix="chapter_2",
)

file_system_io_manager = FilesystemIOManager(base_dir="data/pickled")
# TODO: Configure with env variable
s3_resource = S3Resource(region_name="eu-west-1", endpoint_url="http://localstack:4566")
s3_json_io_manager = S3JsonIOManager(s3_resource=s3_resource, s3_bucket="dagster", s3_prefix="json")
# TODO: Configure with env variables
postgres_resource = PostgresResource(
    hostname="postgres_db",
    port="5432",
    username="postgres_user",
    password="postgres_password",
    db_name="workshop_assets",
)
partitioned_numeric_time_series_postgres_io_manager = PartitionedNumericTimeSeriesPostgresIOManager(
    postgres_resource=postgres_resource
)


definitions = Definitions(
    assets=asset_definitions,
    jobs=[introspect_table_job],
    resources={
        "operational_data_repository": operational_data_repository,
        "io_manager": file_system_io_manager,
        "s3_json_io_manager": s3_json_io_manager,
        "postgres": postgres_resource,
        "partitioned_numeric_time_series_postgres_io_manager": partitioned_numeric_time_series_postgres_io_manager,
    },
)
