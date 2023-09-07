import pandas as pd
from dagster import AssetExecutionContext, asset


@asset
def example_units_sold(
    context: AssetExecutionContext,
    example_operational_data: pd.DataFrame,  # Asset is referenced only through its asset key in this case (referencing could also be more explicit)
) -> int:
    # Cast to int to avoid compatibility problems with numpy data types
    result = int(example_operational_data["Quantity"].sum())
    context.add_output_metadata({"value": result})
    return result


@asset
def example_revenue(
    context: AssetExecutionContext,
    example_operational_data: pd.DataFrame,  # Asset is referenced only through its asset key in this case
) -> float:
    # Cast to float to avoid compatibility problems with numpy data types
    result = float(example_operational_data["Sales"].sum())
    context.add_output_metadata({"value": result})
    return result


@asset
def example_average_sales_price(
    context: AssetExecutionContext,
    example_units_sold: int,
    example_revenue: float,
) -> float:
    result = example_revenue / example_units_sold
    context.add_output_metadata({"value": result})
    return result
