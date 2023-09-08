from numbers import Number

from dagster import AssetKey, ConfigurableIOManager, InputContext, OutputContext

from ..utils.time_series_dao import TimeSeriesDao
from .postgres_resource import PostgresResource


class PartitionedNumericTimeSeriesPostgresIOManager(ConfigurableIOManager):
    """
    Hyper-specific and not robust, do not use un production!

    """

    postgres_resource: PostgresResource

    def handle_output(self, context: OutputContext, obj):
        assert isinstance(obj, Number)

        date = context.asset_partition_key
        dao = self._create_dao_for_asset(context.asset_key)
        dao.upsert_record(date, obj)

    def load_input(self, context: InputContext) -> Number:
        date = context.asset_partition_key
        dao = self._create_dao_for_asset(context.asset_key)
        return dao.get_value(date)

    def _create_dao_for_asset(self, asset_key: AssetKey) -> TimeSeriesDao:
        asset_name = asset_key.path[-1]
        return TimeSeriesDao(table_name=asset_name, postgres=self.postgres_resource)
