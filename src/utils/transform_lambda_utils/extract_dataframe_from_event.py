from typing import Dict

import boto3
import pandas as pd

from src.utils.parquets.create_data_frame_from_parquet import (
    create_data_frame_from_parquet,
)
from src.utils.s3.get_file_from_s3_bucket import get_file_from_s3_bucket

BUCKET_NAME = "ingestion-zone-20250530151335299400000005"
client = boto3.client("s3")


def get_dataframes_from_event(client, event) -> Dict[str, pd.DataFrame]:
    """
    Extracts data from a list of S3 Parquet file metadata and returns table-specific DataFrames.

    Args:
        client (BaseClient): A Boto3 S3 client instance.
        event (List[Dict[str, str]]): List of metadata dicts, each containing:
            - 'table_name': str
            - 'extraction_timestamp': str
            - 'last_updated': str
            - 'file_name': str
            - 'key': str (S3 object path)

    Returns:
        Dict[str, pd.DataFrame]: A dictionary mapping each table name to its corresponding DataFrame.

    Raises:
        Exception: If a table's data cannot be fetched or converted from S3.
    """
    extracted_data_frames = {}

    for table in event:
        key = table["key"]
        table_name = table["table_name"]

        try:
            s3_result = get_file_from_s3_bucket(client, BUCKET_NAME, key)

            if not s3_result.get("success") or "data" not in s3_result["success"]:
                raise Exception(s3_result["error"]["message"])

            parquet_bytes = s3_result["success"]["data"]
            data_frame = create_data_frame_from_parquet(parquet_bytes)
            extracted_data_frames[table_name] = data_frame

        except Exception as e:
            raise Exception(f"Error processing table '{table_name}': {e}")

    return extracted_data_frames
