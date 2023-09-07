import pandas as pd
from dagster import AssetExecutionContext, MarkdownMetadataValue, asset


@asset
def operational_data(
    context: AssetExecutionContext,
) -> pd.DataFrame:
    data = pd.read_csv(
        "https://raw.githubusercontent.com/dfernandezcalle/stock-data/main/data/csv/2023-08-02/stock.csv"
    )
    context.add_output_metadata(
        {
            "num_records": len(data),
            "preview": MarkdownMetadataValue.md(data.head().to_markdown()),
        }
    )  # This metadata is a visual aid to ease our understanding of the assets we are manipulating
    return data
