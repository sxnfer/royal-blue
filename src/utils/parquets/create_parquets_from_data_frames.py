from datetime import datetime
from io import BytesIO
from typing import Any, Dict, Union

import pandas as pd


def create_parquets_from_data_frames(
    data: list,
) -> Dict[str, Union[Dict[str, Any], Dict[str, str]]]:
    """
    Converts a list of data frames into in-memory Parquet files.

    This function receives a list of dictionaries where each dictionary represents a table
    with metadata and a pandas DataFrame. It serializes each DataFrame into a compressed
    Parquet file stored in a BytesIO buffer.

    If any conversion fails, the function returns an error dictionary containing the table name
    and the error message. Otherwise, it returns a success dictionary with all converted files.

    Args:
        data (list): A list of dictionaries, each containing:
            - table_name (str): Name of the table.
            - last_updated (str): ISO timestamp of the latest data update.
            - data_frame (pandas.DataFrame): DataFrame to be serialized.

    Returns:
        dict: A JSON-style response indicating success or failure.

        Success:
            {
                "success": {
                    "message": "Parquet file conversion successful.",
                    "data": [
                        {
                            "table_name": "example_table",
                            "last_updated": "2025-05-27 12:00:00",
                            "parquet_file": <_io.BytesIO>
                        },
                        ...
                    ]
                }
            }

        Error:
            {
                "error": {
                    "message": "table_name: error_description"
                }
            }
    """
    parquet_files = []

    for table in data:
        table_name: str = table.get("table_name")
        last_updated: datetime = table.get("last_updated")
        data_frame = table.get("data_frame")

        if not isinstance(data_frame, pd.DataFrame):
            return {"error": {"message": f"{table_name}: invalid data type."}}

        buffer: BytesIO = BytesIO()

        try:
            data_frame.to_parquet(buffer, engine="pyarrow", compression="gzip")
            buffer.seek(0)

            parquet_files.append(
                {
                    "table_name": table_name,
                    "last_updated": last_updated,
                    "parquet_file": buffer,
                }
            )
        except Exception as err:
            return {"error": {"message": f"{table_name}: {err}"}}

    return {
        "success": {
            "message": "Parquet file conversion successful.",
            "data": parquet_files,
        }
    }
