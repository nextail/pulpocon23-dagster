import datetime
from io import StringIO

import pandas as pd


def csv_str_to_df(csv_string: str) -> pd.DataFrame:
    return pd.read_csv(StringIO(csv_string))


ISO_DATE_FORMAT = "%Y-%m-%d"


def date_str_to_date(iso_date_str: str) -> datetime.date:
    return datetime.datetime.strptime(iso_date_str, ISO_DATE_FORMAT).date()


def date_to_date_str(date: datetime.date) -> str:
    return date.strftime(ISO_DATE_FORMAT)
