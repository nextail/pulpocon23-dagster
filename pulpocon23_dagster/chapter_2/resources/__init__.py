import datetime

import requests
from dagster import ConfigurableResource

from ..utils.data_transformation import date_to_date_str


class OperationalDataRepository(ConfigurableResource):
    url_base: str

    def get_csv_for_date(self, date: datetime.date) -> str:  # Check if it would make sense to change to CSV
        csv_file_path = f"{date_to_date_str(date)}/stock.csv"  # Change to data.csv when we rename data
        return self.get_csv(csv_file_path)

    def get_csv(self, csv_file_path) -> str:  # Check if it would make sense to change to CSV
        return self._get_data(f"csv/{csv_file_path}").text

    def _get_data(self, url_path):
        return requests.get(f"{self.url_base}/{url_path}")


# In a real world context, this value would be provided by an environment variable
operational_data_repository = OperationalDataRepository(
    url_base="https://raw.githubusercontent.com/dfernandezcalle/stock-data/main/data"
)
