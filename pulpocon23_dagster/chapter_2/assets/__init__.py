import pandas as pd
from dagster import AssetExecutionContext, AssetIn, MarkdownMetadataValue, asset


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


# With basic managed-loading dependency (https://docs.dagster.io/concepts/assets/software-defined-assets#defining-basic-managed-loading-dependencies)
@asset
def revenue(context: AssetExecutionContext, operational_data: pd.DataFrame) -> float:
    value = float(
        operational_data["Sales"].sum()
    )  # Need to convert to float because numpy numeric types are not supported
    context.add_output_metadata({"value": value})
    return value


# With explicit managed-loading dependency (https://docs.dagster.io/concepts/assets/software-defined-assets#defining-explicit-managed-loading-dependencies)
@asset(
    ins={"upstream_operational_data": AssetIn(key=["operational_data"])},
    key="units_sold",  # default key (function name) can be overridden
)
def function_computing_units_sold(
    context: AssetExecutionContext, upstream_operational_data: pd.DataFrame
) -> int:
    value = int(upstream_operational_data["Quantity"].sum())
    context.add_output_metadata({"value": value})
    return value


@asset
def average_sales_price(
    context: AssetExecutionContext, revenue: float, units_sold: int
) -> float:
    value = revenue / units_sold
    context.add_output_metadata({"value": value})
    return value
