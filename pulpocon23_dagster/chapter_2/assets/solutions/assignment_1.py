import pandas as pd
from dagster import AssetExecutionContext, MetadataValue, asset


@asset
def example_operational_data(
    context: AssetExecutionContext,
) -> pd.DataFrame:
    operational_data = pd.read_csv(
        "https://raw.githubusercontent.com/dfernandezcalle/stock-data/main/data/csv/2023-08-02/stock.csv"
    )
    context.add_output_metadata(
        {
            "num_records": len(operational_data),
            "preview": MetadataValue.md(operational_data.head().to_markdown()),
        }
    )
    return operational_data
