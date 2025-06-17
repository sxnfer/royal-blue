import logging
from copy import deepcopy
from datetime import datetime
from typing import List

import pandas as pd

from src.utils.custom_errors import InvalidEmptyList

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_data_frame_from_list(data: List[dict]) -> pd.DataFrame:
    """
    Converts a non-empty list of dictionaries into a pandas DataFrame.

    Args:
        data (List[dict]): The list of dictionary records to convert.

    Returns:
        pd.DataFrame: The resulting DataFrame.

    Raises:
        InvalidEmptyList: If the input list is empty.
    """
    if len(data):
        return pd.DataFrame(data)
    else:
        raise InvalidEmptyList("ERROR: List is empty")


def get_last_updated_from_raw_table_data(rows: List[dict]) -> datetime:
    """
    Extracts the most recent datetime from the 'last_updated' field in a list of dictionaries.

    Args:
        rows (List[dict]): The raw table data with datetime entries under the 'last_updated' key.

    Returns:
        datetime: The latest 'last_updated' datetime found.

    Raises:
        InvalidEmptyList: If the input list is empty.
    """
    if not len(rows):
        raise InvalidEmptyList("ERROR: List is empty")
    last_updated_column = "last_updated"
    list_of_datetimes = []
    for row in rows:
        if last_updated_column in row:
            value = row[last_updated_column]
            if isinstance(value, datetime):
                list_of_datetimes.append(value)

    return max(list_of_datetimes)


def initialize_table_state(current_state, table_name):
    """
    Ensures the ingest state for a given table exists in the current state dictionary.
    If not present, it initializes the table with default metadata.

    Args:
        current_state (dict): The current state containing ingest information.
        table_name (str): The name of the table to initialize.

    Returns:
        dict: The updated or unchanged state dictionary.
    """
    if current_state["ingest_state"].get(table_name):
        return current_state

    new_state = deepcopy(current_state)
    new_state["ingest_state"][table_name] = {
        "last_updated": None,
        "ingest_log": [],
    }
    return new_state


def create_parquet_metadata(
    new_table_data_last_updated: datetime, table_name: str
) -> tuple[str, str]:
    """
    Generates a filename and S3 key for storing a Parquet file based on a timestamp.

    Args:
        new_table_data_last_updated (datetime): The timestamp to include in the metadata.
        table_name (str): The name of the table the data belongs to.

    Returns:
        tuple[str, str]: A tuple containing the filename and the S3 key.
    """
    year = new_table_data_last_updated.year
    month = new_table_data_last_updated.month
    day = new_table_data_last_updated.day

    # currency_2025-06-13_10-35-20_012023.parquet
    filename = f"{table_name}_{year}-{month}-{day}_{new_table_data_last_updated.hour}-{new_table_data_last_updated.minute}-{new_table_data_last_updated.second}_{new_table_data_last_updated.microsecond}.parquet"

    # 2025/06/13/currency_2025-06-13_10-35-20_012023.parquet
    key = f"{year}/{month}/{day}/{filename}"

    return filename, key
