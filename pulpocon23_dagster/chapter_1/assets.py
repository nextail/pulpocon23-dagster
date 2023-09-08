import json

from dagster import AssetExecutionContext, AssetObservation, asset, graph_asset, job, op

STORE_STOCK = """{
    "date": "29/08/2023",
    "warehouse": [
        {"Item": "Shirts", "Stock": 3},
        {"Item": "Coats", "Stock": 10},
        {"Item": "Jeans", "Stock": 2}
    ]
}"""


@op
def daily_stock_op(context):
    store_data = json.loads(STORE_STOCK)
    daily_stock = sum(item["Stock"] for item in store_data["warehouse"])
    context.log.info(daily_stock)
    context.log_event(
        AssetObservation(
            asset_key="examples/daily_stock",
            metadata={"daily_stock": daily_stock},
        )
    )
    return daily_stock


@job
def daily_stock_job():
    daily_stock_op()


@graph_asset(key_prefix=["examples"], group_name="stock", name="daily_stock_asset_from_op")
def daily_stock_as_asset_from_op():
    daily_stock = daily_stock_op()
    return daily_stock


@asset(key_prefix=["examples"], group_name="stock", name="daily_stock_asset")
def daily_stock_asset(context: AssetExecutionContext):
    store_data = json.loads(STORE_STOCK)
    daily_stock = sum(item["Stock"] for item in store_data["warehouse"])
    context.log.info(daily_stock)
    return daily_stock


@asset(key_prefix=["examples"], group_name="stock", name="weekly_stock_asset", deps=[daily_stock_asset])
def weekly_stock_asset():
    pass


@asset(
    key_prefix=["examples"],
    group_name="forecast",
    name="forecast_next_month_asset",
    deps=[weekly_stock_asset, daily_stock_asset],
)
def forecast_next_month_asset():
    pass
