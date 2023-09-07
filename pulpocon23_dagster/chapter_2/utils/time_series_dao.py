import datetime
from numbers import Number
from typing import Optional, Union

from ..resources.postgres_resource import PostgresResource


class TimeSeriesDao:
    def __init__(self, table_name: str, postgres: PostgresResource) -> None:
        self._table_name = table_name
        self._postgres = postgres

    def upsert_record(self, date: Union[datetime.date, str], numeric_value: Number):
        self._postgres.execute(f"""
          INSERT INTO {self._table_name}(date, value)
          VALUES ('{date}', {numeric_value})
            ON CONFLICT(date)
            DO
              UPDATE SET value=excluded.value
        """)

    def get_value(self, date: Union[datetime.date, str]) -> Optional[Number]:
        result = self._postgres.query(f"""
          SELECT value FROM {self._table_name}
          WHERE date = '{date}'
        """)
        return None if len(result) == 0 else result[0][0]
