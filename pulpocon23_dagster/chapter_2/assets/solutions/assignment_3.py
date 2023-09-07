import pandas as pd
from dagster import AssetExecutionContext, Config, MetadataValue, asset
from pydantic import Field


class OperationalDataConfig(Config):
    source_data_path: str = Field(description="The path to the source of a chunk of operational data")


@asset
def example_configurable_operational_data(
    context: AssetExecutionContext,
    config: OperationalDataConfig,
) -> pd.DataFrame:
    operational_data = pd.read_csv(config.source_data_path)
    context.add_output_metadata(
        {
            "num_records": len(operational_data),
            "preview": MetadataValue.md(operational_data.head().to_markdown()),
        }
    )
    return operational_data
